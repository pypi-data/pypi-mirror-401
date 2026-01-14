use super::{
    Block, BlockMetadata, BlockName, BlockType, KnowledgeBase, StructureBlockMetadata,
    TheoryBlockMetadata, VocabBlockMetadata,
};
use crate::{
    ast::ProcedureBlock,
    fodot::{
        error::{
            BlockMismatch, BlockRedeclaration, MissingBlock,
            parse::{Diagnostics, DiagnosticsBuilder, IDPError},
        },
        knowledge_base::{
            ProcedureMetadata,
            procedure::{Procedure, ProcedureLang},
        },
        vocabulary::Vocabulary,
    },
};
use crate::{
    ast::{
        self, Ast, Parser, Span, Spanned, StructureBlock, TheoryBlock, VocabBlock,
        tree_sitter::{TsAst, TsParser},
    },
    sli_entrance,
};
use indexmap::{IndexMap, map};
use itertools::Either;
use sli_collections::{cell::OnceCell, rc::Rc};
use std::{borrow::Cow, ops::Deref};

pub struct LazyKnowledgeBase<'a> {
    source: &'a str,
    ast: TsAst,
    blocks: IndexMap<Rc<str>, LazyBlock>,
    dep_count: IndexMap<Rc<str>, usize>,
    config: KnowledgeBaseConfig,
}

#[derive(Debug, Clone)]
enum _BlockName {
    Vocabulary,
    Theory {
        vocab_name: Rc<str>,
        vocab_span: Option<Span>,
    },
    Structure {
        vocab_name: Rc<str>,
        vocab_span: Option<Span>,
    },
    Procedure,
}

struct LazyBlock {
    block: OnceCell<(Block, Option<Diagnostics>)>,
    pos: LazyBlockPos,
}

enum LazyBlockPos {
    Pos {
        decl_or_name_span: Span,
        name: _BlockName,
        pos: usize,
    },
    Redeclaration {
        error: BlockRedeclaration,
        span: Span,
    },
}

pub struct KnowledgeBaseConfig {
    pub default_theory_name: Rc<str>,
    pub default_vocabulary_name: Rc<str>,
    pub default_structure_name: Rc<str>,
}

impl Default for KnowledgeBaseConfig {
    fn default() -> Self {
        Self {
            default_theory_name: "T".into(),
            default_vocabulary_name: "V".into(),
            default_structure_name: "S".into(),
        }
    }
}

#[derive(Debug, Clone)]
pub enum LazyError<T, D = T> {
    Block(BlockError<T>),
    BlockDependency { name: String, error: BlockError<D> },
}

impl ToDiagnostics for LazyError<&'_ Diagnostics> {
    fn diag_or_idp_error(self) -> Either<DiagnosticsBuilder, IDPError> {
        match self {
            Self::Block(block) => block.diag_or_idp_error(),
            Self::BlockDependency { error, .. } => error.diag_or_idp_error(),
        }
    }
}

#[derive(Debug, Clone)]
pub enum BlockError<T> {
    Diagnostics(T),
    Redeclaration {
        error: BlockRedeclaration,
        span: Span,
    },
    MissingBlock {
        error: MissingBlock,
        span: Span,
    },
    BlockMismatch {
        error: BlockMismatch,
        span: Span,
    },
}

pub trait ToDiagnostics: Sized {
    fn add_to_diagnostics(self, diagnostics: &mut DiagnosticsBuilder) {
        match self.diag_or_idp_error() {
            Either::Left(mut diag) => diagnostics.append_builder(&mut diag),
            Either::Right(error) => diagnostics.add_error(error),
        }
    }
    fn diag_or_idp_error(self) -> Either<DiagnosticsBuilder, IDPError>;
}

impl ToDiagnostics for BlockError<&'_ Diagnostics> {
    fn diag_or_idp_error(self) -> Either<DiagnosticsBuilder, IDPError> {
        match self {
            Self::Diagnostics(diag) => Either::Left(diag.clone().into()),
            Self::Redeclaration { error, span } => {
                Either::Right(IDPError::new_with_span(error.into(), span))
            }
            Self::MissingBlock { error, span } => {
                Either::Right(IDPError::new_with_span(error.into(), span))
            }
            Self::BlockMismatch { error, span } => {
                Either::Right(IDPError::new_with_span(error.into(), span))
            }
        }
    }
}

