//! [ast] implementation for FO(·) tree-sitter parser.
use super::{
    AppliedSymbol, Assertion, AstParser, BinaryOp, BinaryOpKind, CmpOp, ConjuctiveGuard, CountAgg,
    Declaration, Definition, DefinitionalRule, Element, Enumeration, EnumerationInterpretation,
    EnumerationRange, Expression, Expressions, IfGuard, ImplicativeGuard, InEnumeration, Ite,
    MaybePoisoned, ParseError, PfuncDeclaration, ProcedureBlock, Quantification,
    QuantificationKind, SetElement, Span, Spanned, StructureAst, StructureBlock, StructureNames,
    SumAgg, SymbolInterpretation, TheoryAst, TheoryBlock, TheoryDecls, TheoryNames, Tuple,
    TypeDeclaration, UnaryOp, Variables, VocabAst, VocabBlock, VocabDecls,
};
use crate::ast::{self, CmpOpKind};
use itertools::Either;
use std::{marker::PhantomData, num::NonZeroU16, ops::Range};
use tree_sitter::Node;
use tree_sitter_fodot::{FodotFields, FodotSymbols};

trait NamedChildByFieldId: Sized {
    /// Looks for the first named child, returns none on error or missing node, and ignores extra nodes
    /// (comments).
    fn named_child_by_field_id(&self, field_id: u16) -> Option<Self>;
}

impl NamedChildByFieldId for Node<'_> {
    fn named_child_by_field_id(&self, field_id: u16) -> Option<Self> {
        self.child_by_field_id(field_id).and_then(|f| {
            let mut cur = Some(f);
            while let Some(cur_val) = cur {
                if cur_val.is_error() || cur_val.is_missing() {
                    return None;
                }
                // SymComment may appear everywhere but should be ignored
                if cur_val.is_named()
                    && FodotSymbols::from(cur_val.kind_id()) != FodotSymbols::SymComment
                {
                    break;
                }
                cur = cur_val.next_named_sibling();
                if cur.is_none() {
                    cur = cur_val.named_child(0);
                }
            }
            cur
        })
    }
}

struct NamedChildrenIter<'a> {
    named_children: Range<usize>,
    cursor: tree_sitter::TreeCursor<'a>,
}

impl<'a> NamedChildrenIter<'a> {
    fn new(node: &Node<'a>) -> Self {
        let mut cursor = node.walk();
        cursor.goto_first_child();
        Self {
            named_children: 0..node.named_child_count(),
            cursor,
        }
    }
}

impl<'a> Iterator for NamedChildrenIter<'a> {
    type Item = Node<'a>;

    fn next(&mut self) -> Option<Self::Item> {
        self.named_children.next().map(|_| {
            while !self.cursor.node().is_named() {
                if !self.cursor.goto_next_sibling() {
                    break;
                }
            }
            let result = self.cursor.node();
            self.cursor.goto_next_sibling();
            result
        })
    }
}

struct FieldChildrenIter<'a> {
    cursor: tree_sitter::TreeCursor<'a>,
    field_id: core::num::NonZeroU16,
    done: bool,
}

impl<'a> FieldChildrenIter<'a> {
    fn new(node: &Node<'a>, field_id: u16) -> Self {
        let mut cursor = node.walk();
        cursor.goto_first_child();
        Self {
            cursor,
            done: false,
            field_id: field_id.try_into().unwrap(),
        }
    }

    #[allow(unused)]
    fn empty(cursor: tree_sitter::TreeCursor<'a>) -> Self {
        Self {
            cursor,
            done: true,
            field_id: NonZeroU16::new(1).unwrap(),
        }
    }
}

impl<'a> Iterator for FieldChildrenIter<'a> {
    type Item = Node<'a>;

    fn next(&mut self) -> Option<Self::Item> {
        if self.done {
            return None;
        }
        while self.cursor.field_id() != Some(self.field_id) {
            if !self.cursor.goto_next_sibling() {
                return None;
            }
        }
        let result = self.cursor.node();
        if !self.cursor.goto_next_sibling() {
            self.done = true;
        }
        Some(result)
    }
}

struct NodeTraversal<'a> {
    cursor: Option<tree_sitter::TreeCursor<'a>>,
}

impl<'a> NodeTraversal<'a> {
    fn new(node: Node<'a>) -> Self {
        Self {
            cursor: node.walk().into(),
        }
    }
}

impl<'a> Iterator for NodeTraversal<'a> {
    type Item = Node<'a>;

    fn next(&mut self) -> Option<Self::Item> {
        let cursor = match &mut self.cursor {
            Some(cursor) => cursor,
            None => return None,
        };

        let node = cursor.node();

        if cursor.goto_first_child() || cursor.goto_next_sibling() {
            return Some(node);
        }

        loop {
            if !cursor.goto_parent() {
                self.cursor = None;
                break;
            }

            if cursor.goto_next_sibling() {
                break;
            }
        }
        Some(node)
    }
}

pub struct TsParser(tree_sitter::Parser);

impl Default for TsParser {
    fn default() -> Self {
        Self::new()
    }
}

impl TsParser {
    pub fn new() -> Self {
        let mut ts_parser = tree_sitter::Parser::new();
        ts_parser
            .set_language(&tree_sitter_fodot::language())
            .expect("Incompatible tree-sitter version");
        Self(ts_parser)
    }
}

struct StitchedStr<'a> {
    pre: &'a str,
    middle: &'a str,
    post: &'a str,
}

impl StitchedStr<'_> {
    fn get_longest_at(&self, pos: usize) -> &str {
        if pos < self.pre.len() {
            &self.pre[pos..]
        } else if pos < self.pre.len() + self.middle.len() {
            &self.middle[(pos - self.pre.len())..]
        } else {
            &self.post[(pos - self.pre.len() - self.middle.len())..]
        }
    }
}

const PREFIX_VOCAB_DECL_PARSE: &str = "vocabulary {";
const POSTFIX_DECL_PARSE: &str = "}";

const PREFIX_THEORY_DECL_PARSE: &str = "theory {";
const PREFIX_STRUCTURE_DECL_PARSE: &str = "structure {";

impl ast::Parser<&str> for TsParser {
    fn parse(&mut self, source: &str) -> Self::Ast {
        TsAst(self.0.parse(source, None).unwrap())
    }

    fn parse_vocab(&mut self, source: &str) -> <Self::Ast as ast::Ast>::VocabAst {
        let stitched = StitchedStr {
            pre: PREFIX_VOCAB_DECL_PARSE,
            middle: source,
            post: POSTFIX_DECL_PARSE,
        };
        TsVocabAst(
            self.0
                .parse_with_options(&mut |pos, _| stitched.get_longest_at(pos), None, None)
                .unwrap(),
        )
    }

    fn parse_theory(&mut self, source: &str) -> <Self::Ast as ast::Ast>::TheoryAst {
        let stitched = StitchedStr {
            pre: PREFIX_THEORY_DECL_PARSE,
            middle: source,
            post: POSTFIX_DECL_PARSE,
        };
        TsTheoryAst(
            self.0
                .parse_with_options(&mut |pos, _| stitched.get_longest_at(pos), None, None)
                .unwrap(),
        )
    }

    fn parse_structure(&mut self, source: &str) -> <Self::Ast as ast::Ast>::StructureAst {
        let stitched = StitchedStr {
            pre: PREFIX_STRUCTURE_DECL_PARSE,
            middle: source,
            post: POSTFIX_DECL_PARSE,
        };
        TsStructureAst(
            self.0
                .parse_with_options(&mut |pos, _| stitched.get_longest_at(pos), None, None)
                .unwrap(),
        )
    }
}

impl AstParser for TsParser {
    type Ast = TsAst;
}

pub struct TsAst(tree_sitter::Tree);

