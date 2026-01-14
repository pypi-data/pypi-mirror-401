use super::vocabulary::Vocabulary;
use crate::interior_mut::InnerMut;
use pyo3::{exceptions::PyValueError, prelude::*, types::PyString};
use sli_collections::rc::Rc;
use sli_lib::fodot::{theory, vocabulary::VocabSwap};
use std::ops::Deref;

pub use crate::fodot::knowledge_base::Inferenceable;

#[pyclass(frozen)]
/// A set of FO(·) assertions.
pub struct Theory(pub(crate) InnerMut<Rc<theory::Theory>>);

impl Theory {
    pub(crate) fn construct(theory: Rc<theory::Theory>) -> Self {
        Self(InnerMut::new(theory))
    }
}

#[pymethods]
impl Theory {
    #[new]
    fn new(vocabulary: &Bound<'_, Vocabulary>) -> Self {
        let vocab = vocabulary.get().0.get_py(vocabulary.py()).clone();
        Self::construct(theory::Theory::new(vocab).into())
    }

    fn merge(&self, other: &Self, py: Python) -> PyResult<()> {
        // avoid deadlock
        if core::ptr::eq(self, other) {
            return Ok(());
        }

        Rc::make_mut(&mut self.0.get_mut_py(py))
            .merge(other.0.get_py(py).deref().as_ref().clone())
            .map_err(|f| PyValueError::new_err(format!("{}", f)))
    }

    fn swap_vocab(&self, new_vocab: &Vocabulary, py: Python<'_>) -> PyResult<()> {
        Rc::make_mut(&mut self.0.get_mut_py(py))
            .swap_vocab(new_vocab.0.get_py(py).deref().clone())
            .map_err(|f| PyValueError::new_err(format!("{}", f)))
    }

    /// Returns the vocabulary of the theory.
    fn vocab(slf: &Bound<'_, Self>) -> Vocabulary {
        Vocabulary::construct(slf.get().0.get_py(slf.py()).vocab_rc().clone())
    }

    /// Adds the given string form FO(·) theory to this object.
    fn parse(slf: Bound<'_, Self>, decls: Bound<'_, PyString>) -> PyResult<()> {
        let source = decls.to_cow()?;
        let source_str: &str = &source;
        Rc::make_mut(&mut slf.get().0.get_mut_py(slf.py()))
            .parse(source_str)
            .map_err(|f| PyValueError::new_err(format!("{}", f.with_source(&source_str))))?;
        Ok(())
    }

    fn __str__(&self, py: Python) -> String {
        format!("{}", self.0.get_py(py).as_ref())
    }
}

pub fn submodule(py: Python) -> PyResult<Bound<'_, PyModule>> {
    let m = PyModule::new(py, "theory")?;
    m.gil_used(false)?;
    m.add_class::<Theory>()?;
    Ok(m)
}
