use super::{Vocabulary, convert_or_parse_type_from_python, convert_type};
use pyo3::{
    BoundObject, IntoPyObjectExt,
    exceptions::{PyIndexError, PyNotImplementedError, PyStopIteration, PyTypeError, PyValueError},
    prelude::*,
    types::PyString,
};
use sli_collections::{cell::Cell, rc::Rc};
use sli_lib::fodot::vocabulary::{
    self, ConstructorRef, DomainId, DomainRc, ExtendedDomain, PfuncRc, PfuncRef, SymbolRef,
};

#[pyclass(frozen, subclass)]
/// An FO(·) symbol.
pub struct Symbol;

#[pymethods]
impl Symbol {
    fn name(&self) -> PyResult<()> {
        Err(PyNotImplementedError::new_err(()))
    }

    fn __str__(&self) -> PyResult<()> {
        Err(PyNotImplementedError::new_err(()))
    }
}

#[pyclass(frozen, extends=Symbol, subclass)]
/// A custom FO(·) symbol, this is always linked to a vocabulary.
///
/// A `CustomSymbol` can become invalid if an operation on the underlying vocabulary causes the
/// symbol to no longer exist in this vocabulary.
/// Any operation on a `CustomSymbol` in this state raises `RuntimeError`.
pub struct CustomSymbol {
    pub(crate) symbol: Rc<str>,
    pub(crate) vocab: Py<Vocabulary>,
}

#[pymethods]
impl CustomSymbol {
    /// Returns the name of the symbol.
    pub fn name(&self) -> &str {
        self.symbol.as_ref()
    }

    /// Vocabulary of the given symbol.
    pub fn vocab(slf: &Bound<'_, Self>) -> Py<Vocabulary> {
        slf.get().vocab.clone_ref(slf.py())
    }

    pub fn domain(&self, py: Python<'_>) -> PyResult<Py<PyAny>> {
        let vocab = self.vocab.bind(py);
        let vocab_guard = vocab.get().0.get_py(py);
        match vocab_guard.parse_symbol(&self.symbol).unwrap().domain() {
            ExtendedDomain::UnaryUniverse => Ok(py_unary_universe(py).unbind()),
            ExtendedDomain::Domain(domain) => {
                Domain::construct(domain.to_id(), self.vocab.clone_ref(py)).into_py_any(py)
            }
        }
    }

    pub fn codomain(&self, py: Python<'_>) -> PyResult<Py<PyAny>> {
        let vocab = self.vocab.bind(py);
        let vocab_guard = vocab.get().0.get_py(py);
        convert_type(
            vocab_guard.parse_symbol(&self.symbol).unwrap().codomain(),
            vocab,
        )
    }

    pub fn __str__(&self) -> &str {
        self.symbol.as_ref()
    }
}

#[pyclass(frozen, extends=CustomSymbol)]
pub struct Pfunc;

impl Pfunc {
    pub fn with_ref<R, F: FnOnce(PfuncRef) -> R>(slf: Borrowed<Self>, f: F) -> PyResult<R> {
        Ok(f(slf
            .as_super()
            .get()
            .vocab
            .get()
            .0
            .get_py(slf.py())
            .parse_pfunc(slf.as_super().get().name())
            .unwrap()))
    }

    pub fn as_rc(slf: Borrowed<Self>) -> PyResult<PfuncRc> {
        Ok(vocabulary::Vocabulary::parse_pfunc_rc(
            &slf.as_super().get().vocab.get().0.get_py(slf.py()),
            slf.as_super().get().name(),
        )
        .unwrap())
    }
}

#[pymethods]
impl Pfunc {
    pub fn __str__(slf: &Bound<Self>) -> PyResult<String> {
        Self::with_ref(slf.as_borrowed(), |f| format!("{}", f))
    }

    pub fn __repr__(slf: &Bound<Self>) -> PyResult<String> {
        Self::with_ref(slf.as_borrowed(), |f| {
            Ok(format!(
                "<Pfunc({}, {})>",
                f,
                slf.as_super().get().vocab.bind(slf.py()).repr()?
            ))
        })
        .and_then(|f| f)
    }
}

impl Pfunc {
    pub fn construct(symbol: Rc<str>, vocab: Py<Vocabulary>, py: Python) -> PyResult<Py<Self>> {
        Py::new(
            py,
            PyClassInitializer::from(Symbol)
                .add_subclass(CustomSymbol { symbol, vocab })
                .add_subclass(Pfunc),
        )
    }

    pub(crate) fn from_ref(
        pfunc: PfuncRef,
        vocab: Py<Vocabulary>,
        py: Python,
    ) -> PyResult<Py<Self>> {
        Self::construct(pfunc.name_rc(), vocab, py)
    }
}

#[pyclass(frozen, extends=CustomSymbol)]
pub struct Constructor;

impl Constructor {
    pub fn construct(symbol: Rc<str>, vocab: Py<Vocabulary>, py: Python) -> PyResult<Py<Self>> {
        Py::new(
            py,
            PyClassInitializer::from(Symbol)
                .add_subclass(CustomSymbol { symbol, vocab })
                .add_subclass(Constructor),
        )
    }

    pub(crate) fn from_ref(
        constructor: ConstructorRef,
        vocab: Py<Vocabulary>,
        py: Python,
    ) -> PyResult<Py<Self>> {
        Self::construct(constructor.name_rc(), vocab, py)
    }
}

/// An FO(·) domain.
#[pyclass(frozen, sequence)]
pub struct Domain {
    domain: DomainId,
    vocab: Py<Vocabulary>,
}

impl Domain {
    pub(crate) fn construct(domain: DomainId, vocab: Py<Vocabulary>) -> Self {
        Self { domain, vocab }
    }

