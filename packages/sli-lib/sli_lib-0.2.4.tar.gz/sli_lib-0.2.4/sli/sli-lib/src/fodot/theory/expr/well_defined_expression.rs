use super::{Expr, ExprRef, VarSwapMapping, default_vocab_swap};
use crate::fodot::display_as_debug;
use crate::fodot::error::{
    NotWellDefinedCause, NotWellDefinedExpression, NotWellDefinedExpressionError,
    VocabMismatchError, VocabSupersetError,
};
use crate::fodot::fmt::FodotOptions;
use crate::fodot::fmt::{Fmt, FodotDisplay};
use crate::fodot::vocabulary::{VocabSwap, VocabSwapper, Vocabulary};
use sli_collections::rc::{Rc, RcA};
use std::fmt::{Debug, Display};

/// Condition for an expression to be well defined.
#[derive(Debug, Clone)]
pub struct WellDefinedCondition<'a> {
    pub(super) condition: Expr,
    pub(super) origin: ExprRef<'a>,
}

impl<'a> WellDefinedCondition<'a> {
    pub fn condition(&self) -> &Expr {
        &self.condition
    }

    pub fn origin(&self) -> ExprRef<'a> {
        self.origin
    }
}

/// An [Expr] that is well defined.
///
/// An expression is well defined if it has no well defined conditions.
#[derive(Clone, PartialEq, Eq)]
pub struct WellDefinedExpr(Expr);

impl FodotOptions for WellDefinedExpr {
    type Options<'a>
        = <Expr as FodotOptions>::Options<'a>
    where
        Self: 'a;
}

impl FodotDisplay for WellDefinedExpr {
    fn fmt(
        fmt: Fmt<&Self, Self::Options<'_>>,
        f: &mut std::fmt::Formatter<'_>,
    ) -> std::fmt::Result {
        write!(f, "{}", fmt.with_opts(&fmt.value.0))
    }
}

impl Display for WellDefinedExpr {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.display())
    }
}

display_as_debug!(WellDefinedExpr);

impl WellDefinedExpr {
    pub fn expr(self) -> Expr {
        self.0
    }

    pub fn as_expr(&self) -> &Expr {
        &self.0
    }

    pub fn vocab(&self) -> Option<&Vocabulary> {
        self.0.vocab()
    }

    pub fn vocab_rc(&self) -> Option<&RcA<Vocabulary>> {
        self.0.vocab_rc()
    }

    pub(crate) fn _vocab_swap(&mut self, vocab: &Rc<Vocabulary>, swapping: &mut VarSwapMapping) {
        self.0._vocab_swap(vocab, swapping);
    }
}

impl VocabSwap for WellDefinedExpr {
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

impl AsRef<Expr> for WellDefinedExpr {
    fn as_ref(&self) -> &Expr {
        &self.0
    }
}

impl TryFrom<Expr> for WellDefinedExpr {
    type Error = NotWellDefinedExpressionError;

    fn try_from(value: Expr) -> Result<Self, Self::Error> {
        let wdcs = value.collect_wdcs();
        if !wdcs.is_empty() {
            Err(NotWellDefinedExpression {
                causes: wdcs
                    .into_iter()
                    .map(|f| NotWellDefinedCause {
                        condition: f.condition,
                        origin: f.origin.to_owned(),
                    })
                    .collect(),
            }
            .into())
        } else {
            Ok(Self(value))
        }
    }
}

impl<'a> From<&'a WellDefinedExpr> for ExprRef<'a> {
    fn from(value: &'a WellDefinedExpr) -> Self {
        ExprRef::from(&value.0)
    }
}
