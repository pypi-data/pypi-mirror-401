use super::{
    MetadataIm, display_as_debug,
    error::{
        BlockMismatch, BlockMismatches, FromBlocksError, FromBlocksKBError, FromBlocksKBErrorKind,
        InconsistentInterpretation, InconsistentInterpretations, InterpMergeErrorKind,
        ManyRedeclarations, MissingBlock, Redeclaration, VocabMismatchError,
        parse::{Diagnostics, DiagnosticsBuilder, IDPError, LabeledSpan, to_ordinal_numeral},
    },
    fmt::{Fmt, FodotDisplay, FodotOptions, FormatOptions},
    structure::{IncompleteStructure, PartialStructure, TypeInterps},
    theory::{Theory, vocabs_ptr_eq},
    vocabulary::{SymbolError, Vocabulary},
};
use crate::{
    ast::{ParseError, Span, StructureNames, TheoryNames},
    fodot::error::MissingBlocks,
};
use comp_core::constraints::ParsedConstraints;
use indexmap::{IndexMap, IndexSet};
use itertools::Itertools;
use lazy::{KnowledgeBaseConfig, LazyKnowledgeBase, ToDiagnostics};
use procedure::Procedure;
use sli_collections::rc::Rc;
use std::{
    fmt::{Debug, Display},
    hash::Hash,
};

pub mod lazy;
pub mod procedure;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum BlockType {
    Vocabulary,
    Theory,
    Structure,
    Procedure,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum BlockKind {
    Vocabulary,
    Theory,
    Structure,
    LogicalBlock,
    Procedure,
    NonLogicalBlock,
}

impl BlockKind {
    pub(crate) fn sentence(&self) -> &'static str {
        match self {
            Self::Vocabulary => "vocabulary block",
            Self::Theory => "theory block",
            Self::Structure => "structure block",
            Self::Procedure => "procedure block",
            Self::LogicalBlock => "vocabulary, theory or structure block",
            Self::NonLogicalBlock => "procedure block",
        }
    }
}

impl From<BlockType> for BlockKind {
    fn from(value: BlockType) -> Self {
        match value {
            BlockType::Vocabulary => BlockKind::Vocabulary,
            BlockType::Theory => BlockKind::Theory,
            BlockType::Structure => BlockKind::Structure,
            BlockType::Procedure => BlockKind::Procedure,
        }
    }
}

impl Display for BlockType {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::Vocabulary => f.write_str("vocabulary"),
            Self::Theory => f.write_str("theory"),
            Self::Structure => f.write_str("structure"),
            Self::Procedure => f.write_str("procedure"),
        }
    }
}

#[derive(Debug, Clone)]
pub enum Block {
    Vocabulary {
        vocab: Rc<Vocabulary>,
        metadata: VocabBlockMetadata,
    },
    Theory {
        theory: Theory,
        metadata: TheoryBlockMetadata,
    },
    Structure {
        structure: IncompleteStructure,
        metadata: StructureBlockMetadata,
    },
    Procedure {
        procedure: Procedure,
        metadata: ProcedureMetadata,
    },
}

impl Block {
    pub fn expect_vocab(self, msg: &str) -> (Rc<Vocabulary>, VocabBlockMetadata) {
        if let Block::Vocabulary { vocab, metadata } = self {
            (vocab, metadata)
        } else {
            panic!("{}", msg);
        }
    }

