use bevy::{
    anti_alias::AntiAliasPlugin,
    app::{PanicHandlerPlugin, PluginsState, ScheduleRunnerPlugin, TerminalCtrlCHandlerPlugin},
    asset::UnapprovedPathMode,
    camera::{CameraPlugin, primitives::Aabb},
    color::palettes::css::{BLACK, WHITE},
    core_pipeline::CorePipelinePlugin,
    diagnostic::{DiagnosticsPlugin, FrameCountPlugin},
    gltf::GltfPlugin,
    light::LightPlugin,
    log::LogPlugin,
    mesh::MeshPlugin,
    pbr::PbrPlugin,
    post_process::PostProcessPlugin,
    prelude::*,
    render::{
        RenderPlugin,
        pipelined_rendering::PipelinedRenderingPlugin,
        render_resource::{Extent3d, TextureFormat},
        view::screenshot::{Screenshot, ScreenshotCaptured, save_to_disk},
    },
    scene::ScenePlugin,
    state::app::StatesPlugin,
    tasks::tick_global_task_pools_on_main_thread,
    time::TimePlugin,
    window::ExitCondition,
};
use bevy_obj::ObjPlugin;
use bevy_stl::StlPlugin;
use pyo3::{panic::PanicException, prelude::*};
use std::path::{Path, PathBuf};

// determines if files should be saved or only returned from the function call
// useful for debugging
const SAVE: bool = false;

#[pymodule]
#[pyo3(name = "tag_render")]
// the main module that is exported to python
mod tag_render {
    #[pymodule_export]
    use super::ImagePixels;
    #[pymodule_export]
    use super::ModelRender;
}

#[pyclass(unsendable)]
// the main struct holding the app that does the rendering
pub struct ModelRender {
    app: App,
}
#[allow(unused)]
#[pyclass]
#[derive(Debug, PartialEq, Eq, Clone)]
// the struct returned from the image function containing the pixel data
pub struct ImagePixels {
    #[pyo3(get)]
    pub data: Vec<u8>,
}

#[pymethods]
impl ModelRender {
    #[new]
    // creates a new ModelRender with an app that is initialised
    pub fn new() -> std::result::Result<Self, AppError> {
        let mut app = App::new();
        app.add_plugins((
            PanicHandlerPlugin,
            LogPlugin::default(),
            TaskPoolPlugin::default(),
            FrameCountPlugin,
            TimePlugin,
            TransformPlugin,
            DiagnosticsPlugin,
            ScheduleRunnerPlugin::default(),
            // required to prevent everything else from breaking
            WindowPlugin {
                primary_window: None,
                exit_condition: ExitCondition::DontExit,
                close_when_requested: false,
                ..Default::default()
            },
            TerminalCtrlCHandlerPlugin,
        ))
        .add_plugins((
            AssetPlugin {
                // required to allow files from outside the assets folder to be loaded
                unapproved_path_mode: UnapprovedPathMode::Allow,
                ..Default::default()
            },
            ScenePlugin,
            RenderPlugin::default(),
            ImagePlugin::default(),
            MeshPlugin,
            CameraPlugin,
            LightPlugin,
            PipelinedRenderingPlugin,
            CorePipelinePlugin,
            PostProcessPlugin,
            AntiAliasPlugin,
        ))
        .add_plugins((
            PbrPlugin::default(),
            GltfPlugin::default(),
            StatesPlugin,
            StlPlugin,
            ObjPlugin,
        ))
        .init_state::<AppState>()
        .init_resource::<Waiting>()
        .add_systems(PostStartup, log_state)
        .add_systems(PostUpdate, log_state)
        .add_systems(Startup, setup)
        .add_systems(Update, update)
        .add_systems(Update, loading.run_if(in_state(AppState::ImageLoading)));
        let plugins_state = app.plugins_state();
        if plugins_state != PluginsState::Cleaned {
            while app.plugins_state() == PluginsState::Adding {
                tick_global_task_pools_on_main_thread();
            }
            app.finish();
            app.cleanup();
        }
        while app.world().resource::<State<AppState>>().get() != &AppState::Waiting {
            app.update();
        }
        Ok(ModelRender { app })
    }