pub type LazyErrorRef<'a> = LazyError<&'a Diagnostics>;

impl<'a> LazyKnowledgeBase<'a> {
    pub fn new(source: &'a str, config: KnowledgeBaseConfig) -> (Self, Option<Diagnostics>) {
        let mut parser = TsParser::new();
        let ast = parser.parse(source);
        let get_name = |name: Option<ast::Span>, default: &Rc<str>| {
            name.map(|f| f.get_str(source).as_ref().into())
                .unwrap_or_else(|| default.clone())
        };
        let get_vocab_name =
            |name: Option<ast::Span>| get_name(name, &config.default_vocabulary_name);
        let get_theory_name = |name: Option<ast::Span>| get_name(name, &config.default_theory_name);
        let get_structure_name =
            |name: Option<ast::Span>| get_name(name, &config.default_structure_name);
        let mut blocks = IndexMap::default();
        let mut dep_count = IndexMap::default();
        let mut diag = DiagnosticsBuilder::new();
        for ((block_name, decl_or_name_span), (name, pos)) in
            ast.iter_decls().enumerate().map(|(i, f)| match f {
                ast::Block::Vocab(vocab) => {
                    let block_name = get_vocab_name(vocab.name());
                    let decl_or_name_span = vocab
                        .name()
                        .map(|f| (vocab.keyword_span().start..f.end).into())
                        .unwrap_or(vocab.keyword_span());
                    (
                        (block_name.clone(), decl_or_name_span),
                        (_BlockName::Vocabulary, i),
                    )
                }
                ast::Block::Theory(theory) => {
                    let theory_name = theory.names();
                    let block_name = get_theory_name(theory_name.as_ref().map(|f| f.theory_name));
                    let decl_or_name_span = theory
                        .names()
                        .map(|f| (theory.keyword_span().start..f.vocab_name.end).into())
                        .unwrap_or(theory.keyword_span());
                    let vocab_span = theory_name.as_ref().map(|f| f.vocab_name);
                    let vocab_name = get_vocab_name(vocab_span);
                    dep_count
                        .entry(vocab_name.clone())
                        .and_modify(|f| *f += 1)
                        .or_insert(1);
                    (
                        (block_name.clone(), decl_or_name_span),
                        (
                            _BlockName::Theory {
                                vocab_name,
                                vocab_span,
                            },
                            i,
                        ),
                    )
                }
                ast::Block::Structure(structure) => {
                    let structure_name = structure.names();
                    let block_name =
                        get_structure_name(structure_name.as_ref().map(|f| f.structure_name));
                    let decl_or_name_span = structure
                        .names()
                        .map(|f| (structure.keyword_span().start..f.vocab_name.end).into())
                        .unwrap_or(structure.keyword_span());
                    let vocab_span = structure_name.as_ref().map(|f| f.vocab_name);
                    let vocab_name = get_vocab_name(vocab_span);
                    dep_count
                        .entry(vocab_name.clone())
                        .and_modify(|f| *f += 1)
                        .or_insert(1);
                    (
                        (block_name.clone(), decl_or_name_span),
                        (
                            _BlockName::Structure {
                                vocab_name,
                                vocab_span,
                            },
                            i,
                        ),
                    )
                }
                ast::Block::Procedure(procedure) => {
                    let name = procedure.name().get_str(source).as_ref().into();
                    let decl_span = (procedure.keyword_span().start..procedure.name().end).into();
                    ((name, decl_span), (_BlockName::Procedure, i))
                }
            })
        {
            match blocks.entry(block_name.clone()) {
                map::Entry::Occupied(mut occupied) => {
                    let block_redecl = BlockRedeclaration(block_name.as_ref().into());
                    diag.add_error(IDPError::new_with_span(
                        block_redecl.clone().into(),
                        decl_or_name_span,
                    ));
                    *occupied.get_mut() = LazyBlock {
                        block: Default::default(),
                        pos: LazyBlockPos::Redeclaration {
                            error: block_redecl,
                            span: decl_or_name_span,
                        },
                    };
                }
                map::Entry::Vacant(vacant) => {
                    vacant.insert(LazyBlock {
                        block: Default::default(),
                        pos: LazyBlockPos::Pos {
                            decl_or_name_span,
                            name,
                            pos,
                        },
                    });
                }
            }
        }
        for (parse_error, span) in ast.parse_errors() {
            diag.add_error(IDPError::new_with_span(parse_error.into(), span));
        }
        (
            Self {
                source,
                ast,
                blocks,
                dep_count,
                config,
            },
            diag.finish().ok(),
        )
    }