    pub fn expect_vocab_ref<'a>(
        &'a self,
        msg: &str,
    ) -> (&'a Rc<Vocabulary>, &'a VocabBlockMetadata) {
        if let Block::Vocabulary { vocab, metadata } = self {
            (vocab, metadata)
        } else {
            panic!("{}", msg);
        }
    }

    pub fn expect_theory(self, msg: &str) -> (Theory, TheoryBlockMetadata) {
        if let Block::Theory { theory, metadata } = self {
            (theory, metadata)
        } else {
            panic!("{}", msg);
        }
    }

    pub fn expect_theory_ref<'a>(&'a self, msg: &str) -> (&'a Theory, &'a TheoryBlockMetadata) {
        if let Block::Theory { theory, metadata } = self {
            (theory, metadata)
        } else {
            panic!("{}", msg);
        }
    }

    pub fn expect_structure(self, msg: &str) -> (IncompleteStructure, StructureBlockMetadata) {
        if let Block::Structure {
            structure,
            metadata,
        } = self
        {
            (structure, metadata)
        } else {
            panic!("{}", msg);
        }
    }

    pub fn expect_structure_ref<'a>(
        &'a self,
        msg: &str,
    ) -> (&'a IncompleteStructure, &'a StructureBlockMetadata) {
        if let Block::Structure {
            structure,
            metadata,
        } = self
        {
            (structure, metadata)
        } else {
            panic!("{}", msg);
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BlockMetadata {
    pub span: Span,
    pub decl_span: Span,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct VocabBlockMetadata {
    pub block: BlockMetadata,
    pub name_span: Option<Span>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct TheoryBlockMetadata {
    pub block: BlockMetadata,
    pub vocab_name: Box<str>,
    pub name_span: Option<TheoryNames>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct StructureBlockMetadata {
    pub block: BlockMetadata,
    pub vocab_name: Box<str>,
    pub name_span: Option<StructureNames>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ProcedureMetadata {
    pub block: BlockMetadata,
    pub name: Span,
    pub args: Box<[Span]>,
}

pub enum BlockName<'a> {
    Vocabulary(&'a str),
    Theory { block: &'a str, vocab: &'a str },
    Structure { block: &'a str, vocab: &'a str },
    Procedure(&'a str),
}

impl<'a> BlockName<'a> {
    pub fn name(&self) -> &'a str {
        match self {
            Self::Vocabulary(name) => name,
            Self::Theory { block, .. } => block,
            Self::Structure { block, .. } => block,
            Self::Procedure(name) => name,
        }
    }
}

#[derive(Debug, Clone)]
pub struct KnowledgeBase {
    blocks: IndexMap<Rc<str>, Block>,
}

impl FodotOptions for KnowledgeBase {
    type Options<'a> = FormatOptions;
}

impl FodotDisplay for KnowledgeBase {
    fn fmt(
        fmt: super::fmt::Fmt<&Self, Self::Options<'_>>,
        f: &mut std::fmt::Formatter<'_>,
    ) -> std::fmt::Result {
        for (name, block) in fmt.value {
            match block {
                Block::Vocabulary { vocab, .. } => {
                    writeln!(f, "vocabulary {} {{", name)?;
                    Display::fmt(&fmt.with_format_opts(vocab.as_ref()).with_indent(), f)?;
                    writeln!(f, "}}")?;
                }
                Block::Theory { theory, metadata } => {
                    writeln!(f, "theory {}: {} {{", name, metadata.vocab_name)?;
                    Display::fmt(&fmt.with_format_opts(theory).with_indent(), f)?;
                    writeln!(f, "}}")?;
                }
                Block::Structure {
                    structure,
                    metadata,
                } => {
                    writeln!(f, "structure {}: {} {{", name, metadata.vocab_name)?;
                    Display::fmt(
                        &fmt.with_format_opts(structure)
                            .map_options(|f| f.with_full())
                            .with_indent(),
                        f,
                    )?;
                    writeln!(f, "}}")?;
                }
                Block::Procedure { procedure, .. } => {
                    writeln!(
                        f,
                        "procedure {}({}) {{",
                        procedure.name,
                        procedure.args.iter().format(", "),
                    )?;
                    write!(f, "{}", procedure.content)?;
                    writeln!(f, "}}")?;
                }
            }
        }
        Ok(())
    }
}

impl Display for KnowledgeBase {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        Display::fmt(&self.display(), f)
    }
}

impl KnowledgeBase {
    pub fn new(source: &str, config: KnowledgeBaseConfig) -> Result<KnowledgeBase, Diagnostics> {
        let (lazy, diag) = LazyKnowledgeBase::new(source, config);
        if let Some(diag) = diag {
            return Err(diag);
        }
        lazy.into_knowledge_base()
    }

    /// Get a reference to the block with the given name, if it exists.
    pub fn get(&self, name: &str) -> Option<&Block> {
        self.blocks.get(name)
    }

    /// Take the block with the given name out of the knowledge base, if it exists.
    pub fn take(&mut self, name: &str) -> Option<Block> {
        self.blocks.shift_remove(name)
    }

    pub fn iter(&self) -> Iter<'_> {
        Iter(self.blocks.iter())
    }

    pub fn len(&self) -> usize {
        self.blocks.len()
    }

    pub fn is_empty(&self) -> bool {
        self.blocks.is_empty()
    }

    pub fn theory_from_blocks<'a, I: IntoIterator<Item = &'a str>>(
        &self,
        blocks: I,
    ) -> Result<Inferenceable, FromBlocksKBError> {
        let blocks = blocks.into_iter().collect();
        self._theory_from_blocks(&blocks)
    }

    pub fn theory_from_blocks_diags<'a, I: IntoIterator<Item = &'a str>>(
        &self,
        blocks: I,
    ) -> Result<Inferenceable, Diagnostics> {
        let blocks = blocks.into_iter().collect();
        let value = self._theory_from_blocks(&blocks);
        match value {
            Ok(value) => Ok(value),
            Err(error) => match error.take_kind() {
                FromBlocksKBErrorKind::MissingBlocks(missing_blocks) => {
                    let mut diag_builder = DiagnosticsBuilder::new();
                    for missing_block in missing_blocks.0 {
                        diag_builder.add_error(IDPError::new(MissingBlock(missing_block).into()));
                    }
                    Err(diag_builder.finish().unwrap())
                }
                FromBlocksKBErrorKind::MissingTypeInterps(missing_type_interps) => {
                    let mut labels = Vec::new();
                    for missing in missing_type_interps.missing.iter() {
                        let Some(decl_span) = blocks
                            .iter()
                            .find_map(|f| {
                                let vocab = match self.get(f).unwrap() {
                                    Block::Vocabulary { vocab, .. } => vocab.as_ref(),
                                    Block::Theory { theory, .. } => theory.vocab(),
                                    Block::Structure { structure, .. } => structure.vocab(),
                                    Block::Procedure { .. } => unreachable!(),
                                };
                                vocab.parse_custom_type(missing).ok()
                            })
                            .unwrap()
                            .metadata()
                            .and_then(|f| f.span)
                        else {
                            continue;
                        };
                        labels.push(LabeledSpan::new(
                            format!("'{}' defined here", missing),
                            decl_span,
                        ));
                    }
                    let mut error = IDPError::new(missing_type_interps.into());
                    error.set_labels(labels);
                    Err(Diagnostics::new(error))
                }
                FromBlocksKBErrorKind::ManyRedeclarations(redecls) => {
                    let mut diag_builder = DiagnosticsBuilder::new();
                    for redecl in redecls.0 {
                        let mut main_span = None;
                        let mut secondary = Vec::new();
                        for (i, symbol_decl) in blocks
                            .iter()
                            .filter_map(|f| {
                                let vocab = match self.get(f).unwrap() {
                                    Block::Vocabulary { vocab, .. } => vocab.as_ref(),
                                    Block::Theory { theory, .. } => theory.vocab(),
                                    Block::Structure { structure, .. } => structure.vocab(),
                                    Block::Procedure { .. } => unreachable!(),
                                };
                                vocab.parse_symbol(&redecl).ok()
                            })
                            .enumerate()
                        {
                            let Some(symbol_decl) = symbol_decl.metadata().and_then(|f| f.span)
                            else {
                                continue;
                            };
                            if main_span.is_none() {
                                main_span = Some(symbol_decl);
                                continue;
                            }
                            secondary.push(LabeledSpan::new(
                                format!("{} declaration", to_ordinal_numeral(i + 1)),
                                symbol_decl,
                            ));
                        }
                        let mut error = IDPError::new(Redeclaration(redecl).into());
                        if let Some(main_span) = main_span {
                            error = error.with_span(main_span);
                        }
                        error.set_labels(secondary);
                        diag_builder.add_error(error);
                    }
                    Err(diag_builder.finish().unwrap())
                }
                FromBlocksKBErrorKind::InconsistentInterpretations(incon_interps) => {
                    let mut diag_builder = DiagnosticsBuilder::new();
                    for incon_interp in incon_interps.symbol_names {
                        diag_builder.add_error(IDPError::new(
                            InconsistentInterpretation {
                                symbol_name: incon_interp,
                            }
                            .into(),
                        ));
                    }
                    Err(diag_builder.finish().unwrap())
                }
                FromBlocksKBErrorKind::BlockMismatches(mismatches) => {
                    let mut diag_builder = DiagnosticsBuilder::new();
                    for mismatch in mismatches.0 {
                        diag_builder.add_error(IDPError::new(mismatch.into()));
                    }
                    Err(diag_builder.finish().unwrap())
                }
            },
        }
    }

    fn _theory_from_blocks(
        &self,
        blocks: &IndexSet<&str>,
    ) -> Result<Inferenceable, FromBlocksKBError> {
        let mut vocabularies = Vec::new();
        let mut theories = Vec::new();
        let mut structures = Vec::new();
        let mut missing = Vec::new();
        let mut mismatch = Vec::new();
        for (name, block) in blocks.into_iter().map(|f| (f, self.get(f))) {
            let Some(block) = block else {
                missing.push(name.to_string());
                continue;
            };
            match block {
                Block::Vocabulary { vocab, .. } => {
                    vocabularies.push(vocab.clone());
                }
                Block::Theory { theory: assert, .. } => {
                    theories.push(assert.clone());
                }
                Block::Structure { structure, .. } => {
                    structures.push(structure.clone());
                }
                Block::Procedure { procedure, .. } => {
                    mismatch.push(BlockMismatch {
                        name: procedure.name.to_string(),
                        expected: BlockKind::LogicalBlock,
                        found: BlockKind::Procedure,
                    });
                }
            }
        }
        if !missing.is_empty() {
            return Err(MissingBlocks(missing).into());
        }
        if !mismatch.is_empty() {
            return Err(BlockMismatches(mismatch).into());
        }
        Inferenceable::from_blocks(vocabularies, theories, structures).map_err(|f| f.into())
    }
}

#[derive(Debug, Clone)]
pub struct Iter<'a>(indexmap::map::Iter<'a, Rc<str>, Block>);

impl<'a> Iterator for Iter<'a> {
    type Item = (&'a str, &'a Block);

    fn next(&mut self) -> Option<Self::Item> {
        self.0.next().map(|f| (f.0.as_ref(), f.1))
    }

    fn size_hint(&self) -> (usize, Option<usize>) {
        self.0.size_hint()
    }

    fn count(self) -> usize {
        self.0.count()
    }

    fn nth(&mut self, n: usize) -> Option<Self::Item> {
        self.0.nth(n).map(|f| (f.0.as_ref(), f.1))
    }

    fn last(mut self) -> Option<Self::Item> {
        self.0.next_back().map(|f| (f.0.as_ref(), f.1))
    }

    fn collect<B: FromIterator<Self::Item>>(self) -> B {
        self.0.map(|f| (f.0.as_ref(), f.1)).collect()
    }
}

impl DoubleEndedIterator for Iter<'_> {
    fn next_back(&mut self) -> Option<Self::Item> {
        self.0.next_back().map(|f| (f.0.as_ref(), f.1))
    }

    fn nth_back(&mut self, n: usize) -> Option<Self::Item> {
        self.0.nth(n).map(|f| (f.0.as_ref(), f.1))
    }
}

impl<'a> IntoIterator for &'a KnowledgeBase {
    type Item = (&'a str, &'a Block);
    type IntoIter = Iter<'a>;

    fn into_iter(self) -> Self::IntoIter {
        self.iter()
    }
}

/// A special form of [KnowledgeBase], with one [Theory] and one [PartialStructure] over the same
/// [Vocabulary].
#[derive(Clone)]
pub struct Inferenceable {
    theory: Rc<Theory>,
    structure: PartialStructure,
}

impl FodotOptions for Inferenceable {
    type Options<'a> = FormatOptions;
}

impl FodotDisplay for Inferenceable {
    fn fmt(
        fmt: Fmt<&Self, Self::Options<'_>>,
        f: &mut std::fmt::Formatter<'_>,
    ) -> std::fmt::Result {
        write!(
            f,
            "\
                vocabulary {{
                    {}\
                }}\n\n\
                theory {{\n\
                    {}\
                }}\n\n\
                structure {{\n\
                    {}\
                }}\n\n\
            ",
            fmt.with_format_opts(fmt.value.vocab()),
            fmt.with_format_opts(fmt.value.theory()).with_indent(),
            fmt.with_format_opts(fmt.value.structure()).with_indent(),
        )
    }
}