fn get_errors(node: tree_sitter::Node) -> impl Iterator<Item = (ast::ParseError, Span)> {
    if node.has_error() {
        Either::Left(NodeTraversal::new(node).filter_map(|f| {
            if f.is_error() {
                Some((
                    ParseError {
                        message: "invalid fodot".into(),
                    },
                    (f.start_byte()..f.end_byte()).into(),
                ))
            } else if f.is_missing() {
                Some((
                    ParseError {
                        message: format!("invalid fodot: missing a {}", f.kind()),
                    },
                    (f.start_byte()..f.end_byte()).into(),
                ))
            } else {
                None
            }
        }))
    } else {
        Either::Right(core::iter::empty())
    }
}

fn get_decl_errors(
    node: tree_sitter::Node,
    message: &str,
) -> impl Iterator<Item = (ast::ParseError, Span)> {
    get_errors(node).chain({
        let root = node;
        if root.child_count() > 1 {
            // Since we add a postfix to the parser by hand we must remove its span from the
            // root_node
            let end = root.end_byte() - POSTFIX_DECL_PARSE.len();
            let second = root.child(1).unwrap();
            let start = second.start_byte();
            Some((
                ast::ParseError {
                    message: message.into(),
                },
                (start..end).into(),
            ))
            .into_iter()
        } else {
            None.into_iter()
        }
    })
}

impl ast::Ast for TsAst {
    type Vocab<'a> = TsVocabBlock<'a>;
    type Theory<'a> = TsTheoryBlock<'a>;
    type Structure<'a> = TsStructureBlock<'a>;
    type Procedure<'a> = TsProcedure<'a>;
    type VocabAst = TsVocabAst;
    type TheoryAst = TsTheoryAst;
    type StructureAst = TsStructureAst;

    fn iter_decls(&self) -> impl Iterator<Item = ast::AstBlock<'_, Self>> {
        NamedChildrenIter::new(&self.0.root_node()).filter_map(|f| {
            match FodotSymbols::from(f.kind_id()) {
                FodotSymbols::SymBlockVoc => {
                    Some(ast::Block::Vocab(TsVocabBlock::new_unchecked(f)))
                }
                FodotSymbols::SymBlockTheory => {
                    Some(ast::Block::Theory(TsTheoryBlock::new_unchecked(f)))
                }
                FodotSymbols::SymBlockStructure => {
                    Some(ast::Block::Structure(TsStructureBlock::new_unchecked(f)))
                }
                FodotSymbols::SymProcedureBlock => {
                    Some(ast::Block::Procedure(TsProcedure::new(f)?))
                }
                FodotSymbols::SymComment => None,
                _ => None,
            }
        })
    }

    fn parse_errors(&self) -> impl Iterator<Item = (ast::ParseError, Span)> {
        get_errors(self.0.root_node())
    }
}

pub struct TsVocabAst(tree_sitter::Tree);

impl TsVocabAst {
    fn get_root(&self) -> tree_sitter::Node<'_> {
        self.0.root_node_with_offset(
            // Uses C unsigned addition behaviour to have a 'negative' offset.
            // Any node before the prefix will have a nonsensical offset though + unsure if
            // tree-sitter will always have this behaviour...
            // Oh well good tests should catch this behaviour change.
            const { usize::MAX - PREFIX_VOCAB_DECL_PARSE.len() + 1 },
            tree_sitter::Point::new(0, 0),
        )
    }
}

impl VocabAst for TsVocabAst {
    type Decls<'a> = TsVocabDecls<'a>;

    fn decls(&self) -> Self::Decls<'_> {
        let source_file = self.get_root();
        TsVocabBlock::new_unchecked(source_file.child(0).unwrap()).decls()
    }

    fn parse_errors(&self) -> impl Iterator<Item = (ParseError, Span)> {
        get_decl_errors(self.get_root(), "invalid vocab declarations")
    }
}

pub struct TsTheoryAst(tree_sitter::Tree);

impl TsTheoryAst {
    fn get_root(&self) -> tree_sitter::Node<'_> {
        self.0.root_node_with_offset(
            // Uses C unsigned addition behaviour to have a 'negative' offset.
            // Any node before the prefix will have a nonsensical offset though + unsure if
            // tree-sitter will always have this behaviour...
            // Oh well good tests should catch this behaviour change.
            const { usize::MAX - PREFIX_THEORY_DECL_PARSE.len() + 1 },
            tree_sitter::Point::new(0, 0),
        )
    }
}

impl TheoryAst for TsTheoryAst {
    type Decls<'a> = TsTheoryDecls<'a>;

    fn decls(&self) -> Self::Decls<'_> {
        let source_file = self.get_root();
        TsTheoryBlock::new_unchecked(source_file.child(0).unwrap()).decls()
    }

    fn parse_errors(&self) -> impl Iterator<Item = (ParseError, Span)> {
        get_decl_errors(self.get_root(), "invalid theory declarations")
    }
}

pub struct TsStructureAst(tree_sitter::Tree);

impl TsStructureAst {
    fn get_root(&self) -> tree_sitter::Node<'_> {
        self.0.root_node_with_offset(
            // Uses C unsigned addition behaviour to have a 'negative' offset.
            // Any node before the prefix will have a nonsensical offset though + unsure if
            // tree-sitter will always have this behaviour...
            // Oh well good tests should catch this behaviour change.
            const { usize::MAX - PREFIX_STRUCTURE_DECL_PARSE.len() + 1 },
            tree_sitter::Point::new(0, 0),
        )
    }
}

impl StructureAst for TsStructureAst {
    type Decls<'a> = TsStructureDecls<'a>;

    fn decls(&self) -> Self::Decls<'_> {
        let source_file = self.get_root();
        TsStructureBlock::new_unchecked(source_file.child(0).unwrap()).decls()
    }

    fn parse_errors(&self) -> impl Iterator<Item = (ParseError, Span)> {
        get_decl_errors(self.get_root(), "invalid structure declarations")
    }
}

pub struct TsVocabBlock<'a>(Node<'a>);

impl<'a> TsVocabBlock<'a> {
    fn new_unchecked(node: Node<'a>) -> Self {
        debug_assert!(Self::new(node).is_some());
        Self(node)
    }

    fn new(node: Node<'a>) -> Option<Self> {
        use FodotSymbols as F;
        match FodotSymbols::from(node.kind_id()) {
            F::SymBlockVoc => Some(Self(node)),
            _ => None,
        }
    }
}

impl Spanned for TsVocabBlock<'_> {
    fn span(&self) -> Span {
        Span::from(self.0.start_byte()..self.0.end_byte())
    }
}

impl<'a> VocabBlock for TsVocabBlock<'a> {
    type Decls = TsVocabDecls<'a>;

    fn keyword_span(&self) -> Span {
        let keyword = self.0.child(0).unwrap();
        (keyword.start_byte()..keyword.end_byte()).into()
    }

    fn name(&self) -> Option<Span> {
        self.0
            .child_by_field_id(FodotFields::Name.into())
            .map(|name| Span::from(name.start_byte()..name.end_byte()))
    }

    fn decls(&self) -> Self::Decls {
        TsVocabDecls::new_unchecked(self.0)
    }
}

pub struct TsVocabDecls<'a>(Node<'a>);

impl<'a> TsVocabDecls<'a> {
    fn new_unchecked(node: Node<'a>) -> Self {
        debug_assert!(Self::new(node).is_some());
        Self(node)
    }

    fn new(node: Node<'a>) -> Option<Self> {
        use FodotSymbols as F;
        match FodotSymbols::from(node.kind_id()) {
            F::SymBlockVoc => Some(Self(node)),
            _ => None,
        }
    }
}

impl<'a> VocabDecls for TsVocabDecls<'a> {
    type Type = TsTypeDecl<'a>;
    type Pfunc = TsPfuncDecl<'a>;