    // returns the pixel data or an error (exception in python) for the given model and size
    pub fn image(
        &mut self,
        path: String,
        dimensions: (u32, u32),
    ) -> std::result::Result<ImagePixels, AppError> {
        let Ok(path) = Path::new(&path).canonicalize() else {
            return Err(AppError::PathError);
        };
        if !path.extension().is_some_and(|ext| {
            SUPPORTED.contains(&ext.to_string_lossy().to_string().to_lowercase().trim())
        }) {
            return Err(AppError::NotSupported);
        }
        self.app.insert_resource(ImageWaiting(path, dimensions));
        while !self.app.world().contains_resource::<ImageDone>() {
            self.app.update();
        }
        let done = self.app.world_mut().remove_resource::<ImageDone>().unwrap();
        self.app.update();
        Ok(done.0)
    }
}
impl From<Image> for ImagePixels {
    fn from(image: Image) -> Self {
        Self {
            data: image.data.unwrap(),
        }
    }
}
#[derive(Debug, Clone)]
// the errors or exceptions that the image function returns
pub enum AppError {
    PathError,
    NotSupported,
}
impl ToString for AppError {
    fn to_string(&self) -> String {
        match self {
            AppError::PathError => "error processing given path".to_string(),
            AppError::NotSupported => "file format not supported".to_string(),
        }
    }
}
impl From<AppError> for PyErr {
    fn from(value: AppError) -> Self {
        Self::new::<PanicException, _>(value.to_string())
    }
}