impl Display for Inferenceable {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.display())
    }
}

display_as_debug!(Inferenceable);

impl Inferenceable {
    pub fn empty() -> Self {
        let (_, part_type_interps) = Vocabulary::new().complete_vocab();
        let type_interps = Rc::new(part_type_interps.try_err_complete().unwrap());
        Self {
            theory: Theory::new(type_interps.vocab_rc().clone()).into(),
            structure: PartialStructure::new(type_interps),
        }
    }

    /// Creates an new [Inferenceable].
    pub fn new(
        theory: Rc<Theory>,
        structure: PartialStructure,
    ) -> Result<Self, VocabMismatchError> {
        if !theory.vocab().exact_eq(structure.vocab()) {
            return Err(VocabMismatchError);
        }
        Ok(Self { theory, structure })
    }

    pub fn vocab(&self) -> &Vocabulary {
        self.structure.vocab()
    }

    pub fn vocab_rc(&self) -> &Rc<Vocabulary> {
        self.structure.vocab_rc()
    }

    pub fn type_interps(&self) -> &TypeInterps {
        self.structure.type_interps()
    }

    pub fn type_interps_rc(&self) -> &Rc<TypeInterps> {
        self.structure.type_interps_rc()
    }

    pub fn theory(&self) -> &Theory {
        &self.theory
    }