    fn iter_decls(&self) -> impl Iterator<Item = Declaration<Self::Type, Self::Pfunc>> + '_ {
        use FodotSymbols as F;
        FieldChildrenIter::new(&self.0, FodotFields::Declaration.into()).filter_map(|decl| {
            match F::from(decl.kind_id()) {
                F::SymTypeDeclaration => Some(Declaration::Type(TsTypeDecl::new(decl)?)),
                F::SymPfuncDeclaration => Some(Declaration::Pfunc(TsPfuncDecl::new(decl)?)),
                _ => unreachable!(),
            }
        })
    }
}

pub struct TsTypeDecl<'a>(Node<'a>);

impl<'a> TsTypeDecl<'a> {
    #[allow(unused)]
    fn new_unchecked(node: Node<'a>) -> Self {
        debug_assert!(Self::new(node).is_some());
        Self(node)
    }

    #[allow(unused)]
    fn new(node: Node<'a>) -> Option<Self> {
        use FodotSymbols as F;
        match FodotSymbols::from(node.kind_id()) {
            F::SymTypeDeclaration => {
                if node
                    .child_by_field_id(FodotFields::Name.into())
                    .map(|f| f.is_error())
                    .unwrap_or(true)
                {
                    return None;
                }
                Some(Self(node))
            }
            _ => None,
        }
    }
}

impl Spanned for TsTypeDecl<'_> {
    fn span(&self) -> Span {
        Span::from(self.0.start_byte()..self.0.end_byte())
    }
}

impl<'a> TypeDeclaration for TsTypeDecl<'a> {
    type Enumeration = TsEnumeration<'a>;

    fn name(&self) -> Span {
        let name = self.0.child_by_field_id(FodotFields::Name.into()).unwrap();
        (name.start_byte()..name.end_byte()).into()
    }

    fn supertype(&self) -> Option<Span> {
        self.0
            .child_by_field_id(FodotFields::Subset.into())
            .map(|f| (f.start_byte()..f.end_byte()).into())
    }

    fn enumeration(&self) -> Option<TsEnumeration<'a>> {
        self.0
            .child_by_field_id(FodotFields::Interpretation.into())
            .and_then(TsEnumeration::new)
    }
}

pub struct TsPfuncDecl<'a>(Node<'a>);

impl<'a> TsPfuncDecl<'a> {
    #[allow(unused)]
    fn new_unchecked(node: Node<'a>) -> Self {
        debug_assert!(Self::new(node).is_some());
        Self(node)
    }

    #[allow(unused)]
    fn new(node: Node<'a>) -> Option<Self> {
        use FodotSymbols as F;
        match FodotSymbols::from(node.kind_id()) {
            F::SymPfuncDeclaration => Some(Self(node)),
            _ => None,
        }
    }
}

impl Spanned for TsPfuncDecl<'_> {
    fn span(&self) -> Span {
        Span::from(self.0.start_byte()..self.0.end_byte())
    }
}

impl PfuncDeclaration for TsPfuncDecl<'_> {
    fn names(&self) -> impl Iterator<Item = Span> + '_ {
        FieldChildrenIter::new(
            &self.0.child_by_field_id(FodotFields::Names.into()).unwrap(),
            FodotFields::Name.into(),
        )
        .map(|f| (f.start_byte()..f.end_byte()).into())
    }

    fn domain(&self) -> impl Iterator<Item = Span> + '_ {
        match self.0.child_by_field_id(FodotFields::Domain.into()) {
            Some(value) => FieldChildrenIter::new(&value, FodotFields::Name.into()),
            None => FieldChildrenIter::empty(self.0.walk()),
        }
        .map(|f| (f.start_byte()..f.end_byte()).into())
    }

    fn codomain(&self) -> MaybePoisoned<Span> {
        self.0
            .child_by_field_id(FodotFields::Codomain.into())
            .and_then(|codomain| {
                if !codomain.is_error() {
                    Some((codomain.start_byte()..codomain.end_byte()).into())
                } else {
                    None
                }
            })
            .into()
    }
}

pub struct TsTheoryBlock<'a>(Node<'a>);

impl<'a> TsTheoryBlock<'a> {
    fn new_unchecked(node: Node<'a>) -> Self {
        debug_assert!(Self::new(node).is_some());
        Self(node)
    }

    fn new(node: Node<'a>) -> Option<Self> {
        use FodotSymbols as F;
        match FodotSymbols::from(node.kind_id()) {
            F::SymBlockTheory => Some(Self(node)),
            _ => None,
        }
    }
}

impl Spanned for TsTheoryBlock<'_> {
    fn span(&self) -> Span {
        Span::from(self.0.start_byte()..self.0.end_byte())
    }
}

impl<'a> TheoryBlock for TsTheoryBlock<'a> {
    type Decls = TsTheoryDecls<'a>;

    fn keyword_span(&self) -> Span {
        let keyword = self.0.child(0).unwrap();
        (keyword.start_byte()..keyword.end_byte()).into()
    }

    fn names(&self) -> Option<ast::TheoryNames> {
        self.0
            .child_by_field_id(FodotFields::Name.into())
            .and_then(|name| {
                self.0
                    .child_by_field_id(FodotFields::VocabName.into())
                    .map(|vocab_name| TheoryNames {
                        theory_name: Span::from(name.start_byte()..name.end_byte()),
                        vocab_name: Span::from(vocab_name.start_byte()..vocab_name.end_byte()),
                    })
            })
    }

    fn decls(&self) -> Self::Decls {
        TsTheoryDecls::new_unchecked(self.0)
    }
}

pub struct TsTheoryDecls<'a>(Node<'a>);

impl<'a> TsTheoryDecls<'a> {
    fn new_unchecked(node: Node<'a>) -> Self {
        debug_assert!(Self::new(node).is_some());
        Self(node)
    }

    fn new(node: Node<'a>) -> Option<Self> {
        use FodotSymbols as F;
        match FodotSymbols::from(node.kind_id()) {
            F::SymBlockTheory => Some(Self(node)),
            _ => None,
        }
    }
}

impl<'a> TheoryDecls for TsTheoryDecls<'a> {
    type Expressions = TsExpressions<'a>;
    type Definition = TsDefinition<'a>;

    fn iter_decls(
        &self,
    ) -> impl Iterator<Item = ast::Assertion<Self::Expressions, Self::Definition>> {
        FieldChildrenIter::new(&self.0, FodotFields::Assertions.into())
            .filter_map(|f| to_assertion(f))
    }
}

pub struct TsExpressions<'a>(PhantomData<&'a ()>);

impl<'a> Expressions for TsExpressions<'a> {
    type BinaryOp = TsBinaryOp<'a>;
    type CmpOp = TsCmpOp<'a>;
    type UnaryOp = TsUnaryOp<'a>;
    type Variables = TsVariables<'a>;
    type Quantification = TsQuantification<'a>;
    type CountAgg = TsCountAgg<'a>;
    type SumAgg = TsSumAgg<'a>;
    type Ite = TsIte<'a>;
    type AppliedSymbol = TsAppliedSymbol<'a>;
    type InEnumeration = TsInEnumeration<'a>;
    type ConjuctiveGuard = TsConjuctiveGuard<'a>;
    type ImplicativeGuard = TsImplicativeGuard<'a>;
    type IfGuard = TsIfGuard<'a>;
    type IsEnumerated = TsIsEnumerated<'a>;
}

pub struct TsBinaryOp<'a>(Node<'a>);

impl<'a> TsBinaryOp<'a> {
    #[allow(unused)]
    fn new_unchecked(node: Node<'a>) -> Self {
        debug_assert!(Self::new(node).is_some());
        Self(node)
    }

    fn new(node: Node<'a>) -> Option<Self> {
        Self::construct(node).and_then(|f| f.left())
    }

