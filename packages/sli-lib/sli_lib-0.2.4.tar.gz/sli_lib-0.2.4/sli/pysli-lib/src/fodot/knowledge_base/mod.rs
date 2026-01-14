use std::{ops::Deref, ptr::NonNull, sync::Mutex};

use pyo3::{
    IntoPyObjectExt,
    exceptions::{PyKeyError, PyValueError},
    prelude::*,
    sync::MutexExt,
    types::{PyString, PyTuple},
};
use sli_collections::rc::Rc;
use sli_lib::fodot::knowledge_base::{self, procedure};

use crate::interior_mut::InnerMut;

use super::{structure::Structure, theory::Theory, vocabulary::Vocabulary};

#[pyclass(frozen)]
pub struct _KnowledgeBase(knowledge_base::KnowledgeBase);

#[pymethods]
impl _KnowledgeBase {
    #[staticmethod]
    fn from_str(knowledge_base: &str) -> PyResult<Self> {
        knowledge_base::KnowledgeBase::new(knowledge_base, Default::default())
            .map(Self)
            .map_err(|f| PyValueError::new_err(format!("{}", f.with_source(&knowledge_base))))
    }

    fn __getitem__(
        slf: Bound<'_, Self>,
        name: Bound<'_, PyAny>,
        py: Python<'_>,
    ) -> PyResult<Py<PyAny>> {
        let name_str = name.cast::<PyString>()?;
        let Some(block) = slf.get().0.get(&name_str.to_cow()?) else {
            return Err(PyKeyError::new_err(name.unbind()));
        };
        match block {
            knowledge_base::Block::Vocabulary { vocab, .. } => {
                Vocabulary::construct(vocab.clone()).into_py_any(py)
            }
            knowledge_base::Block::Theory { theory, .. } => {
                Theory::construct(theory.clone().into()).into_py_any(py)
            }
            knowledge_base::Block::Structure { structure, .. } => {
                Structure::construct(structure.clone()).into_py_any(py)
            }
            knowledge_base::Block::Procedure { procedure, .. } => {
                Ok(construct_procedure(procedure, slf.as_borrowed()).into())
            }
        }
    }

    fn __repr__(&self) -> String {
        format!("KnowledgeBase.from_str(\n\"\"\"\n{}\"\"\")", self.0)
    }

    fn __len__(&self) -> usize {
        self.0.len()
    }

    fn __iter__(slf: Bound<'_, Self>) -> _KnowledgeBaseIter {
        let iter: Box<dyn Iterator<Item = _> + Send + Sync> = Box::new(slf.get().0.iter());
        // we unsure this Box<_> lives for as long as slf, as such the lifetimes are respected
        let iter = unsafe {
            core::mem::transmute::<
                Box<dyn Iterator<Item = (&str, &knowledge_base::Block)> + Send + Sync + '_>,
                Box<
                    dyn Iterator<Item = (&'static str, &'static knowledge_base::Block)>
                        + Send
                        + Sync
                        + 'static,
                >,
            >(iter)
        };
        unsafe { _KnowledgeBaseIter::new_extended(iter, slf.unbind()) }
    }

    fn __str__(&self) -> String {
        format!("{}", self.0)
    }
}

#[pyclass(frozen)]
pub struct _KnowledgeBaseIter {
    inner: Mutex<
        NonNull<
            dyn Iterator<Item = (&'static str, &'static knowledge_base::Block)>
                + Sync
                + Send
                + 'static,
        >,
    >,
    // Field required so we don't drop Model when iterating.
    #[allow(unused)]
    kb: Py<_KnowledgeBase>,
}

impl _KnowledgeBaseIter {
    unsafe fn new_extended<'a>(
        inner: Box<
            dyn Iterator<Item = (&'static str, &'static knowledge_base::Block)> + Sync + Send + 'a,
        >,
        kb: Py<_KnowledgeBase>,
    ) -> Self {
        #[allow(clippy::unnecessary_cast)]
        Self {
            inner: Mutex::new(
                NonNull::new(unsafe {
                    core::mem::transmute::<
                        *mut (
                            dyn Iterator<Item = (&'static str, &'static knowledge_base::Block)>
                                + Sync
                                + Send
                                + 'a
                        ),
                        *mut (
                            dyn Iterator<Item = (&'static str, &'static knowledge_base::Block)>
                                + Sync
                                + Send
                                + 'static
                        ),
                    >(Box::into_raw(inner))
                })
                .unwrap(),
            ),
            kb,
        }
    }
}

// Safety:
// This is safe since all fields are Sync and Send, and KnowledgeBase is immutable.
unsafe impl Sync for _KnowledgeBaseIter {}
// Safety:
// This is safe since all fields are Sync and Send, and KnowledgeBase is immutable.
unsafe impl Send for _KnowledgeBaseIter {}

#[pymethods]
impl _KnowledgeBaseIter {
    fn __iter__(slf: Bound<'_, Self>) -> Bound<'_, Self> {
        slf
    }

    fn __next__(slf: Bound<'_, Self>, py: Python<'_>) -> PyResult<Option<Py<PyTuple>>> {
        // SAFETY:
        // this pointer was created from Box::into_raw and we never share it
        unsafe { slf.get().inner.lock_py_attached(slf.py()).unwrap().as_mut() }
            .next()
            .map(|(name, block)| {
                let block = match block {
                    knowledge_base::Block::Vocabulary { vocab, .. } => {
                        Vocabulary::construct(vocab.clone()).into_py_any(py)
                    }
                    knowledge_base::Block::Theory { theory, .. } => {
                        Theory::construct(theory.clone().into()).into_py_any(py)
                    }
                    knowledge_base::Block::Structure { structure, .. } => {
                        Structure::construct(structure.clone()).into_py_any(py)
                    }
                    knowledge_base::Block::Procedure { procedure, .. } => Ok(construct_procedure(
                        procedure,
                        slf.get().kb.bind(slf.py()).into(),
                    )
                    .into()),
                }?;
                (name.to_string(), block)
                    .into_pyobject(py)
                    .map(|f| f.unbind())
            })
            .transpose()
    }
}

pub fn construct_procedure<'a>(
    procedure: &procedure::Procedure,
    kb: Borrowed<'_, 'a, _KnowledgeBase>,
) -> Bound<'a, PyAny> {
    let py_procedure = py_procedure_ty(kb.py());
    py_procedure
        .call1((
            py_procedure_lang_python(kb.py()),
            procedure.name.deref(),
            procedure.args.iter().map(|f| f.deref()).collect::<Vec<_>>(),
            procedure.content.deref(),
            kb.py().None(),
        ))
        .unwrap()
}