    pub fn iter_block_name(&self) -> impl Iterator<Item = BlockName<'_>> + '_ {
        self.blocks.iter().filter_map(|f| match &f.1.pos {
            LazyBlockPos::Pos {
                name: _BlockName::Vocabulary,
                ..
            } => Some(BlockName::Vocabulary(f.0.deref())),
            LazyBlockPos::Pos {
                name: _BlockName::Theory { vocab_name, .. },
                ..
            } => Some(BlockName::Theory {
                block: f.0.deref(),
                vocab: vocab_name.deref(),
            }),
            LazyBlockPos::Pos {
                name: _BlockName::Structure { vocab_name, .. },
                ..
            } => Some(BlockName::Structure {
                block: f.0.deref(),
                vocab: vocab_name.deref(),
            }),
            LazyBlockPos::Pos {
                name: _BlockName::Procedure,
                ..
            } => Some(BlockName::Procedure(f.0.deref())),
            LazyBlockPos::Redeclaration { .. } => None,
        })
    }

    pub fn into_knowledge_base(self) -> Result<KnowledgeBase, Diagnostics> {
        let mut blocks = IndexMap::default();
        let mut diag_builder = DiagnosticsBuilder::new();
        for (name, block) in self._into_iter() {
            match block {
                Ok(block) => {
                    blocks.insert(name, block);
                }
                Err(LazyError::Block(BlockError::Diagnostics(diag))) => {
                    diag_builder.append_diag(diag);
                }
                Err(LazyError::Block(BlockError::BlockMismatch { error, span })) => {
                    diag_builder.add_error(IDPError::new_with_span(error.into(), span));
                }
                Err(LazyError::Block(BlockError::Redeclaration { error, span })) => {
                    diag_builder.add_error(IDPError::new_with_span(error.into(), span));
                }
                Err(LazyError::Block(BlockError::MissingBlock { error, span })) => {
                    diag_builder.add_error(IDPError::new_with_span(error.into(), span));
                }
                Err(LazyError::BlockDependency { .. }) => {}
            }
        }
        if let Ok(diag) = diag_builder.finish() {
            Err(diag)
        } else {
            Ok(KnowledgeBase { blocks })
        }
    }