    fn construct(node: Node<'a>) -> Option<Either<Self, TsCmpOp<'a>>> {
        use FodotSymbols as F;
        match FodotSymbols::from(node.kind_id()) {
            F::SymLand
            | F::SymLor
            | F::SymRimplication
            | F::SymLimplication
            | F::SymEquivalence
            | F::SymSum
            | F::SymSubtraction
            | F::SymMultiplication
            | F::SymDivision
            | F::SymRemainder => Some(Either::Left(Self(node))),
            F::SymEquality | F::SymGe | F::SymGeq | F::SymLe | F::SymLeq | F::SymInequality => {
                if let Some(value) = TsCmpOp::new(node) {
                    Some(Either::Right(value))
                } else {
                    Some(Either::Left(Self(node)))
                }
            }
            _ => None,
        }
    }

    fn get_kind(&self) -> BinaryOpKind {
        use FodotSymbols as F;
        match self.0.kind_id().into() {
            F::SymLand => BinaryOpKind::And,
            F::SymLor => BinaryOpKind::Or,
            F::SymRimplication => BinaryOpKind::Rimpl,
            F::SymLimplication => BinaryOpKind::Limpl,
            F::SymEquivalence => BinaryOpKind::Eqv,

            F::SymSum => BinaryOpKind::Sum,
            F::SymSubtraction => BinaryOpKind::Sub,
            F::SymMultiplication => BinaryOpKind::Mult,
            F::SymDivision => BinaryOpKind::Div,
            F::SymRemainder => BinaryOpKind::Rem,

            F::SymEquality => BinaryOpKind::Eq,
            F::SymGe => BinaryOpKind::Gt,
            F::SymGeq => BinaryOpKind::Ge,
            F::SymLe => BinaryOpKind::Lt,
            F::SymLeq => BinaryOpKind::Le,
            F::SymInequality => BinaryOpKind::Neq,
            _ => unreachable!(),
        }
    }
}

fn to_assertion(node: Node) -> Option<Assertion<TsExpressions, TsDefinition>> {
    if let Some(value) = to_expression(node) {
        Some(Assertion::Expr(value))
    } else {
        TsDefinition::new(node).map(Assertion::Def)
    }
}

fn to_expression(node: Node) -> Option<Expression<TsExpressions>> {
    if let Some(value) = TsBinaryOp::construct(node) {
        match value {
            Either::Left(value) => Some(Expression::BinOp(value)),
            Either::Right(value) => Some(Expression::CmpOp(value)),
        }
    } else if let Some(value) = TsUnaryOp::new(node) {
        Some(Expression::UnaryOp(value))
    } else if let Some(value) = TsQuantification::new(node) {
        Some(Expression::Quantification(value))
    } else if let Some(value) = TsCountAgg::new(node) {
        Some(Expression::Count(value))
    } else if let Some(value) = TsSumAgg::new(node) {
        Some(Expression::Sum(value))
    } else if let Some(value) = TsIte::new(node) {
        Some(Expression::Ite(value))
    } else if let Some(value) = TsAppliedSymbol::new(node) {
        Some(Expression::AppliedSymbol(value))
    } else if let Some(value) = TsInEnumeration::new(node) {
        Some(Expression::InEnumeration(value))
    } else if let Some(value) = TsConjuctiveGuard::new(node) {
        Some(Expression::ConjuctiveGuard(value))
    } else if let Some(value) = TsImplicativeGuard::new(node) {
        Some(Expression::ImplicativeGuard(value))
    } else if let Some(value) = TsIfGuard::new(node) {
        Some(Expression::IfGuard(value))
    } else if let Some(value) = TsIsEnumerated::new(node) {
        Some(Expression::IsEnumerated(value))
    } else {
        node_to_enum_elem(node).map(Expression::Element)
    }
}

fn unwrap_expression(node: Node) -> Expression<TsExpressions> {
    to_expression(node).unwrap()
}

fn error_or_expression(node: Node) -> Option<Expression<TsExpressions>> {
    if node.is_error() || node.is_missing() {
        return None;
    }
    Some(unwrap_expression(node))
}

impl Spanned for TsBinaryOp<'_> {
    fn span(&self) -> Span {
        Span::from(self.0.start_byte()..self.0.end_byte())
    }
}

impl<'a> BinaryOp for TsBinaryOp<'a> {
    type Formula = TsExpressions<'a>;

    fn lhs(&self) -> MaybePoisoned<Expression<Self::Formula>> {
        self.0
            .named_child_by_field_id(FodotFields::Lhs.into())
            .and_then(error_or_expression)
            .into()
    }

    fn rhs(&self) -> MaybePoisoned<Expression<Self::Formula>> {
        self.0
            .named_child_by_field_id(FodotFields::Rhs.into())
            .and_then(error_or_expression)
            .into()
    }

    fn binop_span(&self) -> Span {
        let bin_op = self.0.child_by_field_id(FodotFields::BinOp.into()).unwrap();
        (bin_op.start_byte()..bin_op.end_byte()).into()
    }

    fn kind(&self) -> BinaryOpKind {
        self.get_kind()
    }
}

pub struct TsCmpOp<'a>(Node<'a>);

impl<'a> TsCmpOp<'a> {
    #[allow(unused)]
    fn new_unchecked(node: Node<'a>) -> Self {
        debug_assert!(Self::new(node).is_some());
        Self(node)
    }

    fn new(node: Node<'a>) -> Option<Self> {
        use FodotSymbols as F;
        match FodotSymbols::from(node.kind_id()) {
            F::SymEquality | F::SymGe | F::SymGeq | F::SymLe | F::SymLeq | F::SymInequality => {
                let this = Self(node);
                if this.next_rhs_with_next().1.is_some() {
                    Some(this)
                } else {
                    None
                }
            }
            _ => None,
        }
    }

    fn new_half_assed(node: Node<'a>) -> Option<Self> {
        use FodotSymbols as F;
        match FodotSymbols::from(node.kind_id()) {
            F::SymEquality | F::SymGe | F::SymGeq | F::SymLe | F::SymLeq | F::SymInequality => {
                Some(Self(node))
            }
            _ => None,
        }
    }

    fn kind(&self) -> CmpOpKind {
        node_cmp_op(&self.0).unwrap()
    }

    fn next_rhs_with_next(&self) -> (MaybePoisoned<Expression<TsExpressions<'a>>>, Option<Self>) {
        self.0
            .child_by_field_id(FodotFields::Rhs.into())
            .and_then(|f| {
                self.0
                    .named_child_by_field_id(FodotFields::Rhs.into())
                    .map(|d| (f, d))
            })
            .map(|(outer, named)| {
                // There does not seem to be a better way to do this.
                if FodotSymbols::from(outer.kind_id()) == FodotSymbols::AnonSymLPAREN {
                    (Some(named), None)
                } else if let Some(value) = Self::new_half_assed(named) {
                    (
                        value.0.named_child_by_field_id(FodotFields::Lhs.into()),
                        Some(value),
                    )
                } else {
                    (Some(named), None)
                }
            })
            .map(|f| (MaybePoisoned::from(f.0.and_then(to_expression)), f.1))
            .unwrap_or((MaybePoisoned::Poisoned, None))
    }

    fn next_rhs(&self) -> MaybePoisoned<Expression<TsExpressions<'a>>> {
        self.next_rhs_with_next().0
    }
}

fn node_cmp_op(node: &tree_sitter::Node) -> Option<CmpOpKind> {
    use FodotSymbols as F;
    match node.kind_id().into() {
        F::SymEquality => Some(CmpOpKind::Eq),
        F::SymGe => Some(CmpOpKind::Gt),
        F::SymGeq => Some(CmpOpKind::Ge),
        F::SymLe => Some(CmpOpKind::Lt),
        F::SymLeq => Some(CmpOpKind::Le),
        F::SymInequality => Some(CmpOpKind::Neq),
        _ => None,
    }
}

impl Spanned for TsCmpOp<'_> {
    fn span(&self) -> Span {
        Span::from(self.0.start_byte()..self.0.end_byte())
    }
}

impl<'a> CmpOp for TsCmpOp<'a> {
    type Formula = TsExpressions<'a>;

