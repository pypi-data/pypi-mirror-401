use pyo3::prelude::*;

pub mod collections;
pub mod knowledge_base;
pub mod structure;
pub mod theory;
pub mod vocabulary;

pub fn submodule(py: Python) -> PyResult<Bound<'_, PyModule>> {
    let m = PyModule::new(py, "_fodot")?;
    m.gil_used(false)?;
    let vocab = vocabulary::submodule(m.py())?;
    m.add_submodule(&vocab)?;
    m.py()
        .import("sys")?
        .getattr("modules")?
        .set_item("sli_lib._fodot.vocabulary", &vocab)?;

    let structure = structure::submodule(m.py())?;
    m.add_submodule(&structure)?;
    m.py()
        .import("sys")?
        .getattr("modules")?
        .set_item("sli_lib._fodot.structure", &structure)?;

    let theory = theory::submodule(m.py())?;
    m.add_submodule(&theory)?;
    m.py()
        .import("sys")?
        .getattr("modules")?
        .set_item("sli_lib._fodot.theory", &theory)?;

    let knowledge_base = knowledge_base::submodule(m.py())?;
    m.add_submodule(&knowledge_base)?;
    m.py()
        .import("sys")?
        .getattr("modules")?
        .set_item("sli_lib._fodot.knowledge_base", &knowledge_base)?;
    let collections = collections::submodule(m.py())?;
    m.add_submodule(&collections)?;
    m.py()
        .import("sys")?
        .getattr("modules")?
        .set_item("sli_lib._fodot.collections", &collections)?;
    Ok(m)
}
