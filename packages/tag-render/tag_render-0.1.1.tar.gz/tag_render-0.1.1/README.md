# tag_render

A renderer of .stl and .obj files for Tag Studio written in bevy in rust and pyo3 for interop.

The exported functions include new that creates a ModelRender for rendering, and an image which renders an image when given the path and dimensions.

The bindings can be created using [maturin](https://github.com/PyO3/maturin). A .whl is already built for linux.