    pub fn theory_rc(&self) -> &Rc<Theory> {
        &self.theory
    }

    pub fn structure(&self) -> &PartialStructure {
        &self.structure
    }

    pub fn set_structure(&mut self, structure: PartialStructure) -> Result<(), VocabMismatchError> {
        if !vocabs_ptr_eq(Some(self.vocab()), Some(structure.vocab())) {
            return Err(VocabMismatchError);
        }
        self.structure = structure;
        Ok(())
    }

    pub(crate) fn lower(&self) -> Result<ParsedConstraints, SymbolError> {
        self.theory.lower(self.structure())
    }

    pub fn from_blocks(
        vocabularies: Vec<Rc<Vocabulary>>,
        theories: Vec<Theory>,
        structures: Vec<IncompleteStructure>,
    ) -> Result<Self, FromBlocksError> {
        if vocabularies.is_empty() && theories.is_empty() && structures.is_empty() {
            return Ok(Self::empty());
        }
        let mut vocabs_to_merge: IndexSet<_> = vocabularies
            .into_iter()
            .chain(theories.iter().map(|f| f.vocab_rc().clone()))
            .chain(structures.iter().map(|f| f.vocab_rc().clone()))
            .map(RcPtrEq)
            .collect();
        let mut final_vocab = vocabs_to_merge
            .shift_remove_index(0)
            .expect("we checked that at least one vocabulary/theory/structure exists")
            .0;
        let final_vocab_mut = Rc::make_mut(&mut final_vocab);
        let mut redecls = IndexSet::new();
        for vocab in vocabs_to_merge.into_iter().map(|f| f.0) {
            if let Err(value) = final_vocab_mut.merge(&vocab) {
                redecls.extend(value.take().0.into_iter());
            }
        }
        if !redecls.is_empty() {
            return Err(ManyRedeclarations(redecls.into_iter().collect()).into());
        }
        let theory = {
            let mut theories = theories;
            for assert in theories.iter_mut() {
                assert._vocab_swap(&final_vocab);
            }
            theories
                .into_iter()
                .reduce(|mut left, right| {
                    left.merge(right).expect("has same vocabulary");
                    left
                })
                .unwrap_or_else(|| Theory::new(final_vocab.clone()))
        };
        let structure = {
            let mut structures = structures;
            for structure in structures.iter_mut() {
                structure._swap_vocab(final_vocab.clone());
            }
            let structure = if !structures.is_empty() {
                let mut final_structure = structures.remove(0);
                let mut incon_assign = IndexSet::new();
                for structure in structures {
                    if let Err(value) = final_structure.merge(structure) {
                        match value.take_kind() {
                            InterpMergeErrorKind::VocabMismatchError(_) => {
                                unreachable!("has same vocab")
                            }
                            InterpMergeErrorKind::InconsistentInterpretations(interps) => {
                                incon_assign.extend(interps.symbol_names.into_iter());
                            }
                        }
                    }
                }
                if !incon_assign.is_empty() {
                    return Err(InconsistentInterpretations {
                        symbol_names: incon_assign.into_iter().collect(),
                    }
                    .into());
                }
                final_structure
            } else {
                IncompleteStructure::new(Vocabulary::get_type_interps(final_vocab))
            };
            structure
                .try_into_partial()
                .map_err(|f| f.type_interps().missing_type_error())?
        };
        Ok(Self::new(theory.into(), structure).expect("same vocabulary"))
    }

