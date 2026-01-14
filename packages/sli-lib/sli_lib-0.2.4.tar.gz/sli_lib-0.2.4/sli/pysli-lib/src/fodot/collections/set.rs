use std::ops::Deref;

use pyo3::{
    exceptions::{PyRuntimeError, PyValueError},
    prelude::*,
    types::PyTuple,
};

use crate::{
    fodot::{
        structure::{Structure, args_to_py_tuple, py_tuple_to_args},
        vocabulary::{Domain, Vocabulary},
    },
    interior_mut::{InnerImIter, InnerMut},
};
use sli_collections::rc::Rc;
use sli_lib::fodot::{collections::set, structure::ArgsRef};

/// An FO(·) set over a given domain.
#[pyclass(frozen)]
pub struct Set(InnerMut<set::Set>);

impl AsRef<InnerMut<set::Set>> for Set {
    fn as_ref(&self) -> &InnerMut<set::Set> {
        &self.0
    }
}

impl Set {
    pub(crate) fn construct(set: set::Set) -> Self {
        Set(InnerMut::new(set))
    }
}

#[pymethods]
impl Set {
    #[new]
    fn new(domain: &Domain, structure: &Structure, py: Python<'_>) -> PyResult<Self> {
        let domain_full = domain
            .get_rc(py)
            .with_partial_interps(Rc::clone(structure.0.get_py(py).type_interps_rc()))
            .map_err(|f| PyValueError::new_err(format!("{}", f)))?;
        set::Set::new(domain_full)
            .map(|f| Set(InnerMut::new(f)))
            .map_err(|f| PyValueError::new_err(format!("{}", f)))
    }

    fn vocab(&self, py: Python<'_>) -> Vocabulary {
        Vocabulary::construct(Rc::clone(self.0.get_py(py).type_interps().vocab_rc()))
    }

    fn __len__(&self, py: Python<'_>) -> usize {
        self.0.get_py(py).cardinality()
    }

    fn __contains__(&self, value: Bound<'_, PyAny>, py: Python<'_>) -> PyResult<bool> {
        let set_guard = self.0.get_py(py);
        let Ok(args) = (if let Ok(value) = value.cast::<PyTuple>() {
            py_tuple_to_args(value, set_guard.domain().into())
        } else {
            let singleton_tuple = PyTuple::new(py, [value])?;
            py_tuple_to_args(&singleton_tuple, set_guard.domain().into())
        }) else {
            return Ok(false);
        };
        Ok(set_guard
            .contains_args(args)
            .expect("argument created with the same domain"))
    }

    /// Adds the given tuple to the set.
    ///
    /// Raises an exception if the given tuple is not of the sets domain.
    fn add(&self, args: &Bound<'_, PyTuple>, py: Python<'_>) -> PyResult<()> {
        let mut set_guard = self.0.get_mut_py(py);
        let domain = set_guard.domain().clone();
        let args = py_tuple_to_args(args, (&domain).into())
            .map_err(|f| PyValueError::new_err(format!("{}", f)))?;
        set_guard
            .add_args(args)
            .expect("arguments created from set domain");
        Ok(())
    }

    /// Negates the set in place over its domain.
    ///
    /// The unary operator `~` returns a copy of this set negated over its domain.
    fn negate(&self, py: Python<'_>) {
        self.0.get_mut_py(py).negate();
    }

    fn __invert__(&self, py: Python<'_>) -> Self {
        let mut new_set = set::Set::clone(&self.0.get_py(py));
        new_set.negate();
        Self::construct(new_set)
    }

    fn domain(&self, py: Python<'_>) -> PyResult<Domain> {
        let set_guard = self.0.get_py(py);
        Ok(Domain::construct(
            set_guard.domain().as_domain().to_id(),
            Py::new(py, self.vocab(py))?,
        ))
    }

    /// @public
    fn __iter__(slf: Bound<'_, Self>) -> PyResult<SetIter> {
        let inner = unsafe {
            InnerImIter::try_construct(&slf, |f| {
                let iter = f.iter();
                // Safety:
                // InnerMutIter guarantees a is never used after mutation occurs and may life for as long
                // as slf.structure lives (which is just as long as InnerMutIter lives).
                PyResult::Ok(core::mem::transmute::<set::Iter<'_>, set::Iter<'static>>(
                    iter,
                ))
            })
        }?;
        Ok(SetIter(inner))
    }

    fn __repr__(&self, py: Python<'_>) -> String {
        let set_guard = self.0.get_py(py);
        format!("<Set({})>", set_guard.deref())
    }

    fn __str__(&self, py: Python<'_>) -> String {
        format!("{}", self.0.get_py(py).deref())
    }
}

#[pyclass(frozen)]
pub struct SetIter(InnerImIter<ArgsRef<'static>, Set, set::Set, set::Iter<'static>>);

#[pymethods]
impl SetIter {
    fn __iter__(slf: Bound<'_, Self>) -> Bound<'_, Self> {
        slf
    }

    fn __next__(slf: Bound<'_, Self>) -> PyResult<Option<Py<PyTuple>>> {
        let iter = slf.get().0.aquire_iter(slf.py());
        iter.next()
            .map_err(|_| PyRuntimeError::new_err("underlying Set changed during iteration"))?
            .map(|f| args_to_py_tuple(slf.py(), f).map(|f| f.unbind()))
            .transpose()
    }
}

pub fn submodule(py: Python) -> PyResult<Bound<'_, PyModule>> {
    let m = PyModule::new(py, "set")?;
    m.gil_used(false)?;
    m.add_class::<Set>()?;
    Ok(m)
}
