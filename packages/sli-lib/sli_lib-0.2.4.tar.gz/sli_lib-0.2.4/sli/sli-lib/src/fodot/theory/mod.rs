//! Theory datatructures and methods.
//!
//! A [Theory] represents an FO(·) Theory.
//!
//! [Inferenceable] is a special form of [KnowledgeBase],
//! with one [Theory] and one [PartialStructure], usable for all inference tasks.

use super::{
    display_as_debug,
    error::{
        VocabMismatchError, VocabSupersetError,
        parse::{Diagnostics, DiagnosticsBuilder, IDPError},
    },
    fmt::{Fmt, FodotDisplay, FodotOptions, FormatOptions},
    lower::translate_theory,
    structure::PartialStructure,
    vocabulary::{SymbolError, VocabSwap, VocabSwapper, Vocabulary, default_vocab_swap},
};
#[cfg(doc)]
use crate::fodot::knowledge_base::KnowledgeBase;
use crate::{
    ast::{self, TheoryAst, tree_sitter::TsParser},
    sli_entrance::parse_theory_decls,
};
use comp_core::constraints::ParsedConstraints;
use sli_collections::{iterator::Iterator as SIterator, rc::Rc};
use std::fmt::Display;

mod expr;
pub use super::knowledge_base::Inferenceable;
pub use expr::*;

/// A list of [Assertion]s.
#[derive(Clone)]
pub struct Theory {
    vocab: Rc<Vocabulary>,
    assertions: Vec<Assertion>,
}

impl PartialEq for Theory {
    fn eq(&self, other: &Self) -> bool {
        Rc::ptr_eq(&self.vocab, &other.vocab) && self.assertions == other.assertions
    }
}

impl Eq for Theory {}

impl FodotOptions for Theory {
    type Options<'a> = FormatOptions;
}

impl FodotDisplay for Theory {
    fn fmt(
        fmt: Fmt<&Self, Self::Options<'_>>,
        f: &mut std::fmt::Formatter<'_>,
    ) -> std::fmt::Result {
        for assertion in fmt.value {
            fmt.write_indent(f)?;
            writeln!(f, "{}.", fmt.with_opts(assertion))?;
        }
        Ok(())
    }
}

impl Display for Theory {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.display())
    }
}

display_as_debug!(Theory);

impl Theory {
    /// Create an empty [Theory].
    pub fn new(vocab: Rc<Vocabulary>) -> Self {
        Self {
            vocab,
            assertions: Default::default(),
        }
    }

    pub fn parse(&mut self, decls: &str) -> Result<&mut Self, Diagnostics> {
        let mut parser = TsParser::new();
        let theory_ast = ast::Parser::parse_theory(&mut parser, decls);
        let mut diagnostics = DiagnosticsBuilder::new();
        for (err, span) in theory_ast.parse_errors() {
            diagnostics.add_error(IDPError::new_with_span(err.into(), span));
        }
        let vocabulary = self.vocab.clone();
        let count_before = self.assertions.len();
        parse_theory_decls(
            &vocabulary,
            self,
            theory_ast.decls(),
            &decls,
            &mut diagnostics,
        );
        if let Ok(diag) = diagnostics.finish() {
            self.assertions.truncate(count_before);
            Err(diag)
        } else {
            Ok(self)
        }
    }

    pub fn vocab(&self) -> &Vocabulary {
        &self.vocab
    }

    pub fn vocab_rc(&self) -> &Rc<Vocabulary> {
        &self.vocab
    }

    /// Add an [Assertion], fails if the [Assertion]'s corresponding [Vocabulary] is different.
    pub fn add_assertion(&mut self, assertion: Assertion) -> Result<(), VocabMismatchError> {
        if !vocabs_ptr_eq(Some(self.vocab.as_ref()), assertion.vocab()) {
            return Err(VocabMismatchError);
        }
        self.assertions.push(assertion);
        Ok(())
    }

    /// Returns an [Iterator] over all [Assertion]s.
    pub fn iter(&self) -> impl SIterator<Item = &Assertion> {
        self.into_iter()
    }

    pub fn merge(&mut self, mut other: Self) -> Result<(), VocabMismatchError> {
        if !self.vocab().exact_eq(other.vocab()) {
            return Err(VocabMismatchError);
        }
        self.assertions.append(&mut other.assertions);
        Ok(())
    }

    pub(crate) fn lower(
        &self,
        structure: &PartialStructure,
    ) -> Result<ParsedConstraints, SymbolError> {
        let mut parsed_constraints =
            ParsedConstraints::new(Rc::clone(structure.type_interps().cc()));
        translate_theory(self, structure, &mut parsed_constraints)?;
        Ok(parsed_constraints)
    }

    pub(crate) fn _vocab_swap(&mut self, vocab: &Rc<Vocabulary>) {
        let mut swapping = Default::default();
        for assert in self.assertions.iter_mut() {
            assert._vocab_swap(vocab, &mut swapping);
            swapping.clear();
        }
        self.vocab = vocab.clone();
    }
}

impl VocabSwap for Theory {
    fn swap_vocab(&mut self, vocabulary: Rc<Vocabulary>) -> Result<(), VocabSupersetError> {
        default_vocab_swap(self, self.vocab_rc().clone(), vocabulary)
    }

    fn vocab_swapper(
        &mut self,
        vocabulary_swapper: VocabSwapper,
    ) -> Result<(), VocabMismatchError> {
        if !self.vocab().exact_eq(vocabulary_swapper.get_old()) {
            return Err(VocabMismatchError);
        }
        self._vocab_swap(vocabulary_swapper.get_new_rc());
        Ok(())
    }
}

impl<'a> IntoIterator for &'a Theory {
    type IntoIter = core::slice::Iter<'a, Assertion>;
    type Item = &'a Assertion;

    fn into_iter(self) -> Self::IntoIter {
        self.assertions.iter()
    }
}

#[cfg(test)]
mod tests {
    use super::Theory;
    use crate::fodot::vocabulary::{BaseType, Vocabulary};

    #[test]
    fn parse_theory() {
        let mut vocab = Vocabulary::new();
        vocab.add_type_decl("D", BaseType::Int).unwrap();
        vocab.parse("type T p: T -> Bool r: T -> D").unwrap();
        let (vocab, _) = vocab.complete_vocab();
        let mut theory = Theory::new(vocab);
        theory
            .parse("!x in T: p(x). ?x in T, y in D: r(x) = y & y > 2.")
            .unwrap();
    }

    #[test]
    fn failed_parse_theory() {
        let mut vocab = Vocabulary::new();
        vocab.add_type_decl("D", BaseType::Int).unwrap();
        vocab.parse("type T p: T -> Bool r: T -> D").unwrap();
        let (vocab, _) = vocab.complete_vocab();
        let mut theory = Theory::new(vocab);
        let prev_theory = theory.clone();
        theory
            .parse("!x in T: p(x). ?x in T, y in D: r(x) = y & y > 2")
            .unwrap_err();
        assert!(prev_theory == theory);
    }

    #[test]
    fn escaped_theory() {
        let mut vocab = Vocabulary::new();
        vocab.add_type_decl("D", BaseType::Int).unwrap();
        vocab.parse("type T p: T -> Bool r: T -> D").unwrap();
        let (vocab, _) = vocab.complete_vocab();
        let mut theory = Theory::new(vocab);
        let decls = "!x in T: p(x). } vocabulary V {";
        let diag = theory.parse(decls).unwrap_err();
        assert!(diag.errors().len() == 1);
        let a = diag.errors().first().unwrap();
        assert_eq!(a.span().unwrap().end, decls.len());
    }
}