pub fn py_procedure_ty(py: Python<'_>) -> Bound<'_, PyAny> {
    py.import("sli_lib.fodot.knowledge_base")
        .unwrap()
        .getattr("Procedure")
        .unwrap()
}

pub fn py_procedure_lang_python(py: Python<'_>) -> Bound<'_, PyAny> {
    py.import("sli_lib.fodot.knowledge_base")
        .unwrap()
        .getattr("ProcedureLang")
        .unwrap()
        .getattr("PYTHON")
        .unwrap()
}

impl Drop for _KnowledgeBaseIter {
    fn drop(&mut self) {
        // Even if we poisoned the lock we allocation is still ok and should be cleaned up,
        // See https://doc.rust-lang.org/nomicon/poisoning.html
        let ptr = self
            .inner
            .get_mut()
            .unwrap_or_else(|e| e.into_inner())
            .as_ptr();
        // Safety:
        // The pointer was created from a into_raw call
        drop(unsafe { Box::from_raw(ptr) })
    }
}

#[pyclass(frozen)]
/// A special form of `KnowledgeBase`, with one `sli_lib.fodot.theory.Theory` and one
/// `sli_lib.fodot.structure.Structure`.
pub struct Inferenceable(pub(crate) knowledge_base::Inferenceable);

impl Inferenceable {
    pub(crate) fn construct(inferenceable: knowledge_base::Inferenceable) -> Self {
        Self(inferenceable)
    }
}

impl AsRef<knowledge_base::Inferenceable> for Inferenceable {
    fn as_ref(&self) -> &knowledge_base::Inferenceable {
        &self.0
    }
}

#[pymethods]
impl Inferenceable {
    #[new]
    fn new(theory: Bound<'_, Theory>, structure: Bound<'_, Structure>) -> PyResult<Self> {
        let structure = structure
            .get()
            .0
            .get_py(theory.py())
            .clone()
            .try_into_partial()
            .map_err(|f| f.type_interps().missing_type_error())
            .map_err(|f| PyValueError::new_err(format!("{}", f)))?;
        Ok(Self::construct(
            knowledge_base::Inferenceable::new(
                theory.get().0.get_py(theory.py()).clone(),
                structure,
            )
            .map_err(|f| PyValueError::new_err(format!("{}", f)))?,
        ))
    }

    /// Creates a `Inferenceable` from an FO(·) specification containing one vocabulary block, one theory
    /// block and one structure block.
    #[staticmethod]
    fn from_specification(value: &str) -> PyResult<Self> {
        knowledge_base::Inferenceable::from_specification(value)
            .map(Inferenceable::construct)
            .map_err(|f| pyo3::exceptions::PyValueError::new_err(format!("{}", f)))
    }

    #[staticmethod]
    #[pyo3(signature = (*blocks))]
    fn from_blocks(blocks: Bound<'_, PyAny>) -> PyResult<Self> {
        let mut vocabularies = Vec::new();
        let mut theories = Vec::new();
        let mut structures = Vec::new();
        for block in blocks.try_iter()? {
            let block = block?;
            if let Ok(vocab) = block.cast::<Vocabulary>() {
                vocabularies.push(vocab.get().0.get_py(blocks.py()).clone());
            } else if let Ok(assertion) = block.cast::<Theory>() {
                theories.push(Rc::as_ref(&assertion.get().0.get_py(blocks.py())).clone());
            } else if let Ok(structure) = block.cast::<Structure>() {
                structures.push(structure.get().0.get_py(blocks.py()).clone());
            } else {
                return Err(PyValueError::new_err(format!(
                    "expected a tuple of Vocabularies, Theories and, Structures, found '{}'",
                    block.get_type().str()?
                )));
            }
        }
        Ok(Self::construct(
            knowledge_base::Inferenceable::from_blocks(vocabularies, theories, structures)
                .map_err(|f| PyValueError::new_err(format!("{}", f)))?,
        ))
    }

    /// Returns the vocabulary of the inferenceable.
    fn vocab(slf: Bound<'_, Self>) -> Vocabulary {
        Vocabulary(InnerMut::new(slf.get().0.vocab_rc().clone()))
    }

    /// Returns the theory of the inferenceable.
    fn theory(&self) -> Theory {
        Theory::construct(self.0.theory_rc().clone())
    }

    /// Returns the structure of the inferenceable.
    fn structure(slf: Bound<'_, Self>) -> Structure {
        Structure::construct(slf.get().0.structure().clone().into_incomplete())
    }

    fn __str__(&self) -> String {
        format!("{}", &self.0)
    }
}

pub fn submodule(py: Python) -> PyResult<Bound<'_, PyModule>> {
    let m = PyModule::new(py, "knowledge_base")?;
    m.gil_used(false)?;
    m.add_class::<_KnowledgeBase>()?;
    m.add_class::<Inferenceable>()?;
    Ok(m)
}