    /// Create a [Inferenceable] from a specification.
    ///
    /// The source string must contain one vocabulary block, one theory block and one
    /// structure block.
    pub fn from_specification(source: &str) -> Result<Self, Diagnostics> {
        let (lazy, diag) = LazyKnowledgeBase::new(source, Default::default());
        if let Some(diag) = diag {
            return Err(diag);
        }
        let mut diagnostics = DiagnosticsBuilder::new();
        {
            let mut vocab_name = None;
            for the in lazy.iter_block_name().filter_map(|f| match f {
                BlockName::Vocabulary(vocab) => Some(vocab),
                _ => None,
            }) {
                if vocab_name.is_none() {
                    vocab_name = Some(the);
                } else {
                    diagnostics.add_error(IDPError::new(
                        ParseError {
                            message: "only one vocab block allowed".into(),
                        }
                        .into(),
                    ));
                }
            }
        }
        let mut theory_name = None;
        for the in lazy.iter_block_name().filter_map(|f| match f {
            BlockName::Theory { block, .. } => Some(block),
            _ => None,
        }) {
            if theory_name.is_none() {
                theory_name = Some(the);
            } else {
                diagnostics.add_error(IDPError::new(
                    ParseError {
                        message: "only one theory block allowed".into(),
                    }
                    .into(),
                ));
            }
        }
        let mut structure_name = None;
        for stru in lazy.iter_block_name().filter_map(|f| match f {
            BlockName::Structure { block, .. } => Some(block),
            _ => None,
        }) {
            if structure_name.is_none() {
                structure_name = Some(stru);
            } else {
                diagnostics.add_error(IDPError::new(
                    ParseError {
                        message: "only one structure block allowed".into(),
                    }
                    .into(),
                ));
            }
        }
        let Some(theory_name) = theory_name else {
            return Err(diagnostics.finish_with(IDPError::new(
                ParseError {
                    message: "missing a theory block".into(),
                }
                .into(),
            )));
        };
        let Some(structure_name) = structure_name else {
            return Err(diagnostics.finish_with(IDPError::new(
                ParseError {
                    message: "missing a structure block".into(),
                }
                .into(),
            )));
        };
        let theory = lazy
            .get(theory_name)
            .expect("we previously checked if this block exists")
            .map(|f| {
                f.clone()
                    .expect_theory("we previously checked if this theory exists")
            })
            .map_err(|f| f.add_to_diagnostics(&mut diagnostics))
            .ok();
        let structure = lazy
            .get(structure_name)
            .expect("we previously checked if this block exists")
            .map(|f| {
                f.clone()
                    .expect_structure("we previously checked if this structure exists")
            })
            .map_err(|f| f.add_to_diagnostics(&mut diagnostics))
            .ok();
        let mut diagnostics = match diagnostics.finish() {
            Ok(diag) => return Err(diag),
            Err(diag) => diag,
        };
        let (theory, _) = theory.expect("non empty diagnostic, due to map_err");
        let (structure, struct_metadata) = structure.expect("non empty diagnostic, due to map_err");
        let Ok(structure) = structure.try_into_partial().map_err(|f| {
            diagnostics.add_error(IDPError::new_with_span(
                f.type_interps().missing_type_error().into(),
                struct_metadata.block.span,
            ));
        }) else {
            return Err(diagnostics.finish().expect("we just added an error"));
        };
        let inferenceable = Self::new(Rc::new(theory), structure)
            .expect("we checked for the existence of only one vocab block");

        if let Ok(diag) = diagnostics.finish() {
            Err(diag)
        } else {
            Ok(inferenceable)
        }
    }
}

struct RcPtrEq<T>(Rc<T>);

impl<T> Debug for RcPtrEq<T> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "RcPtrEq({:p})", self.0.as_ref())
    }
}

impl<T> PartialEq for RcPtrEq<T> {
    fn eq(&self, other: &Self) -> bool {
        Rc::ptr_eq(&self.0, &other.0)
    }
}

impl<T> Eq for RcPtrEq<T> {}

impl<T> Hash for RcPtrEq<T> {
    fn hash<H: std::hash::Hasher>(&self, state: &mut H) {
        core::ptr::hash(self.0.as_ref(), state)
    }
}