    fn _into_iter(self) -> lazy_knowledge_base::_IntoIter<'a> {
        lazy_knowledge_base::_IntoIter::new(self)
    }

    /// Take ownership of the given block in the knowledge base.
    ///
    /// If the block is depended on by other blocks it will be cloned otherwise it is removed from
    /// the knowledge base.
    pub fn take(&mut self, name: &str) -> Option<Result<Block, LazyError<Diagnostics, ()>>> {
        match self.get(name)? {
            Ok(block) => {
                let dep_count = self.dep_count.get(name).copied().unwrap_or(0);
                if dep_count != 0 {
                    return Some(Ok(block.clone()));
                }
            }
            Err(LazyError::BlockDependency { name, error }) => {
                return Some(Err(LazyError::BlockDependency {
                    name,
                    error: match error {
                        BlockError::Diagnostics(_) => BlockError::Diagnostics(()),
                        BlockError::Redeclaration { error, span } => {
                            BlockError::Redeclaration { error, span }
                        }
                        BlockError::MissingBlock { error, span } => {
                            BlockError::MissingBlock { error, span }
                        }
                        BlockError::BlockMismatch { error, span } => {
                            BlockError::BlockMismatch { error, span }
                        }
                    },
                }));
            }
            Err(LazyError::Block(BlockError::Redeclaration { error, span })) => {
                return Some(Err(LazyError::Block(BlockError::Redeclaration {
                    error,
                    span,
                })));
            }
            Err(LazyError::Block(BlockError::MissingBlock { error, span })) => {
                return Some(Err(LazyError::Block(BlockError::MissingBlock {
                    error,
                    span,
                })));
            }
            Err(LazyError::Block(BlockError::BlockMismatch { error, span })) => {
                return Some(Err(LazyError::Block(BlockError::BlockMismatch {
                    error,
                    span,
                })));
            }
            // Ignore diagnostics here, so we can remove it from the lazy kb
            Err(LazyError::Block(BlockError::Diagnostics(_))) => {}
        }
        // shift_remove retains the ordering of the blocks, we don't use the indexes
        let mut lazy_block = self.blocks.shift_remove(name)?;
        match (lazy_block.block.take(), lazy_block.pos) {
            (Some((_, Some(diags))), _) => {
                Some(Err(LazyError::Block(BlockError::Diagnostics(diags))))
            }
            (Some((Block::Theory { theory, metadata }, _)), _) => {
                let vocab_name = metadata
                    .name_span
                    .as_ref()
                    .map(|f| &self.source[f.vocab_name.start..f.vocab_name.end])
                    .unwrap_or_else(|| &self.config.default_vocabulary_name);
                *self.dep_count.get_mut(vocab_name).unwrap() -= 1;
                Some(Ok(Block::Theory { theory, metadata }))
            }
            (
                Some((
                    Block::Structure {
                        structure,
                        metadata,
                    },
                    _,
                )),
                _,
            ) => {
                let vocab_name = metadata
                    .name_span
                    .as_ref()
                    .map(|f| &self.source[f.vocab_name.start..f.vocab_name.end])
                    .unwrap_or_else(|| &self.config.default_vocabulary_name);
                *self.dep_count.get_mut(vocab_name).unwrap() -= 1;
                Some(Ok(Block::Structure {
                    structure,
                    metadata,
                }))
            }
            (Some((Block::Vocabulary { vocab, metadata }, _)), _) => {
                Some(Ok(Block::Vocabulary { vocab, metadata }))
            }
            (
                Some((
                    Block::Procedure {
                        procedure,
                        metadata,
                    },
                    _,
                )),
                _,
            ) => Some(Ok(Block::Procedure {
                procedure,
                metadata,
            })),
            // There was an error in the dependency, which we check for and bail early if so
            (None, _) => unreachable!(),
        }
    }

    /// Tries getting the block with name `name` if it exists.
    ///
    /// Returns [Err] if the block is incorrect at the knowledge base level
    /// e.g. two blocks have the same name.
    pub fn get<'b>(&'b self, name: &str) -> Option<Result<&'b Block, LazyErrorRef<'b>>> {
        let (name_rc, lazy_block) = self.blocks.get_key_value(name)?;
        if let Some((block, diag)) = lazy_block.block.get() {
            if let Some(diag) = diag {
                return Some(Err(LazyError::Block(BlockError::Diagnostics(diag))));
            }
            return Some(Ok(block));
        }
        /// Checks if the given name is a vocabulary without evaluating the block.
        fn vocab_dep_err<'b>(
            this: &LazyKnowledgeBase<'b>,
            vocab_name: &str,
            vocab_span: Option<Span>,
            decl_span: Span,
        ) -> Result<(), LazyErrorRef<'b>> {
            match this.blocks.get(vocab_name) {
                Some(LazyBlock {
                    block: _,
                    pos: LazyBlockPos::Pos { name, .. },
                }) => {
                    let found = match name {
                        _BlockName::Vocabulary => None,
                        _BlockName::Theory { .. } => Some(BlockType::Theory),
                        _BlockName::Structure { .. } => Some(BlockType::Structure),
                        _BlockName::Procedure => Some(BlockType::Procedure),
                    };
                    if let Some(found) = found {
                        return Err(LazyError::Block(BlockError::BlockMismatch {
                            error: BlockMismatch {
                                name: vocab_name.to_string(),
                                expected: BlockType::Vocabulary.into(),
                                found: found.into(),
                            },
                            span: vocab_span.unwrap_or(decl_span),
                        }));
                    }
                }
                Some(LazyBlock {
                    block: _,
                    pos: LazyBlockPos::Redeclaration { .. },
                }) => {}
                None => {
                    return Err(LazyError::Block(BlockError::MissingBlock {
                        error: MissingBlock(vocab_name.to_string()),
                        span: vocab_span.unwrap_or(decl_span),
                    }));
                }
            }
            Ok(())
        }
        match &lazy_block.pos {
            LazyBlockPos::Redeclaration { error, span } => {
                Some(Err(LazyError::Block(BlockError::Redeclaration {
                    error: error.clone(),
                    span: *span,
                })))
            }
            LazyBlockPos::Pos {
                name: block_name,
                pos,
                decl_or_name_span: decl_span,
            } => match block_name {
                _BlockName::Vocabulary => {
                    let (block, diag) = lazy_block.block.get_or_init(|| {
                        let block = match self.ast.iter_decls().nth(*pos).unwrap() {
                            ast::Block::Vocab(vocab_block) => vocab_block,
                            _ => panic!("Mismatched blocks"),
                        };
                        let metadata = VocabBlockMetadata {
                            block: BlockMetadata {
                                decl_span: block.decl_span(),
                                span: block.span(),
                            },
                            name_span: block.name(),
                        };

                        let mut diag = DiagnosticsBuilder::new();
                        let vocab = sli_entrance::parse_vocab(&self.source, &block, &mut diag);
                        (
                            Block::Vocabulary {
                                vocab: Rc::new(vocab),
                                metadata,
                            },
                            diag.finish().ok(),
                        )
                    });
                    if let Some(diag) = diag {
                        Some(Err(LazyError::Block(BlockError::Diagnostics(diag))))
                    } else {
                        Some(Ok(block))
                    }
                }
                _BlockName::Theory {
                    vocab_name,
                    vocab_span,
                } => {
                    let ast_block = match self.ast.iter_decls().nth(*pos).unwrap() {
                        ast::Block::Theory(ast_block) => ast_block,
                        _ => panic!("Mismatched blocks"),
                    };
                    if let Err(value) = vocab_dep_err(self, vocab_name, *vocab_span, *decl_span) {
                        return Some(Err(value));
                    }
                    let vocab = match self.get(vocab_name) {
                        Some(Ok(Block::Vocabulary { vocab, .. })) => vocab.clone(),
                        // vocab_dep_err returns an error if `vocab_name` was not a vocabulary
                        Some(Ok(_)) => unreachable!(),
                        Some(Err(value)) => match value {
                            value @ LazyError::BlockDependency { .. } => return Some(Err(value)),
                            LazyError::Block(value) => {
                                return Some(Err(LazyError::BlockDependency {
                                    name: vocab_name.to_string(),
                                    error: value,
                                }));
                            }
                        },
                        // vocab_dep_err returns an error if `vocab_name` is missing
                        None => unreachable!(),
                    };
                    let (block, diag) = lazy_block.block.get_or_init(|| {
                        let metadata = TheoryBlockMetadata {
                            block: BlockMetadata {
                                decl_span: ast_block.decl_span(),
                                span: ast_block.span(),
                            },
                            vocab_name: vocab_name.to_string().into_boxed_str(),
                            name_span: ast_block.names(),
                        };

                        let mut diag = DiagnosticsBuilder::new();
                        let theory =
                            sli_entrance::parse_theory(&vocab, &ast_block, &self.source, &mut diag);
                        (Block::Theory { theory, metadata }, diag.finish().ok())
                    });
                    if let Some(diag) = diag {
                        Some(Err(LazyError::Block(BlockError::Diagnostics(diag))))
                    } else {
                        Some(Ok(block))
                    }
                }
                _BlockName::Structure {
                    vocab_name,
                    vocab_span,
                } => {
                    let ast_block = match self.ast.iter_decls().nth(*pos).unwrap() {
                        ast::Block::Structure(block) => block,
                        _ => panic!("Mismatched blocks"),
                    };
                    if let Err(value) = vocab_dep_err(self, vocab_name, *vocab_span, *decl_span) {
                        return Some(Err(value));
                    }
                    let vocab = match self.get(vocab_name) {
                        Some(Ok(Block::Vocabulary { vocab, .. })) => vocab.clone(),
                        // vocab_dep_err returns an error if `vocab_name` was not a vocabulary
                        Some(Ok(_)) => unreachable!(),
                        Some(Err(value)) => match value {
                            value @ LazyError::BlockDependency { .. } => return Some(Err(value)),
                            LazyError::Block(value) => {
                                return Some(Err(LazyError::BlockDependency {
                                    name: vocab_name.to_string(),
                                    error: value,
                                }));
                            }
                        },
                        // vocab_dep_err returns an error if `vocab_name` is missing
                        None => unreachable!(),
                    };
                    let (block, diag) = lazy_block.block.get_or_init(|| {
                        let metadata = StructureBlockMetadata {
                            block: BlockMetadata {
                                decl_span: ast_block.decl_span(),
                                span: ast_block.span(),
                            },
                            vocab_name: vocab_name.to_string().into_boxed_str(),
                            name_span: ast_block.names(),
                        };

                        let mut diag = DiagnosticsBuilder::new();
                        let structure = sli_entrance::parse_struct(
                            Vocabulary::get_type_interps(vocab.clone()),
                            &vocab,
                            &ast_block,
                            &self.source,
                            &mut diag,
                        );
                        (
                            Block::Structure {
                                structure,
                                metadata,
                            },
                            diag.finish().ok(),
                        )
                    });
                    if let Some(diag) = diag {
                        Some(Err(LazyError::Block(BlockError::Diagnostics(diag))))
                    } else {
                        Some(Ok(block))
                    }
                }
                _BlockName::Procedure => {
                    let (block, _) = lazy_block.block.get_or_init(|| {
                        let ast_block = match self.ast.iter_decls().nth(*pos).unwrap() {
                            ast::Block::Procedure(block) => block,
                            _ => panic!("Mismatched blocks"),
                        };
                        let procedure = Procedure {
                            lang: ProcedureLang::Python,
                            name: name_rc.clone(),
                            args: ast_block
                                .args()
                                .map(|f| Cow::into_owned(f.get_str(self.source)).into())
                                .collect(),
                            content: ast_block
                                .content()
                                .map(|f| Cow::into_owned(f.get_str(self.source)).into())
                                .unwrap_or_else(|| "".into()),
                        };
                        let metadata = ProcedureMetadata {
                            block: BlockMetadata {
                                span: ast_block.span(),
                                decl_span: *decl_span,
                            },
                            name: ast_block.name(),
                            args: ast_block.args().collect(),
                        };
                        (
                            Block::Procedure {
                                procedure,
                                metadata,
                            },
                            None,
                        )
                    });
                    Some(Ok(block))
                }
            },
        }
    }
}