// handles the loading of the image once the app is initialised
fn loading(
    asset_server: Res<AssetServer>,
    handle: Res<ImageHandle>,
    mut app_state: ResMut<NextState<AppState>>,
    mut cam: Query<&mut Camera, With<MainCamera>>,
) {
    if asset_server.is_loaded(handle.0.id()) {
        cam.single_mut().unwrap().target = handle.0.clone().into();
        app_state.set(AppState::Waiting);
    }
}
// sets up the app
fn setup(
    mut commands: Commands,
    asset_server: Res<AssetServer>,
    mut app_state_set: ResMut<NextState<AppState>>,
    mut materials: ResMut<Assets<StandardMaterial>>,
) {
    commands.insert_resource(Mat(materials.add(StandardMaterial::from_color(WHITE))));
    let image = Image::new_target_texture(512, 512, TextureFormat::Rgba8UnormSrgb);
    let image_handle = asset_server.add(image);
    commands.spawn((Camera3d::default(), MainCamera, Transform::default()));
    commands.insert_resource(ImageHandle(image_handle));
    commands.insert_resource(AmbientLight {
        brightness: 250.,
        ..Default::default()
    });
    commands.spawn((
        PointLight {
            intensity: 1000000.,
            ..Default::default()
        },
        Transform::default(),
        Light,
    ));
    commands.insert_resource(ClearColor(BLACK.into()));
    app_state_set.set(AppState::ImageLoading);
}
// queries for the current state and either positions the model or captures an image
fn update(
    mut camera: Query<(&mut Transform, &Camera), (With<MainCamera>, Without<Light>)>,
    mut model_aabb: Query<
        (&Aabb, &mut Transform),
        (With<Model>, Without<MainCamera>, Without<Light>),
    >,
    model_ent: Query<(&Mesh3d, Entity), With<Model>>,
    mut light: Query<&mut Transform, (With<Light>, Without<MainCamera>)>,
    mut commands: Commands,
    done: If<Res<ImageWaiting>>,
    app_state: Res<State<AppState>>,
    mut app_state_set: ResMut<NextState<AppState>>,
    asset_server: Res<AssetServer>,
    handles: Res<ImageHandle>,
    mut images: ResMut<Assets<Image>>,
    mat: Res<Mat>,
    mut waiting: ResMut<Waiting>,
) {
    match **app_state {
        AppState::Waiting => {
            *waiting = Waiting::TakeIt;
            let mesh = Mesh3d(asset_server.load(done.0.0.clone()));
            commands.spawn((
                Model,
                mesh,
                MeshMaterial3d(mat.0.clone()),
                Transform::default(),
            ));
            images.get_mut(handles.0.id()).unwrap().resize(Extent3d {
                width: done.1.0,
                height: done.1.1,
                ..Default::default()
            });
            app_state_set.set(AppState::MeshLoading);
        }
        AppState::MeshLoading => {
            let (mesh, _) = model_ent.single().unwrap();
            if asset_server.is_loaded(mesh.0.id()) && asset_server.is_loaded(handles.0.id()) {
                app_state_set.set(AppState::ToPlace);
            }
        }
        AppState::ToPlace => {
            let (aabb, mut trans_model) = model_aabb.single_mut().unwrap();
            let half = aabb.half_extents;
            let up = if half.x < half.y && half.z < half.y {
                Dir3::X
            } else if half.z < half.y && half.z < half.x {
                Dir3::Z
            } else {
                Dir3::Y
            };
            trans_model.rotation =
                Quat::from_rotation_arc(trans_model.up().as_vec3(), up.as_vec3());
            let (mut trans_camera, _) = camera.single_mut().unwrap();
            trans_camera.translation = aabb.half_extents.map(|a| a * 3.).into();
            trans_camera.look_at(aabb.center.into(), Vec3::Y);
            light.single_mut().unwrap().translation = aabb.half_extents.map(|a| a * 2.1).into();
            app_state_set.set(AppState::Placed);
        }
        AppState::Placed => match *waiting {
            Waiting::TakeIt => {
                *waiting = Waiting::Wait(1);
                return;
            }
            Waiting::Wait(a) => {
                if a < 10 {
                    *waiting = Waiting::Wait(a + 1);
                    return;
                }
                commands
                    .spawn(Screenshot(camera.single().unwrap().1.target.clone()))
                    .observe(on_capture);
                *waiting = Waiting::IsOk;
            }
            Waiting::IsOk => {}
        },
        _ => {}
    }
}
// called when the image is captured
fn on_capture(
    on: On<ScreenshotCaptured>,
    mut commands: Commands,
    mut waiting: ResMut<Waiting>,
    model: Query<Entity, With<Model>>,
    mut app_state_set: ResMut<NextState<AppState>>,
    image_waiting: Res<ImageWaiting>,
) {
    if !on
        .image
        .data
        .as_ref()
        .unwrap()
        .iter()
        .any(|a| *a != 255 && *a != 0)
    {
        *waiting = Waiting::TakeIt;
        return;
    }
    let image = on.image.clone();
    if SAVE {
        let name = format!(
            "out_{}.png",
            image_waiting
                .0
                .file_name()
                .map(|name| name.to_string_lossy().to_string())
                .unwrap_or_else(|| "None".to_string())
        );
        save_to_disk(name.as_str())(on);
    }
    commands.remove_resource::<ImageWaiting>();
    commands.entity(model.single().unwrap()).despawn();
    commands.insert_resource(ImageDone(image.into()));
    app_state_set.set(AppState::Waiting);
    info!("captured & `ImageDone` created");
}
// for debugging
fn log_state(app_state: Res<State<AppState>>) {
    if !app_state.is_changed() {
        return;
    }
    info!("app in state: {:?}", app_state.get())
}
#[derive(Component)]
// the main camera
struct MainCamera;
#[derive(Component)]
// the model being rendered
struct Model;
#[derive(Component)]
// the main lighting
struct Light;
#[derive(States, Debug, Clone, Copy, PartialEq, Eq, Hash, Default)]
// the state of positioning the model
enum AppState {
    #[default]
    Started,
    ImageLoading,
    Waiting,
    MeshLoading,
    ToPlace,
    Placed,
}
#[derive(Resource)]
// the image that serves as the target of the camera
struct ImageHandle(Handle<Image>);
#[derive(Resource)]
// the finished image, when this exists the image function returns it
struct ImageDone(ImagePixels);
#[derive(Resource)]
// represents the path and dimensions of an image waiting to be rendered
struct ImageWaiting(PathBuf, (u32, u32));
// the supported file extensions, more can be added
const SUPPORTED: &[&'static str] = &["stl", "obj"];
#[derive(Resource)]
// the material used for all models, this can be changed
struct Mat(Handle<StandardMaterial>);
#[derive(Resource, Default, Clone, Copy, PartialEq, Eq, Debug)]
// the state of capturing the image
enum Waiting {
    #[default]
    TakeIt,
    Wait(usize),
    IsOk,
}
#[cfg(test)]
mod test {
    use crate::ModelRender;
    use std::path::Path;

    #[test]
    // test if multiple files can be rendered sequentially
    fn images() {
        let mut model_render = ModelRender::new().unwrap();
        let folder = Path::new("trial").to_path_buf();
        // enter models to be tested here
        ["cube.stl", "cube.obj"].into_iter().for_each(|name: &str| {
            model_render
                .image(folder.join(name).to_string_lossy().to_string(), (500, 500))
                .unwrap();
        });
    }
}