    fn first(
        &self,
    ) -> (
        MaybePoisoned<Expression<Self::Formula>>,
        CmpOpKind,
        MaybePoisoned<Expression<Self::Formula>>,
    ) {
        let child_lhs = MaybePoisoned::from(
            self.0
                .named_child_by_field_id(FodotFields::Lhs.into())
                .and_then(to_expression),
        );
        let kind = self.kind();
        let child_rhs = self.next_rhs();
        (child_lhs, kind, child_rhs)
    }

    fn rest(&self) -> impl Iterator<Item = (CmpOpKind, Expression<Self::Formula>)> {
        TsCmpOpsIterator {
            cur: self.next_rhs_with_next().1,
        }
    }
}

pub struct TsCmpOpsIterator<'a> {
    cur: Option<TsCmpOp<'a>>,
}

impl<'a> Iterator for TsCmpOpsIterator<'a> {
    type Item = (CmpOpKind, Expression<TsExpressions<'a>>);

    fn next(&mut self) -> Option<Self::Item> {
        loop {
            if let Some(this_cur) = &mut self.cur {
                let (child_rhs, next_cur) = this_cur.next_rhs_with_next();
                let kind = this_cur.kind();
                self.cur = next_cur;
                match child_rhs {
                    MaybePoisoned::Value(value) => return Some((kind, value)),
                    _ => continue,
                }
            }
            return None;
        }
    }
}

pub struct TsVariables<'a>(Node<'a>);

impl<'a> TsVariables<'a> {
    fn new(node: Node<'a>) -> Option<Self> {
        match FodotSymbols::from(node.kind_id()) {
            FodotSymbols::SymQuantification => Some(Self(node)),
            _ => None,
        }
    }
}

impl Spanned for TsVariables<'_> {
    fn span(&self) -> Span {
        Span::from(self.0.start_byte()..self.0.end_byte())
    }
}

impl Variables for TsVariables<'_> {
    fn vars(&self) -> impl Iterator<Item = Span> + '_ {
        FieldChildrenIter::new(&self.0, FodotFields::Variable.into())
            .map(|f| (f.start_byte()..f.end_byte()).into())
    }

    fn var_type(&self) -> MaybePoisoned<Span> {
        let type_ = self.0.child_by_field_id(FodotFields::Type.into()).unwrap();
        if type_.is_error() || type_.is_missing() {
            None.into()
        } else {
            Some((type_.start_byte()..type_.end_byte()).into()).into()
        }
    }
}

pub struct TsQuantification<'a>(Node<'a>);

impl<'a> TsQuantification<'a> {
    #[allow(unused)]
    fn new_unchecked(node: Node<'a>) -> Self {
        debug_assert!(Self::new(node).is_some());
        Self(node)
    }

    fn new(node: Node<'a>) -> Option<Self> {
        match FodotSymbols::from(node.kind_id()) {
            FodotSymbols::SymUniversal | FodotSymbols::SymExistential => Some(Self(node)),
            _ => None,
        }
    }
}

impl Spanned for TsQuantification<'_> {
    fn span(&self) -> Span {
        Span::from(self.0.start_byte()..self.0.end_byte())
    }
}

impl<'a> Quantification for TsQuantification<'a> {
    type Formula = TsExpressions<'a>;

    fn kind(&self) -> QuantificationKind {
        match self.0.kind_id().into() {
            FodotSymbols::SymUniversal => QuantificationKind::Universal,
            FodotSymbols::SymExistential => QuantificationKind::Existential,
            _ => unreachable!(),
        }
    }

    fn kind_span(&self) -> Span {
        let uni_span = self.0.child_by_field_id(FodotFields::Kind.into()).unwrap();
        (uni_span.start_byte()..uni_span.end_byte()).into()
    }

    fn variables(&self) -> impl Iterator<Item = <Self::Formula as Expressions>::Variables> + '_ {
        self.0
            .child_by_field_id(FodotFields::Variables.into())
            .map(|f| FieldChildrenIter::new(&f, FodotFields::VariableGroup.into()))
            .unwrap_or_else(|| FieldChildrenIter::empty(self.0.walk()))
            .filter_map(TsVariables::new)
    }

    fn subformula(&self) -> MaybePoisoned<Expression<Self::Formula>> {
        self.0
            .named_child_by_field_id(FodotFields::Subformula.into())
            .and_then(error_or_expression)
            .into()
    }
}

pub struct TsCountAgg<'a>(Node<'a>);

impl<'a> TsCountAgg<'a> {
    #[allow(unused)]
    fn new_unchecked(node: Node<'a>) -> Self {
        debug_assert!(Self::new(node).is_some());
        Self(node)
    }

    fn new(node: Node<'a>) -> Option<Self> {
        match FodotSymbols::from(node.kind_id()) {
            FodotSymbols::SymCount => Some(Self(node)),
            _ => None,
        }
    }
}

impl Spanned for TsCountAgg<'_> {
    fn span(&self) -> Span {
        Span::from(self.0.start_byte()..self.0.end_byte())
    }
}

impl<'a> CountAgg for TsCountAgg<'a> {
    type Formula = TsExpressions<'a>;

    fn variables(&self) -> impl Iterator<Item = <Self::Formula as Expressions>::Variables> + '_ {
        self.0
            .child_by_field_id(FodotFields::Variables.into())
            .map(|f| FieldChildrenIter::new(&f, FodotFields::VariableGroup.into()))
            .unwrap_or_else(|| FieldChildrenIter::empty(self.0.walk()))
            .filter_map(TsVariables::new)
    }

    fn subformula(&self) -> MaybePoisoned<Expression<Self::Formula>> {
        self.0
            .named_child_by_field_id(FodotFields::Subformula.into())
            .and_then(error_or_expression)
            .into()
    }
}

pub struct TsSumAgg<'a>(Node<'a>);

impl<'a> TsSumAgg<'a> {
    #[allow(unused)]
    fn new_unchecked(node: Node<'a>) -> Self {
        debug_assert!(Self::new(node).is_some());
        Self(node)
    }

    fn new(node: Node<'a>) -> Option<Self> {
        match FodotSymbols::from(node.kind_id()) {
            FodotSymbols::SymSumAgg => Some(Self(node)),
            _ => None,
        }
    }
}

impl Spanned for TsSumAgg<'_> {
    fn span(&self) -> Span {
        Span::from(self.0.start_byte()..self.0.end_byte())
    }
}

impl<'a> SumAgg for TsSumAgg<'a> {
    type Formula = TsExpressions<'a>;

    fn variables(&self) -> impl Iterator<Item = <Self::Formula as Expressions>::Variables> + '_ {
        self.0
            .child_by_field_id(FodotFields::Variables.into())
            .map(|f| FieldChildrenIter::new(&f, FodotFields::VariableGroup.into()))
            .unwrap_or_else(|| FieldChildrenIter::empty(self.0.walk()))
            .filter_map(TsVariables::new)
    }

    fn term(&self) -> MaybePoisoned<Expression<Self::Formula>> {
        self.0
            .named_child_by_field_id(FodotFields::SetTerm.into())
            .and_then(error_or_expression)
            .into()
    }

    fn subformula(&self) -> MaybePoisoned<Expression<Self::Formula>> {
        self.0
            .named_child_by_field_id(FodotFields::SetCondition.into())
            .and_then(error_or_expression)
            .into()
    }
}

pub struct TsIte<'a>(Node<'a>);

impl<'a> TsIte<'a> {
    #[allow(unused)]
    fn new_unchecked(node: Node<'a>) -> Self {
        debug_assert!(Self::new(node).is_some());
        Self(node)
    }

    fn new(node: Node<'a>) -> Option<Self> {
        match FodotSymbols::from(node.kind_id()) {
            FodotSymbols::SymIte => Some(Self(node)),
            _ => None,
        }
    }
}

impl Spanned for TsIte<'_> {
    fn span(&self) -> Span {
        Span::from(self.0.start_byte()..self.0.end_byte())
    }
}