impl<'a> IntoIterator for LazyKnowledgeBase<'a> {
    type Item = (Box<str>, Result<Block, LazyError<Diagnostics, ()>>);
    type IntoIter = lazy_knowledge_base::IntoIter<'a>;

    fn into_iter(self) -> Self::IntoIter {
        lazy_knowledge_base::IntoIter::new(self)
    }
}

mod lazy_knowledge_base {
    use super::{Block, LazyError, LazyKnowledgeBase};
    use crate::fodot::error::parse::Diagnostics;
    use sli_collections::rc::Rc;
    use std::ops::Deref;
    use std::vec;

    pub(crate) struct _IntoIter<'a> {
        names: vec::IntoIter<Rc<str>>,
        lazy_kb: LazyKnowledgeBase<'a>,
    }

    impl<'a> _IntoIter<'a> {
        pub(super) fn new(lazy_kb: LazyKnowledgeBase<'a>) -> Self {
            Self {
                names: lazy_kb
                    .blocks
                    .keys()
                    .cloned()
                    .collect::<Vec<_>>()
                    .into_iter(),
                lazy_kb,
            }
        }
    }

    impl Iterator for _IntoIter<'_> {
        type Item = (Rc<str>, Result<Block, LazyError<Diagnostics, ()>>);

        fn next(&mut self) -> Option<Self::Item> {
            let name = self.names.next()?;
            let block = self.lazy_kb.take(&name).unwrap();
            Some((name, block))
        }
    }

    pub struct IntoIter<'a>(_IntoIter<'a>);

    impl<'a> IntoIter<'a> {
        pub(super) fn new(lazy_kb: LazyKnowledgeBase<'a>) -> Self {
            Self(_IntoIter::new(lazy_kb))
        }
    }

    impl Iterator for IntoIter<'_> {
        type Item = (Box<str>, Result<Block, LazyError<Diagnostics, ()>>);

        fn next(&mut self) -> Option<Self::Item> {
            self.0.next().map(|f| (f.0.deref().into(), f.1))
        }
    }
}