    pub(crate) fn get_rc(&self, py: Python<'_>) -> DomainRc {
        self.domain.to_rc(Rc::clone(&self.vocab.get().0.get_py(py)))
    }
}

macro_rules! domain_ref {
    (
        $dom:expr,
        $py:ident,
        $out_dom:ident $(,)?
    ) => {
        let dom = $dom;
        let vocab = dom.vocab.get().0.get_py($py);
        let $out_dom = dom.domain.to_ref(&vocab);
    };
}

#[pymethods]
impl Domain {
    #[new]
    fn new(vocabulary: Bound<'_, Vocabulary>, types: &Bound<'_, PyAny>) -> PyResult<Self> {
        let domain = {
            let mut sli_types = Vec::new();
            let vocab_borrowed = Borrowed::from(&vocabulary);
            for value in types.try_iter()? {
                let value = value?;
                sli_types.push(convert_or_parse_type_from_python(
                    Borrowed::from(&value),
                    vocab_borrowed,
                )?)
            }
            DomainRc::new(
                &sli_types,
                Rc::clone(&vocabulary.get().0.get_py(vocabulary.py())),
            )
            .map_err(|f| PyValueError::new_err(format!("{}", f)))?
            .to_id()
        };
        Ok(Self {
            domain,
            vocab: vocabulary.unbind(),
        })
    }

    pub fn __getitem__(&self, value: usize, py: Python<'_>) -> PyResult<Py<PyAny>> {
        domain_ref!(self, py, domain);
        if value < domain.arity() {
            convert_type(domain.get(value), self.vocab.bind(py))
        } else {
            Err(PyIndexError::new_err("domain index out of range"))
        }
    }

    pub fn __iter__(slf: Py<Self>) -> DomainIter {
        DomainIter {
            domain: slf,
            cur: 0.into(),
        }
    }

    pub fn __len__(&self, py: Python<'_>) -> usize {
        domain_ref!(self, py, domain);
        domain.arity()
    }

    pub fn vocab(&self, py: Python<'_>) -> Py<Vocabulary> {
        self.vocab.clone_ref(py)
    }

    pub fn __str__(&self, py: Python<'_>) -> String {
        domain_ref!(self, py, domain);
        format!("{}", domain)
    }

    pub fn __repr__(slf: &Bound<'_, Self>, py: Python<'_>) -> PyResult<String> {
        let mut start = format!("<Domain({}, (", slf.get().vocab.bind(py).repr()?,);
        let mut values = slf.try_iter()?.peekable();
        while let Some(value) = values.next() {
            let value = value?;
            start += &value.repr()?.to_cow()?;
            if values.peek().is_some() {
                start += ", ";
            }
        }
        start += "))>";
        Ok(start)
    }
}

#[pyclass(frozen, generic)]
pub struct DomainIter {
    domain: Py<Domain>,
    cur: Cell<usize>,
}

#[pymethods]
impl DomainIter {
    pub fn __iter__(slf: Bound<'_, Self>) -> Bound<'_, Self> {
        slf
    }

    pub fn __next__(&self, py: Python<'_>) -> PyResult<Py<PyAny>> {
        domain_ref!(self.domain.get(), py, domain);
        let index = self.cur.get();
        if index < domain.arity() {
            self.cur.set(index + 1);
            convert_type(domain.get(index), self.domain.get().vocab.bind(py))
        } else {
            Err(PyStopIteration::new_err(()))
        }
    }
}

pub(crate) fn py_unary_universe(python: Python<'_>) -> Bound<'_, PyAny> {
    python
        .import("sli_lib.fodot.vocabulary._pure")
        .unwrap()
        .getattr("_unary_universe")
        .unwrap()
        .cast_into_exact()
        .unwrap()
}

pub fn convert_symbol(
    value: SymbolRef,
    vocab: Borrowed<'_, '_, Vocabulary>,
) -> PyResult<Py<PyAny>> {
    match value {
        vocabulary::Symbol::Type(type_ref) => convert_type(type_ref, &vocab),
        vocabulary::Symbol::Pfunc(pfunc) => {
            Pfunc::from_ref(pfunc, Borrowed::unbind(vocab), vocab.py()).map(|f| f.into())
        }
        vocabulary::Symbol::Constructor(constructor) => {
            Constructor::from_ref(constructor, Borrowed::unbind(vocab), vocab.py())
                .map(|f| f.into())
        }
    }
}

pub(crate) fn convert_pfunc_from_python_ref<'a>(
    pfunc: Borrowed<PyAny>,
    vocab: &'a vocabulary::Vocabulary,
) -> PyResult<PfuncRef<'a>> {
    if let Ok(name) = pfunc.cast::<PyString>() {
        vocabulary::Vocabulary::parse_pfunc(vocab, &name.to_cow()?)
            .map_err(|f| PyValueError::new_err(format!("{}", f)))
    } else if let Ok(pfunc) = pfunc.cast::<Pfunc>() {
        if !pfunc
            .as_super()
            .get()
            .vocab
            .get()
            .0
            .get_py(pfunc.py())
            .exact_eq(vocab)
        {
            return Err(PyValueError::new_err(format!(
                "Found symbol {} from {}, expecting a symbol from <Vocabulary at {:p}>",
                pfunc.as_super().get().name(),
                &pfunc.as_super().get().vocab.bind(pfunc.py()).repr()?,
                vocab,
            )));
        }
        Ok(vocab.parse_pfunc(pfunc.as_super().get().name()).unwrap())
    } else {
        Err(PyTypeError::new_err(format!(
            "expected a 'str' or a 'Pfunc', found a '{}'",
            pfunc.get_type().str()?
        )))
    }
}