impl<'a> Ite for TsIte<'a> {
    type Formula = TsExpressions<'a>;

    fn if_formula(&self) -> MaybePoisoned<Expression<Self::Formula>> {
        self.0
            .named_child_by_field_id(FodotFields::Cond.into())
            .and_then(error_or_expression)
            .into()
    }

    fn then_term(&self) -> MaybePoisoned<Expression<Self::Formula>> {
        self.0
            .named_child_by_field_id(FodotFields::Then.into())
            .and_then(error_or_expression)
            .into()
    }

    fn else_term(&self) -> MaybePoisoned<Expression<Self::Formula>> {
        self.0
            .named_child_by_field_id(FodotFields::Else.into())
            .and_then(error_or_expression)
            .into()
    }
}

pub struct TsAppliedSymbol<'a>(Node<'a>);

impl<'a> TsAppliedSymbol<'a> {
    #[allow(unused)]
    fn new_unchecked(node: Node<'a>) -> Self {
        debug_assert!(Self::new(node).is_some());
        Self(node)
    }

    fn new(node: Node<'a>) -> Option<Self> {
        match FodotSymbols::from(node.kind_id()) {
            FodotSymbols::SymAppliedSymbol => Some(Self(node)),
            _ => None,
        }
    }
}

impl Spanned for TsAppliedSymbol<'_> {
    fn span(&self) -> Span {
        Span::from(self.0.start_byte()..self.0.end_byte())
    }
}

impl<'a> AppliedSymbol for TsAppliedSymbol<'a> {
    type Formula = TsExpressions<'a>;

    fn name(&self) -> Span {
        let name = self.0.child_by_field_id(FodotFields::Name.into()).unwrap();
        Span::from(name.start_byte()..name.end_byte())
    }

    fn args_len(&self) -> usize {
        self.0.named_child_count() - 1
    }

    fn args(&self) -> impl Iterator<Item = Expression<Self::Formula>> {
        FieldChildrenIter::new(&self.0, FodotFields::Args.into()).filter_map(to_expression)
    }
}

pub struct TsUnaryOp<'a>(Node<'a>);

impl<'a> TsUnaryOp<'a> {
    #[allow(unused)]
    fn new_unchecked(node: Node<'a>) -> Self {
        debug_assert!(Self::new(node).is_some());
        Self(node)
    }

    fn new(node: Node<'a>) -> Option<Self> {
        match FodotSymbols::from(node.kind_id()) {
            FodotSymbols::SymNeg | FodotSymbols::SymNumericalNeg => Some(Self(node)),
            _ => None,
        }
    }
}

impl Spanned for TsUnaryOp<'_> {
    fn span(&self) -> Span {
        Span::from(self.0.start_byte()..self.0.end_byte())
    }
}

impl<'a> UnaryOp for TsUnaryOp<'a> {
    type Formula = TsExpressions<'a>;

    fn subformula(&self) -> MaybePoisoned<Expression<Self::Formula>> {
        self.0
            .named_child_by_field_id(FodotFields::Subformula.into())
            .and_then(error_or_expression)
            .into()
    }

    fn kind(&self) -> ast::UnaryOpKind {
        match FodotSymbols::from(self.0.kind_id()) {
            FodotSymbols::SymNeg => ast::UnaryOpKind::Negation,
            FodotSymbols::SymNumericalNeg => ast::UnaryOpKind::NumericNegation,
            _ => unreachable!(),
        }
    }
}

pub struct TsDefinition<'a>(Node<'a>);

impl<'a> TsDefinition<'a> {
    #[allow(unused)]
    fn new_unchecked(node: Node<'a>) -> Self {
        debug_assert!(Self::new(node).is_some());
        Self(node)
    }

    fn new(node: Node<'a>) -> Option<Self> {
        match FodotSymbols::from(node.kind_id()) {
            FodotSymbols::SymDefinition => Some(Self(node)),
            _ => None,
        }
    }
}

impl Spanned for TsDefinition<'_> {
    fn span(&self) -> Span {
        Span::from(self.0.start_byte()..self.0.end_byte())
    }
}

impl<'a> Definition for TsDefinition<'a> {
    type Formula = TsExpressions<'a>;
    type Rule = TsDefinitionalRule<'a>;

    fn rules(&self) -> impl Iterator<Item = Self::Rule> {
        FieldChildrenIter::new(&self.0, FodotFields::Rule.into())
            .map(TsDefinitionalRule::new_unchecked)
    }
}

pub struct TsDefinitionalRule<'a>(Node<'a>);

impl<'a> TsDefinitionalRule<'a> {
    fn new_unchecked(node: Node<'a>) -> Self {
        debug_assert!(Self::new(node).is_some());
        Self(node)
    }

    fn new(node: Node<'a>) -> Option<Self> {
        match FodotSymbols::from(node.kind_id()) {
            FodotSymbols::SymDefinitionalRule => Some(Self(node)),
            _ => None,
        }
    }
}

impl Spanned for TsDefinitionalRule<'_> {
    fn span(&self) -> Span {
        Span::from(self.0.start_byte()..self.0.end_byte())
    }
}

impl<'a> DefinitionalRule for TsDefinitionalRule<'a> {
    type Formula = TsExpressions<'a>;

    fn head(&self) -> MaybePoisoned<Expression<Self::Formula>> {
        self.0
            .named_child_by_field_id(FodotFields::Head.into())
            .and_then(error_or_expression)
            .into()
    }

    fn body(&self) -> MaybePoisoned<Expression<Self::Formula>> {
        self.0
            .named_child_by_field_id(FodotFields::Body.into())
            .and_then(error_or_expression)
            .into()
    }
}

pub struct TsInEnumeration<'a>(Node<'a>);

impl<'a> TsInEnumeration<'a> {
    #[allow(unused)]
    fn new_unchecked(node: Node<'a>) -> Self {
        debug_assert!(Self::new(node).is_some());
        Self(node)
    }

    fn new(node: Node<'a>) -> Option<Self> {
        match FodotSymbols::from(node.kind_id()) {
            FodotSymbols::SymInSet => Some(Self(node)),
            _ => None,
        }
    }
}

impl Spanned for TsInEnumeration<'_> {
    fn span(&self) -> Span {
        Span::from(self.0.start_byte()..self.0.end_byte())
    }
}

impl<'a> InEnumeration for TsInEnumeration<'a> {
    type Formula = TsExpressions<'a>;

    fn expr(&self) -> MaybePoisoned<Expression<Self::Formula>> {
        self.0
            .named_child_by_field_id(FodotFields::Expr.into())
            .and_then(error_or_expression)
            .into()
    }

    fn enumeration(&self) -> impl Iterator<Item = Expression<Self::Formula>> {
        FieldChildrenIter::new(&self.0, FodotFields::Enumeration.into())
            .filter_map(|f| {
                // This is needed for brackets and other nodes hidden in the ast.
                if !f.is_named() {
                    f.named_child(0)
                } else {
                    Some(f)
                }
            })
            .filter_map(error_or_expression)
    }
}

pub struct TsConjuctiveGuard<'a>(Node<'a>);

impl<'a> TsConjuctiveGuard<'a> {
    #[allow(unused)]
    fn new_unchecked(node: Node<'a>) -> Self {
        debug_assert!(Self::new(node).is_some());
        Self(node)
    }

    fn new(node: Node<'a>) -> Option<Self> {
        match FodotSymbols::from(node.kind_id()) {
            FodotSymbols::SymConjuctiveGuard => Some(Self(node)),
            _ => None,
        }
    }
}

impl Spanned for TsConjuctiveGuard<'_> {
    fn span(&self) -> Span {
        Span::from(self.0.start_byte()..self.0.end_byte())
    }
}

impl<'a> ConjuctiveGuard for TsConjuctiveGuard<'a> {
    type Formula = TsExpressions<'a>;

