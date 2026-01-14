use super::{
    Element, Expr, FreeVariableIter, FreeVariables, Metadata, MetadataIm, MetadataMut,
    VarSwapMapping, WellDefinedCondition, default_vocab_swap, vocabs_ptr_eq,
};
use crate::fodot::display_as_debug;
use crate::fodot::error::{
    ApplyError, MismatchedArity, TypeMismatch, VocabMismatchError, VocabSupersetError,
};
use crate::fodot::fmt::FodotOptions;
use crate::fodot::structure::TypeInterp;
use crate::fodot::vocabulary::{CustomType, VocabSwap, VocabSwapper};
use crate::fodot::{
    fmt::{Fmt, FodotDisplay, FormatOptions},
    vocabulary::{ExtendedDomain, SymbolRc, TypeRef, Vocabulary},
};
use itertools::Itertools;
use sli_collections::rc::{Rc, RcA};
use std::fmt::{Display, Write};

/// An applied symbol.
#[derive(Clone)]
pub struct AppliedSymbol {
    symb: SymbolRc,
    args: Box<[Expr]>,
    metadata: Option<Box<Metadata>>,
}

impl PartialEq for AppliedSymbol {
    fn eq(&self, other: &Self) -> bool {
        self.symb == other.symb && self.args == other.args
    }
}

impl Eq for AppliedSymbol {}

impl FodotOptions for AppliedSymbol {
    type Options<'a>
        = FormatOptions
    where
        Self: 'a;
}

impl FodotDisplay for AppliedSymbol {
    fn fmt(
        fmt: Fmt<&Self, Self::Options<'_>>,
        f: &mut std::fmt::Formatter<'_>,
    ) -> std::fmt::Result {
        write!(
            f,
            "{}",
            fmt.with_format_opts(&fmt.value.symb).with_name_only()
        )?;
        if fmt.value.symb.is_constructor() && fmt.value.symb.domain().arity() == 0 {
            return Ok(());
        }
        f.write_char('(')?;
        write!(
            f,
            "{}",
            fmt.value
                .args
                .iter()
                .map(|f| fmt.with_format_opts(f))
                .format(", ")
        )?;
        f.write_char(')')?;
        Ok(())
    }
}

impl Display for AppliedSymbol {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", Fmt::with_defaults(self))
    }
}

display_as_debug!(AppliedSymbol);

impl AppliedSymbol {
    /// Returns the corresponding [Vocabulary] as `&RcA<Vocabulary>`.
    pub fn vocab_rc(&self) -> Option<&RcA<Vocabulary>> {
        self.symb.vocab_rc()
    }

    /// Returns the applied symbol.
    pub fn symbol(&self) -> &SymbolRc {
        &self.symb
    }

    /// Returns the arguments the were applied to the symbol.
    pub fn args(&self) -> &[Expr] {
        &self.args
    }

    /// Returns the codomain of this expression.
    pub fn codomain(&self) -> TypeRef<'_> {
        self.symb.codomain()
    }

    pub fn collect_wdcs(&self) -> Vec<WellDefinedCondition<'_>> {
        self.args.iter().flat_map(|f| f.collect_wdcs()).collect()
    }

    pub(crate) fn _vocab_swap(&mut self, vocab: &Rc<Vocabulary>, swapping: &mut VarSwapMapping) {
        self.symb._vocab_swap(vocab.clone());
        for arg in self.args.iter_mut() {
            arg._vocab_swap(vocab, swapping);
        }
    }
}

impl VocabSwap for AppliedSymbol {
    fn swap_vocab(&mut self, vocabulary: Rc<Vocabulary>) -> Result<(), VocabSupersetError> {
        if let Some(vocab) = self.vocab_rc() {
            default_vocab_swap(self, vocab.clone().into(), vocabulary)
        } else {
            Ok(())
        }
    }

    fn vocab_swapper(
        &mut self,
        vocabulary_swapper: VocabSwapper,
    ) -> Result<(), VocabMismatchError> {
        if let Some(vocab) = self.vocab_rc() {
            if !vocab.exact_eq(vocabulary_swapper.get_old()) {
                return Err(VocabMismatchError);
            }
            self._vocab_swap(vocabulary_swapper.get_new_rc(), &mut Default::default());
        }
        Ok(())
    }
}

impl FreeVariables for AppliedSymbol {
    fn add_to_free_variable_iter<'a>(&'a self, iter: &mut FreeVariableIter<'a>) {
        for arg in self.args() {
            iter.add_expr(arg.into());
        }
    }
}

impl MetadataIm for AppliedSymbol {
    type Metadata = Metadata;
    fn metadata(&self) -> Option<&Metadata> {
        self.metadata.as_deref()
    }
}

impl MetadataMut for AppliedSymbol {
    fn metadata_mut(&mut self) -> &mut Metadata {
        self.metadata.get_or_insert_default()
    }
}

impl SymbolRc {
    /// Try to apply this symbol with the given arguments
    pub fn try_apply<I: Into<Box<[Expr]>>>(self, args: I) -> Result<AppliedSymbol, ApplyError> {
        self._try_apply(args.into())
    }

    fn _try_apply(self, args: Box<[Expr]>) -> Result<AppliedSymbol, ApplyError> {
        if !args.iter().all(|f| vocabs_ptr_eq(f.vocab(), self.vocab())) {
            return Err(VocabMismatchError.into());
        }
        match self.domain() {
            ExtendedDomain::UnaryUniverse if args.len() != 1 => {
                return Err(MismatchedArity {
                    expected: 1,
                    found: args.len(),
                }
                .into());
            }
            ExtendedDomain::UnaryUniverse => {}
            ExtendedDomain::Domain(domain) if args.len() != domain.arity() => {
                return Err(MismatchedArity {
                    expected: domain.arity(),
                    found: args.len(),
                }
                .into());
            }
            ExtendedDomain::Domain(domain) => {
                for (codomain1, expr) in domain.iter().zip(args.iter()) {
                    let expr_codomain = expr.codomain();
                    let ok_codomain = codomain1 == expr_codomain ||
                    // Makes sure that arguments of sub type of something
                    // allow arguments of any thing in that sub type
                    self.vocab()
                        .and_then(|f| Element::try_from(expr).ok().map(|el| (f, el)))
                        .and_then(|(f, el)| {
                            CustomType::try_from(codomain1)
                                .ok()
                                .and_then(|custom_codomain| {
                                    f.get_interp(custom_codomain)
                                        .expect("same vocab")
                                        .map(|f| (f, el))
                                })
                        })
                        .map(|(interp, el)| match (interp, el) {
                            (TypeInterp::Int(int_interp), Element::Int(value)) => {
                                int_interp.contains(value)
                            }
                            (TypeInterp::Real(real_interp), Element::Real(value)) => {
                                real_interp.contains(value)
                            }
                            _ => false,
                        })
                        .unwrap_or(false);
                    if !ok_codomain {
                        return Err(TypeMismatch {
                            found: expr_codomain.into(),
                            expected: codomain1.into(),
                        }
                        .into());
                    }
                }
            }
        }
        Ok(AppliedSymbol {
            symb: self,
            args,
            metadata: Default::default(),
        })
    }
}
