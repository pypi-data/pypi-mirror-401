use pyo3::prelude::*;

pub mod set;

pub fn submodule(py: Python) -> PyResult<Bound<'_, PyModule>> {
    let m = PyModule::new(py, "collections")?;
    m.gil_used(false)?;
    let set = set::submodule(py)?;
    m.add_submodule(&set)?;
    m.py()
        .import("sys")?
        .getattr("modules")?
        .set_item("sli_lib._fodot.collections.set", &set)?;
    Ok(m)
}