    fn subformula(&self) -> MaybePoisoned<Expression<Self::Formula>> {
        self.0
            .child_by_field_id(FodotFields::Subformula.into())
            .and_then(to_expression)
            .into()
    }
}

pub struct TsImplicativeGuard<'a>(Node<'a>);

impl<'a> TsImplicativeGuard<'a> {
    #[allow(unused)]
    fn new_unchecked(node: Node<'a>) -> Self {
        debug_assert!(Self::new(node).is_some());
        Self(node)
    }

    fn new(node: Node<'a>) -> Option<Self> {
        match FodotSymbols::from(node.kind_id()) {
            FodotSymbols::SymImplicativeGuard => Some(Self(node)),
            _ => None,
        }
    }
}

impl Spanned for TsImplicativeGuard<'_> {
    fn span(&self) -> Span {
        Span::from(self.0.start_byte()..self.0.end_byte())
    }
}

impl<'a> ImplicativeGuard for TsImplicativeGuard<'a> {
    type Formula = TsExpressions<'a>;

    fn subformula(&self) -> MaybePoisoned<Expression<Self::Formula>> {
        self.0
            .child_by_field_id(FodotFields::Subformula.into())
            .and_then(to_expression)
            .into()
    }
}

pub struct TsIfGuard<'a>(Node<'a>);

impl<'a> TsIfGuard<'a> {
    #[allow(unused)]
    fn new_unchecked(node: Node<'a>) -> Self {
        debug_assert!(Self::new(node).is_some());
        Self(node)
    }

    fn new(node: Node<'a>) -> Option<Self> {
        match FodotSymbols::from(node.kind_id()) {
            FodotSymbols::SymIfGuard => Some(Self(node)),
            _ => None,
        }
    }
}

impl Spanned for TsIfGuard<'_> {
    fn span(&self) -> Span {
        Span::from(self.0.start_byte()..self.0.end_byte())
    }
}

impl<'a> IfGuard for TsIfGuard<'a> {
    type Formula = TsExpressions<'a>;

    fn term(&self) -> MaybePoisoned<Expression<Self::Formula>> {
        self.0
            .named_child_by_field_id(FodotFields::Subformula.into())
            .and_then(to_expression)
            .into()
    }

    fn else_term(&self) -> MaybePoisoned<Expression<Self::Formula>> {
        self.0
            .named_child_by_field_id(FodotFields::Else.into())
            .and_then(to_expression)
            .into()
    }
}

pub struct TsIsEnumerated<'a>(Node<'a>);

impl<'a> TsIsEnumerated<'a> {
    #[allow(unused)]
    fn new_unchecked(node: Node<'a>) -> Self {
        debug_assert!(Self::new(node).is_some());
        Self(node)
    }

    fn new(node: Node<'a>) -> Option<Self> {
        match FodotSymbols::from(node.kind_id()) {
            FodotSymbols::SymIsEnumerated => Some(Self(node)),
            _ => None,
        }
    }
}

impl Spanned for TsIsEnumerated<'_> {
    fn span(&self) -> Span {
        Span::from(self.0.start_byte()..self.0.end_byte())
    }
}

impl<'a> ast::IsEnumerated for TsIsEnumerated<'a> {
    type Formula = TsExpressions<'a>;

    fn applied_symbol(&self) -> MaybePoisoned<<Self::Formula as Expressions>::AppliedSymbol> {
        self.0
            .child_by_field_id(FodotFields::AppliedSymbol.into())
            .and_then(TsAppliedSymbol::new)
            .into()
    }
}

pub struct TsStructureBlock<'a>(Node<'a>);

impl<'a> TsStructureBlock<'a> {
    fn new_unchecked(node: Node<'a>) -> Self {
        debug_assert!(Self::new(node).is_some());
        Self(node)
    }

    fn new(node: Node<'a>) -> Option<Self> {
        match FodotSymbols::from(node.kind_id()) {
            FodotSymbols::SymBlockStructure => Some(Self(node)),
            _ => None,
        }
    }
}

impl Spanned for TsStructureBlock<'_> {
    fn span(&self) -> Span {
        Span::from(self.0.start_byte()..self.0.end_byte())
    }
}

impl<'a> ast::StructureBlock for TsStructureBlock<'a> {
    type Decls = TsStructureDecls<'a>;

    fn keyword_span(&self) -> Span {
        let keyword = self.0.child(0).unwrap();
        (keyword.start_byte()..keyword.end_byte()).into()
    }

    fn names(&self) -> Option<ast::StructureNames> {
        self.0
            .child_by_field_id(FodotFields::Name.into())
            .and_then(|name| {
                self.0
                    .child_by_field_id(FodotFields::VocabName.into())
                    .map(|vocab_name| StructureNames {
                        structure_name: Span::from(name.start_byte()..name.end_byte()),
                        vocab_name: Span::from(vocab_name.start_byte()..vocab_name.end_byte()),
                    })
            })
    }

    fn decls(&self) -> Self::Decls {
        TsStructureDecls::new_unchecked(self.0)
    }
}

pub struct TsStructureDecls<'a>(Node<'a>);

impl<'a> TsStructureDecls<'a> {
    fn new_unchecked(node: Node<'a>) -> Self {
        debug_assert!(Self::new(node).is_some());
        Self(node)
    }

    fn new(node: Node<'a>) -> Option<Self> {
        match FodotSymbols::from(node.kind_id()) {
            FodotSymbols::SymBlockStructure => Some(Self(node)),
            _ => None,
        }
    }
}

impl<'a> ast::StructureDecls for TsStructureDecls<'a> {
    type Interp = TsSymbolInterpretation<'a>;

    fn interpretations(&self) -> impl Iterator<Item = Self::Interp> {
        FieldChildrenIter::new(&self.0, FodotFields::Interpretation.into())
            .filter_map(TsSymbolInterpretation::new)
    }
}

pub struct TsTuple<'a>(Node<'a>);

impl<'a> TsTuple<'a> {
    fn new_unchecked(node: Node<'a>) -> Self {
        debug_assert!(Self::new(node).is_some());
        Self(node)
    }

    fn new(node: Node<'a>) -> Option<Self> {
        match FodotSymbols::from(node.kind_id()) {
            FodotSymbols::SymTuple => Some(Self(node)),
            _ => None,
        }
    }
}

fn node_to_enum_elem(node: Node) -> Option<Element> {
    match FodotSymbols::from(node.kind_id()) {
        FodotSymbols::SymInt => Some(Element::Int((node.start_byte()..node.end_byte()).into())),
        FodotSymbols::SymReal | FodotSymbols::SymFraction => {
            Some(Element::Real((node.start_byte()..node.end_byte()).into()))
        }
        FodotSymbols::Symstring | FodotSymbols::AliasSymString => {
            Some(Element::String((node.start_byte()..node.end_byte()).into()))
        }
        FodotSymbols::SymExtString => {
            let inner = node.child(1).unwrap();
            Some(Element::String(
                (inner.start_byte()..inner.end_byte()).into(),
            ))
        }
        _ => None,
    }
}

fn node_to_range_elem(node: Node) -> Option<EnumerationRange> {
    match FodotSymbols::from(node.kind_id()) {
        FodotSymbols::SymRange => {
            let start = node.child_by_field_id(FodotFields::RangeStart.into())?;
            let end = node.child_by_field_id(FodotFields::RangeEnd.into())?;
            Some(EnumerationRange {
                start: Span::from(start.start_byte()..start.end_byte()),
                end: Span::from(end.start_byte()..end.end_byte()),
            })
        }
        _ => None,
    }
}

fn unwrap_node_to_enum_elem(node: Node) -> Element {
    node_to_enum_elem(node).unwrap()
}

impl Spanned for TsTuple<'_> {
    fn span(&self) -> Span {
        Span::from(self.0.start_byte()..self.0.end_byte())
    }
}

