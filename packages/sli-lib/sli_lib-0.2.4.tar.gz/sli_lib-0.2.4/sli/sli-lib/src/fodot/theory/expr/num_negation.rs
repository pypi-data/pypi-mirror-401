use crate::fodot::error::{
    SubTypeMismatch, SubTypeMismatchError, VocabMismatchError, VocabSupersetError,
};
use crate::fodot::fmt::{Fmt, FodotDisplay, FodotOptions, FodotPrecDisplay, FormatOptions};
use crate::fodot::vocabulary::{RootType, TypeRef, TypeStr, VocabSwap, VocabSwapper, Vocabulary};
use crate::fodot::{MetadataIm, MetadataMut, display_as_debug};
use sli_collections::rc::{Rc, RcA};
use std::fmt::{Display, Write};

use super::{
    Expr, FreeVariables, Metadata, VarSwapMapping, WellDefinedCondition, default_vocab_swap,
};

#[derive(Clone)]
pub struct NumNegation {
    subexpr: Expr,
    metadata: Option<Box<Metadata>>,
}

impl FodotOptions for NumNegation {
    type Options<'a>
        = FormatOptions
    where
        Self: 'a;
}

impl FodotDisplay for NumNegation {
    fn fmt(
        fmt: Fmt<&Self, Self::Options<'_>>,
        f: &mut std::fmt::Formatter<'_>,
    ) -> std::fmt::Result {
        FodotPrecDisplay::fmt_with_prec(fmt, f, 0)
    }
}

impl FodotPrecDisplay for NumNegation {
    fn fmt_with_prec(
        fmt: Fmt<&Self, Self::Options<'_>>,
        f: &mut std::fmt::Formatter<'_>,
        super_prec: u32,
    ) -> std::fmt::Result {
        let this_prec = fmt.value.precedence();
        let needs_bracket = super_prec > this_prec;
        if needs_bracket {
            f.write_char('(')?;
        }
        f.write_char('-')?;
        write!(
            f,
            "{}",
            fmt.with_format_opts(&fmt.value.subexpr)
                .with_prec(this_prec)
        )?;
        if needs_bracket {
            f.write_char(')')?;
        }
        Ok(())
    }
}

impl Display for NumNegation {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        Display::fmt(&Fmt::with_defaults(self), f)
    }
}

display_as_debug!(NumNegation);

impl PartialEq for NumNegation {
    fn eq(&self, other: &Self) -> bool {
        self.subexpr == other.subexpr
    }
}

impl Eq for NumNegation {}

impl NumNegation {
    /// Try to negate the given expression.
    pub fn new(subexpr: Expr) -> Result<Self, SubTypeMismatchError> {
        if subexpr.codomain().into_root_type() != RootType::Real {
            return Err(SubTypeMismatch {
                found: subexpr.codomain().into(),
                expected: TypeStr::Real,
            }
            .into());
        }
        Ok(Self {
            subexpr,
            metadata: Default::default(),
        })
    }

    pub fn precedence(&self) -> u32 {
        80
    }

    pub fn codomain(&self) -> TypeRef<'_> {
        self.subexpr.codomain()
    }

    pub fn vocab_rc(&self) -> Option<&RcA<Vocabulary>> {
        self.subexpr.vocab_rc()
    }

    /// Returns the given sub expression.
    pub fn subexpr(&self) -> &Expr {
        &self.subexpr
    }

    pub fn collect_wdcs(&self) -> Vec<WellDefinedCondition<'_>> {
        self.subexpr.collect_wdcs()
    }

    pub(crate) fn _vocab_swap(&mut self, vocab: &Rc<Vocabulary>, swapping: &mut VarSwapMapping) {
        self.subexpr._vocab_swap(vocab, swapping);
    }
}

impl VocabSwap for NumNegation {
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

impl FreeVariables for NumNegation {
    fn add_to_free_variable_iter<'a>(&'a self, iter: &mut super::FreeVariableIter<'a>) {
        iter.add_expr(self.subexpr().into());
    }
}

impl MetadataIm for NumNegation {
    type Metadata = Metadata;

    fn metadata(&self) -> Option<&Self::Metadata> {
        self.metadata.as_deref()
    }
}

impl MetadataMut for NumNegation {
    fn metadata_mut(&mut self) -> &mut Self::Metadata {
        self.metadata.get_or_insert_default()
    }
}