impl ast::Tuple for TsTuple<'_> {
    fn get(&self, index: usize) -> Option<Element> {
        FieldChildrenIter::new(&self.0, FodotFields::Element.into())
            .nth(index)
            .map(unwrap_node_to_enum_elem)
    }

    fn len(&self) -> usize {
        self.0.named_child_count()
    }

    fn is_empty(&self) -> bool {
        self.0.named_child_count() == 0
    }

    fn values(&self) -> impl Iterator<Item = Element> + '_ {
        FieldChildrenIter::new(&self.0, FodotFields::Element.into()).map(unwrap_node_to_enum_elem)
    }
}

pub struct TsSymbolInterpretation<'a>(Node<'a>);

impl<'a> TsSymbolInterpretation<'a> {
    fn new(node: Node<'a>) -> Option<Self> {
        if node.has_error() {
            return None;
        }
        match FodotSymbols::from(node.kind_id()) {
            FodotSymbols::SymSymbolInterpretation => Some(Self(node)),
            _ => None,
        }
    }
}

impl Spanned for TsSymbolInterpretation<'_> {
    fn span(&self) -> Span {
        Span::from(self.0.start_byte()..self.0.end_byte())
    }
}

impl<'a> SymbolInterpretation for TsSymbolInterpretation<'a> {
    type Tuple = TsTuple<'a>;
    type Enumeration = TsEnumerationInterpretation<'a>;

    fn name(&self) -> Span {
        let node = self
            .0
            .child_by_field_id(FodotFields::Symbol.into())
            .unwrap();
        Span::from(node.start_byte()..node.end_byte())
    }

    fn interpretation_kind(&self) -> ast::InterpKind {
        let kind = self.0.child_by_field_id(FodotFields::Kind.into()).unwrap();
        match kind.kind_id().into() {
            // :>
            FodotSymbols::AnonSymCOLONGT |
                // ⊇
                FodotSymbols::AnonSymU2287 => ast::InterpKind::Partial,
            // :=
            FodotSymbols::AnonSymCOLONEQ |
                // ≜
                FodotSymbols::AnonSymU225c => ast::InterpKind::Total,
            _ => unreachable!()
        }
    }

    fn interpretation_kind_span(&self) -> Span {
        let kind = self.0.child_by_field_id(FodotFields::Kind.into()).unwrap();
        (kind.start_byte()..kind.end_byte()).into()
    }

    fn interpretation(&self) -> ast::Interpretation<Self::Enumeration> {
        let interpretation = self
            .0
            .child_by_field_id(FodotFields::Interpretation.into())
            .unwrap();
        match FodotSymbols::from(interpretation.kind_id()) {
            FodotSymbols::SymEnumerationInterpretation => ast::Interpretation::Enumeration(
                TsEnumerationInterpretation::new_unchecked(interpretation),
            ),
            _ => ast::Interpretation::Constant(unwrap_node_to_enum_elem(interpretation)),
        }
    }
}

pub struct TsEnumerationInterpretation<'a>(Node<'a>);

impl<'a> TsEnumerationInterpretation<'a> {
    fn new_unchecked(node: Node<'a>) -> Self {
        debug_assert!(Self::new(node).is_some());
        Self(node)
    }

    fn new(node: Node<'a>) -> Option<Self> {
        match FodotSymbols::from(node.kind_id()) {
            FodotSymbols::SymEnumerationInterpretation => Some(Self(node)),
            _ => None,
        }
    }
}

impl Spanned for TsEnumerationInterpretation<'_> {
    fn span(&self) -> Span {
        Span::from(self.0.start_byte()..self.0.end_byte())
    }
}

impl<'a> EnumerationInterpretation for TsEnumerationInterpretation<'a> {
    type Enumeration = TsEnumeration<'a>;

    fn enumeration(&self) -> TsEnumeration<'a> {
        TsEnumeration::new_unchecked(
            self.0
                .child_by_field_id(FodotFields::Enumeration.into())
                .unwrap(),
        )
    }

    fn else_element(&self) -> Option<Element> {
        self.0
            .child_by_field_id(FodotFields::ElseElement.into())
            .map(unwrap_node_to_enum_elem)
    }
}

pub struct TsEnumeration<'a>(Node<'a>);

impl<'a> TsEnumeration<'a> {
    fn new_unchecked(node: Node<'a>) -> Self {
        debug_assert!(Self::new(node).is_some());
        Self(node)
    }

    fn new(node: Node<'a>) -> Option<Self> {
        if node.has_error() {
            return None;
        }
        match FodotSymbols::from(node.kind_id()) {
            FodotSymbols::SymEnumeration => Some(Self(node)),
            _ => None,
        }
    }
}

impl Spanned for TsEnumeration<'_> {
    fn span(&self) -> Span {
        (self.0.start_byte()..self.0.end_byte()).into()
    }
}

impl<'a> Enumeration for TsEnumeration<'a> {
    type Tuple = TsTuple<'a>;

    fn values(&self) -> impl Iterator<Item = ast::EnumerationElement<Self::Tuple>> {
        FieldChildrenIter::new(&self.0, FodotFields::Element.into()).map(|f| {
            if let Some(tuple) = TsTuple::new(f) {
                ast::EnumerationElement::Set(SetElement::Tuple(tuple))
            } else if let Some(element) = node_to_enum_elem(f) {
                ast::EnumerationElement::Set(SetElement::El(element))
            } else if let Some(range) = node_to_range_elem(f) {
                ast::EnumerationElement::Set(SetElement::Range(range))
            } else {
                debug_assert_eq!(FodotSymbols::from(f.kind_id()), FodotSymbols::SymMapping);
                ast::EnumerationElement::Map((
                    node_to_tuple_or_enum_elem(
                        f.child_by_field_id(FodotFields::Args.into()).unwrap(),
                    ),
                    unwrap_node_to_enum_elem(
                        f.child_by_field_id(FodotFields::Value.into()).unwrap(),
                    ),
                ))
            }
        })
    }
}

fn node_to_tuple_or_enum_elem(node: Node) -> ast::TupleOrElement<TsTuple> {
    match FodotSymbols::from(node.kind_id()) {
        FodotSymbols::SymTuple => {
            let tuple = TsTuple::new_unchecked(node);
            let mut values = tuple.values();
            let first = values.next();
            let second = values.next();
            drop(values);
            if let (Some(element), true) = (first, second.is_none()) {
                ast::TupleOrElement::El(element)
            } else {
                ast::TupleOrElement::Tuple(tuple)
            }
        }
        _ => ast::TupleOrElement::El(unwrap_node_to_enum_elem(node)),
    }
}

pub struct TsProcedure<'a>(tree_sitter::Node<'a>);

impl<'a> TsProcedure<'a> {
    fn new(node: Node<'a>) -> Option<Self> {
        if node.has_error() {
            return None;
        }
        match FodotSymbols::from(node.kind_id()) {
            FodotSymbols::SymProcedureBlock => Some(Self(node)),
            _ => None,
        }
    }
}

impl Spanned for TsProcedure<'_> {
    fn span(&self) -> Span {
        (self.0.start_byte()..self.0.end_byte()).into()
    }
}

impl ProcedureBlock for TsProcedure<'_> {
    fn keyword_span(&self) -> Span {
        let keyword = self.0.child(0).unwrap();
        (keyword.start_byte()..keyword.end_byte()).into()
    }

    fn name(&self) -> Span {
        let name = self.0.child_by_field_id(FodotFields::Name.into()).unwrap();
        (name.start_byte()..name.end_byte()).into()
    }

    fn args(&self) -> impl Iterator<Item = Span> {
        FieldChildrenIter::new(&self.0, FodotFields::Args.into())
            .map(|f| (f.start_byte()..f.end_byte()).into())
    }

    fn content(&self) -> Option<Span> {
        self.0
            .child_by_field_id(FodotFields::Content.into())
            .map(|content| (content.start_byte()..content.end_byte()).into())
    }
}
