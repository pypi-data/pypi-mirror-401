use crate::fodot::error::{
    BaseTypeMismatchError, ConvertTypeElementError, InconsistentInterpretations, InterpMergeError,
    MissingTypeElementError, MissingTypeInterps, MissingTypeInterpsError, NoBuiltinTypeInterp,
    OverflowError, ParseIntSubTypeError, ParseRealSubTypeError, ParseTypeElementError,
    SetTypeInterpError, TypeInterpFromStrError, TypeMismatch, VocabMismatchError,
    VocabSupersetError, WithPartialInterpsError,
};
use crate::fodot::fmt::{Fmt, FodotDisplay, FodotOptions, FormatOptions};
use crate::fodot::vocabulary::{
    BaseType, IntType, RealType, StrType, TypeStr, TypeSymbolIndex, VocabSwap, VocabSwapper,
    Vocabulary, parse_bool_value, parse_int_value, parse_real_value,
};
use crate::fodot::vocabulary::{CustomTypeRef, IntTypeRef, RealTypeRef, StrTypeRef, TypeRef};
use crate::fodot::{TryFromCtx, display_as_debug};
use comp_core::vocabulary::{TypeEnum, TypeIndex};
use comp_core::{self as cc, IndexRange, IndexRepr, Int, Real};
use core::ops::{Range, RangeInclusive};
use core::panic;
use duplicate::duplicate_item;
use indexmap::IndexSet;
use itertools::Itertools;
use sli_collections::rc::{PtrRepr, RcA};
use sli_collections::{hash_map::IdHashMap, iterator::Iterator as SIterator, rc::Rc};
use std::borrow::Borrow;
use std::fmt::Display;
use std::fmt::Write;
use std::ops::Deref;

use super::default_vocab_swap;

/// Represents an FO(·) element.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum TypeElement<'a> {
    Bool(bool),
    Int(Int),
    Real(Real),
    Str(StrElement<'a>),
}

impl FodotOptions for TypeElement<'_> {
    type Options<'b> = FormatOptions;
}

impl FodotDisplay for TypeElement<'_> {
    fn fmt(
        fmt: Fmt<&Self, Self::Options<'_>>,
        f: &mut std::fmt::Formatter<'_>,
    ) -> std::fmt::Result {
        match fmt.value {
            TypeElement::Bool(value) => write!(f, "{}", value),
            TypeElement::Int(value) => write!(f, "{}", value),
            TypeElement::Real(value) => write!(f, "{}", value),
            TypeElement::Str(value) => write!(f, "{}", value),
        }
    }
}

impl Display for TypeElement<'_> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.display())
    }
}

impl From<bool> for TypeElement<'_> {
    fn from(value: bool) -> Self {
        TypeElement::Bool(value)
    }
}

impl From<Int> for TypeElement<'_> {
    fn from(value: Int) -> Self {
        TypeElement::Int(value)
    }
}

impl From<Real> for TypeElement<'_> {
    fn from(value: Real) -> Self {
        TypeElement::Real(value)
    }
}

impl<'a> TypeElement<'a> {
    /// Returns the corresponding [TypeInterps] if there is one.
    pub fn type_interps(&self) -> Option<&'a PartialTypeInterps> {
        match self {
            Self::Bool(_) | Self::Int(_) | Self::Real(_) => None,
            Self::Str(value) => Some(value.type_interps),
        }
    }

    pub fn codomain(&self) -> TypeRef<'a> {
        match self {
            Self::Bool(_) => TypeRef::Bool,
            Self::Int(_) => TypeRef::Int,
            Self::Real(_) => TypeRef::Real,
            Self::Str(value) => TypeRef::StrType(value.decl()),
        }
    }
}

impl<'a, I: Borrow<str>> TryFromCtx<I> for TypeElement<'a> {
    type Ctx = TypeFull<'a>;
    type Error = ParseTypeElementError;

    fn try_from_ctx(value: I, ctx: Self::Ctx) -> Result<Self, Self::Error> {
        match ctx {
            TypeFull::Bool => Ok(parse_bool_value(value.borrow())?.into()),
            TypeFull::Int => Ok(parse_int_value(value.borrow())?.into()),
            TypeFull::Real => Ok(parse_real_value(value.borrow())?.into()),
            TypeFull::IntType(interp) => Ok(interp.parse_value(value.borrow())?.into()),
            TypeFull::RealType(interp) => Ok(interp.parse_value(value.borrow())?.into()),
            TypeFull::Str(interp) => Ok(interp.parse_value(value.borrow())?.into()),
        }
    }
}

impl<'a, 'b> TryFromCtx<TypeElement<'a>> for TypeElement<'b> {
    type Ctx = TypeFull<'b>;
    type Error = ConvertTypeElementError;

    fn try_from_ctx(value: TypeElement<'a>, ctx: Self::Ctx) -> Result<Self, Self::Error> {
        match (value, ctx) {
            (TypeElement::Bool(value), TypeFull::Bool) => Ok(value.into()),
            (TypeElement::Int(value), TypeFull::Int) => Ok(value.into()),
            (TypeElement::Real(value), TypeFull::Real) => Ok(value.into()),
            (TypeElement::Int(value), TypeFull::IntType(interp)) => {
                if interp.contains(value) {
                    Ok(value.into())
                } else {
                    Err(MissingTypeElementError.into())
                }
            }
            (TypeElement::Real(value), TypeFull::RealType(interp)) => {
                if interp.contains(value) {
                    Ok(value.into())
                } else {
                    Err(MissingTypeElementError.into())
                }
            }
            (TypeElement::Str(value), TypeFull::Str(interp)) => {
                if core::ptr::eq(value.type_interps, interp.type_interps) {
                    // This is safe since we confirmed above that type_interps of 'a does
                    // infact live for atleast 'b
                    Ok(
                        unsafe { core::mem::transmute::<StrElement<'a>, StrElement<'b>>(value) }
                            .into(),
                    )
                } else {
                    Err(MissingTypeElementError.into())
                }
            }
            (val, ty) => Err(TypeMismatch {
                found: val.codomain().into(),
                expected: ty.into(),
            }
            .into()),
        }
    }
}

/// Represents an non-builtin element.
pub enum CustomElement<'a> {
    Str(StrElement<'a>),
}

impl<'a> From<StrElement<'a>> for CustomElement<'a> {
    fn from(value: StrElement<'a>) -> Self {
        Self::Str(value)
    }
}

impl<'a> From<CustomElement<'a>> for TypeElement<'a> {
    fn from(value: CustomElement<'a>) -> Self {
        match value {
            CustomElement::Str(value) => value.into(),
        }
    }
}

/// Represents a str element.
#[derive(Clone)]
pub struct StrElement<'a> {
    // this value field MUST come from the type interps below (or any reference that points to
    // the same type_interps)
    pub(crate) value: &'a str,
    pub(crate) type_decl_index: TypeSymbolIndex,
    pub(crate) type_interps: &'a PartialTypeInterps,
}

impl FodotOptions for StrElement<'_> {
    type Options<'b> = FormatOptions;
}

impl FodotDisplay for StrElement<'_> {
    fn fmt(
        fmt: Fmt<&Self, Self::Options<'_>>,
        f: &mut std::fmt::Formatter<'_>,
    ) -> std::fmt::Result {
        f.write_str(fmt.value.value)
    }
}

display_as_debug!(StrElement<'a>, gen: ('a));

impl Display for StrElement<'_> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.display())
    }
}

impl PartialEq for StrElement<'_> {
    fn eq(&self, other: &Self) -> bool {
        core::ptr::eq(self.type_interps, other.type_interps)
            && self.type_decl_index == other.type_decl_index
            && self.value == other.value
    }
}

impl Eq for StrElement<'_> {}

impl Deref for StrElement<'_> {
    type Target = str;

    fn deref(&self) -> &Self::Target {
        self.value
    }
}

impl<'a> From<StrElement<'a>> for TypeElement<'a> {
    fn from(value: StrElement<'a>) -> Self {
        Self::Str(value)
    }
}

impl<'a, I: Borrow<str>> TryFromCtx<I> for StrElement<'a> {
    type Ctx = StrTypeFull<'a>;
    type Error = MissingTypeElementError;

    fn try_from_ctx(value: I, ctx: Self::Ctx) -> Result<Self, Self::Error> {
        ctx.parse_value(value.borrow())
    }
}

impl<'a> StrElement<'a> {
    /// Returns the corresponding type declaration.
    pub fn decl(&self) -> StrTypeRef<'a> {
        StrType(self.type_decl_index, self.type_interps.vocab())
    }

    pub fn type_interps(&self) -> &'a PartialTypeInterps {
        self.type_interps
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum StrTypeElement {
    Bool(bool),
    Int(Int),
    Real(Real),
    Str(Box<str>),
}

impl<'a> From<TypeElement<'a>> for StrTypeElement {
    fn from(value: TypeElement<'a>) -> Self {
        match value {
            TypeElement::Bool(value) => Self::Bool(value),
            TypeElement::Int(value) => Self::Int(value),
            TypeElement::Real(value) => Self::Real(value),
            TypeElement::Str(value) => Self::Str(value.value.to_owned().into_boxed_str()),
        }
    }
}

impl Display for StrTypeElement {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::Bool(value) => write!(f, "{}", value),
            Self::Int(value) => write!(f, "{}", value),
            Self::Real(value) => write!(f, "{}", value),
            Self::Str(value) => write!(f, "{}", value),
        }
    }
}

#[repr(transparent)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct IntInterp(pub(crate) cc::structure::IntInterp);

impl Default for IntInterp {
    fn default() -> Self {
        Self::new()
    }
}

impl IntInterp {
    pub fn len(&self) -> usize {
        self.0.len()
    }

    pub fn is_empty(&self) -> bool {
        self.0.is_empty()
    }

    pub fn new() -> IntInterp {
        Self(cc::structure::IntInterp::new())
    }

    pub fn try_from_iterator<T>(value: T) -> Result<Self, OverflowError>
    where
        T: IntoIterator<Item = Int>,
    {
        Ok(Self(
            cc::structure::IntInterp::try_from_iterator(value).map_err(|_| OverflowError)?,
        ))
    }

    pub fn contains(&self, value: Int) -> bool {
        self.0.contains(&value)
    }

    pub(crate) fn rc_to_cc(value: Rc<IntInterp>) -> Rc<cc::structure::IntInterp> {
        // Safety:
        // IntInterp is repr(transparent) over cc::structure::IntInterp.
        unsafe { core::mem::transmute::<Rc<IntInterp>, Rc<cc::structure::IntInterp>>(value) }
    }
}

impl From<IntInterp> for cc::structure::IntInterp {
    fn from(value: IntInterp) -> Self {
        value.0
    }
}

impl FromIterator<Int> for IntInterp {
    fn from_iter<T: IntoIterator<Item = Int>>(iter: T) -> Self {
        Self::try_from_iterator(iter).expect("Number too big")
    }
}

pub mod int_interp {
    use super::Int;
    use comp_core::structure::IntInterpIter;
    #[repr(transparent)]
    #[derive(Clone, Debug)]
    pub struct Iter<'a>(pub(crate) IntInterpIter<'a>);

    impl Iterator for Iter<'_> {
        type Item = Int;

        fn next(&mut self) -> Option<Self::Item> {
            self.0.next()
        }
    }
}

impl TryFrom<Range<Int>> for IntInterp {
    type Error = OverflowError;

    fn try_from(value: Range<Int>) -> Result<Self, Self::Error> {
        Ok(Self(value.try_into().map_err(|_| OverflowError)?))
    }
}

impl TryFrom<RangeInclusive<Int>> for IntInterp {
    type Error = OverflowError;

    fn try_from(value: RangeInclusive<Int>) -> Result<Self, Self::Error> {
        Ok(Self(value.try_into().map_err(|_| OverflowError)?))
    }
}

impl<'a> IntoIterator for &'a IntInterp {
    type Item = Int;
    type IntoIter = int_interp::Iter<'a>;

    fn into_iter(self) -> Self::IntoIter {
        int_interp::Iter(self.0.into_iter())
    }
}

impl FodotOptions for IntInterp {
    type Options<'b> = FormatOptions;
}

impl FodotDisplay for IntInterp {
    fn fmt(
        fmt: Fmt<&Self, Self::Options<'_>>,
        f: &mut std::fmt::Formatter<'_>,
    ) -> std::fmt::Result {
        f.write_char('{')?;
        if !fmt.value.is_empty() {
            write!(f, "{}", fmt.value.into_iter().format(", "))?;
        }
        f.write_char('}')
    }
}

impl Display for IntInterp {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.display())
    }
}

#[repr(transparent)]
#[derive(Debug, PartialEq, Eq, Clone)]
pub struct RealInterp(cc::structure::RealInterp);

impl Default for RealInterp {
    fn default() -> Self {
        Self::new()
    }
}

impl RealInterp {
    pub fn new() -> Self {
        Self(cc::structure::RealInterp::new())
    }

    pub fn len(&self) -> usize {
        self.0.len()
    }

    pub fn is_empty(&self) -> bool {
        self.0.is_empty()
    }

    pub fn contains(&self, value: Real) -> bool {
        self.0.contains(&value)
    }

    pub fn insert(&mut self, value: Real) {
        self.0.insert(value);
    }

    pub(crate) fn rc_to_cc(value: Rc<RealInterp>) -> Rc<cc::structure::RealInterp> {
        // Safety:
        // RealInterp is repr(transparent) over cc::structure::RealInterp.
        unsafe { core::mem::transmute::<Rc<RealInterp>, Rc<cc::structure::RealInterp>>(value) }
    }
}

pub mod real_interp {
    use super::Real;
    use comp_core::structure::RealInterp;
    #[derive(Clone, Debug)]
    pub struct Iter<'a>(pub(crate) <&'a RealInterp as IntoIterator>::IntoIter);

    impl<'a> Iterator for Iter<'a> {
        type Item = &'a Real;

        fn next(&mut self) -> Option<Self::Item> {
            self.0.next()
        }
    }
}

impl<'a> IntoIterator for &'a RealInterp {
    type Item = &'a Real;
    type IntoIter = real_interp::Iter<'a>;

    fn into_iter(self) -> Self::IntoIter {
        real_interp::Iter(self.0.into_iter())
    }
}

impl FromIterator<Real> for RealInterp {
    fn from_iter<T: IntoIterator<Item = Real>>(iter: T) -> Self {
        Self(cc::structure::RealInterp::from_iter(iter))
    }
}

impl FodotOptions for RealInterp {
    type Options<'b> = FormatOptions;
}

impl FodotDisplay for RealInterp {
    fn fmt(
        fmt: Fmt<&Self, Self::Options<'_>>,
        f: &mut std::fmt::Formatter<'_>,
    ) -> std::fmt::Result {
        f.write_char('{')?;
        if !fmt.value.is_empty() {
            write!(f, "{}", fmt.value.into_iter().format(", "))?;
        }
        f.write_char('}')
    }
}

impl Display for RealInterp {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.display())
    }
}

/// Represents a type interpretation of str elements.
/// i.e. `type A := { a, b, c }`
#[derive(PartialEq, Eq, Clone)]
pub struct StrInterp(pub(crate) IndexSet<Rc<str>>);

impl Default for StrInterp {
    fn default() -> Self {
        Self::new()
    }
}

impl StrInterp {
    /// Create an empty [StrInterp].
    pub fn new() -> Self {
        StrInterp(Default::default())
    }

    /// Returns the amount of items in the type interpretation.
    pub fn len(&self) -> usize {
        self.0.len()
    }

    pub fn is_empty(&self) -> bool {
        self.0.is_empty()
    }

    pub fn iter(&self) -> <&IndexSet<Rc<str>> as IntoIterator>::IntoIter {
        self.into_iter()
    }

    pub(crate) fn iter_type_enums(&self) -> IndexRange<TypeEnum> {
        IndexRange::new(0..self.len())
    }
}

impl FodotOptions for StrInterp {
    type Options<'b> = FormatOptions;
}

impl FodotDisplay for StrInterp {
    fn fmt(
        fmt: Fmt<&Self, Self::Options<'_>>,
        f: &mut std::fmt::Formatter<'_>,
    ) -> std::fmt::Result {
        f.write_char('{')?;
        if !fmt.value.is_empty() {
            write!(f, "{}", fmt.value.into_iter().format(", "))?;
        }
        f.write_char('}')
    }
}

impl Display for StrInterp {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.display())
    }
}

display_as_debug!(StrInterp);

impl<'a> IntoIterator for &'a StrInterp {
    type Item = <&'a IndexSet<Rc<str>> as IntoIterator>::Item;
    type IntoIter = <&'a IndexSet<Rc<str>> as IntoIterator>::IntoIter;

    fn into_iter(self) -> Self::IntoIter {
        self.0.borrow().into_iter()
    }
}

impl FromIterator<Rc<str>> for StrInterp {
    fn from_iter<T: IntoIterator<Item = Rc<str>>>(iter: T) -> Self {
        let mut set = IndexSet::from_iter(iter);
        // TODO: keep stuff sorted or something
        set.sort();
        Self(set)
    }
}

impl<'a> FromIterator<&'a str> for StrInterp {
    fn from_iter<T: IntoIterator<Item = &'a str>>(iter: T) -> Self {
        let mut set = IndexSet::from_iter(iter.into_iter().map(|f| f.into()));
        // TODO: keep stuff sorted or something
        set.sort();
        Self(set)
    }
}

/// An enum of type interpretations.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum TypeInterp {
    Int(Rc<IntInterp>),
    Real(Rc<RealInterp>),
    Str(Rc<StrInterp>),
}

impl From<IntInterp> for TypeInterp {
    fn from(value: IntInterp) -> Self {
        Self::Int(value.into())
    }
}

impl From<Rc<IntInterp>> for TypeInterp {
    fn from(value: Rc<IntInterp>) -> Self {
        Self::Int(value)
    }
}

impl From<RealInterp> for TypeInterp {
    fn from(value: RealInterp) -> Self {
        Self::Real(value.into())
    }
}

impl From<Rc<RealInterp>> for TypeInterp {
    fn from(value: Rc<RealInterp>) -> Self {
        Self::Real(value)
    }
}

impl From<StrInterp> for TypeInterp {
    fn from(value: StrInterp) -> Self {
        Self::Str(value.into())
    }
}

impl From<Rc<StrInterp>> for TypeInterp {
    fn from(value: Rc<StrInterp>) -> Self {
        Self::Str(value)
    }
}

impl FodotOptions for TypeInterp {
    type Options<'a> = FormatOptions;
}

impl FodotDisplay for TypeInterp {
    fn fmt(
        fmt: Fmt<&Self, Self::Options<'_>>,
        f: &mut std::fmt::Formatter<'_>,
    ) -> std::fmt::Result {
        match fmt.value {
            Self::Int(value) => FodotDisplay::fmt(fmt.with_opts(value.as_ref()), f),
            Self::Real(value) => FodotDisplay::fmt(fmt.with_opts(value.as_ref()), f),
            Self::Str(value) => FodotDisplay::fmt(fmt.with_opts(value.as_ref()), f),
        }
    }
}

impl Display for TypeInterp {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        Display::fmt(&self.display(), f)
    }
}

impl TypeInterp {
    pub fn base_type(&self) -> BaseType {
        match self {
            Self::Int(_) => BaseType::Int,
            Self::Real(_) => BaseType::Real,
            Self::Str(_) => BaseType::Str,
        }
    }
}

#[derive(Default, Clone)]
pub(crate) struct _PartialTypeInterps(IdHashMap<TypeSymbolIndex, TypeInterp>);

impl _PartialTypeInterps {
    pub fn add_interp(&mut self, index: TypeSymbolIndex, interp: TypeInterp) {
        self.0.insert(index, interp);
    }

    pub fn get_interp(&self, index: TypeSymbolIndex) -> Option<&TypeInterp> {
        self.0.get(&index)
    }

    pub fn iter(&self) -> impl SIterator<Item = (&TypeSymbolIndex, &TypeInterp)> + Clone {
        self.0.iter()
    }
}

/// A collection of type interpretations where a type is allowed to not have an interpretation.
///
/// After ensuring that all types declared in the underlying vocabulary have been given an
/// interpretation calling [Self::try_complete] returns a [TypeInterps].
#[derive(Clone)]
pub struct PartialTypeInterps {
    pub(crate) vocab: Rc<Vocabulary>,
    /// Incomplete types are represented using empty types on the comp-core side.
    pub(crate) cc: Rc<cc::structure::TypeInterps>,
    pub(crate) str_interps: IdHashMap<TypeSymbolIndex, Rc<StrInterp>>,
    pub(crate) complete: Box<[bool]>,
}

impl FodotOptions for PartialTypeInterps {
    type Options<'b> = FormatOptions;
}

impl FodotDisplay for PartialTypeInterps {
    fn fmt(
        fmt: Fmt<&Self, Self::Options<'_>>,
        f: &mut std::fmt::Formatter<'_>,
    ) -> std::fmt::Result {
        let mut iter = fmt.value.iter().peekable();
        while let Some(type_interp) = iter.next() {
            fmt.options.write_indent(f)?;
            write!(f, "{}.", fmt.with_format_opts(&type_interp))?;
            if iter.peek().is_some() {
                writeln!(f)?;
            }
        }
        Ok(())
    }
}

impl Display for PartialTypeInterps {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.display())
    }
}

display_as_debug!(PartialTypeInterps);

impl PartialEq for PartialTypeInterps {
    fn eq(&self, other: &Self) -> bool {
        Rc::ptr_eq(&self.vocab, &other.vocab)
            && self.complete == other.complete
            && self.cc.interps() == other.cc.interps()
    }
}

impl PartialEq<TypeInterps> for PartialTypeInterps {
    fn eq(&self, other: &TypeInterps) -> bool {
        Rc::ptr_eq(&self.vocab, other.vocab_rc())
            && self.is_complete()
            && self.cc.interps() == other.0.cc.interps()
    }
}

impl PartialEq<PartialTypeInterps> for TypeInterps {
    fn eq(&self, other: &PartialTypeInterps) -> bool {
        PartialEq::<TypeInterps>::eq(other, self)
    }
}

impl PartialTypeInterps {
    pub(crate) fn for_vocab(vocab: Rc<Vocabulary>) -> Self {
        let (raw, complete): (Vec<_>, Vec<_>) = vocab
            .id_iter_types()
            .map(|i| {
                let cc_id = vocab.type_decl_to_cc(i);
                if let Some(value) = vocab.part_type_interps.get_interp(i) {
                    return (
                        match value {
                            TypeInterp::Int(value) => IntInterp::rc_to_cc(value.clone()).into(),
                            TypeInterp::Real(value) => RealInterp::rc_to_cc(value.clone()).into(),
                            TypeInterp::Str(value) => {
                                cc::structure::StrInterp::new(value.len()).into()
                            }
                        },
                        true,
                    );
                }
                let cc_decl = &vocab.comp_core_symbs.types[cc_id];
                // type interp not known yet, insert empty interpretations on comp-core side.
                (
                    match cc_decl.super_type {
                        cc::vocabulary::BaseType::Int => {
                            cc::structure::IntInterp::try_from_iterator([])
                                .unwrap()
                                .into()
                        }
                        cc::vocabulary::BaseType::Real => cc::structure::RealInterp::new().into(),
                        cc::vocabulary::BaseType::Str => cc::structure::StrInterp::new(0).into(),
                    },
                    false,
                )
            })
            .unzip();
        Self {
            cc: Rc::new(
                cc::structure::TypeInterps::try_from_raw(vocab.comp_core_symbs.clone(), raw.into())
                    .unwrap(),
            ),
            str_interps: vocab
                .part_type_interps
                .0
                .iter()
                .filter_map(|f| match f.1 {
                    TypeInterp::Str(interp) => Some((*f.0, interp.clone())),
                    TypeInterp::Int(_) | TypeInterp::Real(_) => None,
                })
                .collect(),
            complete: complete.into_boxed_slice(),
            vocab,
        }
    }

    pub(crate) fn ensured_get_interp(&self, type_id: TypeSymbolIndex) -> TypeInterpRef<'_> {
        self._get_interp(type_id).unwrap()
    }

    pub(crate) fn _get_interp(&self, type_id: TypeSymbolIndex) -> Option<TypeInterpRef<'_>> {
        use cc::structure::TypeInterp as TI;
        if !self.complete[usize::from(type_id)] {
            return None;
        }
        Some(match &self.cc[TypeIndex::from(IndexRepr::from(type_id))] {
            TI::Int(int_interp) => TypeInterpRef::Int(unsafe {
                core::mem::transmute::<&cc::structure::IntInterp, &IntInterp>(int_interp.as_ref())
            }),
            TI::Real(real_interp) => TypeInterpRef::Real(unsafe {
                core::mem::transmute::<&cc::structure::RealInterp, &RealInterp>(
                    real_interp.as_ref(),
                )
            }),
            TI::Custom(_) => TypeInterpRef::Str(&self.str_interps[&type_id]),
        })
    }

    pub(crate) fn _get_interp_cloned(&self, type_id: TypeSymbolIndex) -> Option<TypeInterp> {
        use cc::structure::TypeInterp as TI;
        if !self.complete[usize::from(type_id)] {
            return None;
        }
        Some(match &self.cc[TypeIndex::from(IndexRepr::from(type_id))] {
            TI::Int(int_interp) => {
                let raw = Rc::into_raw(Rc::clone(int_interp));
                // Safety:
                // IntInterp is repr(transparent) of comp-core IntInterp
                TypeInterp::Int(unsafe { Rc::from_raw(raw as *const IntInterp) })
            }
            TI::Real(real_interp) => {
                let raw = Rc::into_raw(Rc::clone(real_interp));
                // Safety:
                // RealInterp is repr(transparent) of comp-core RealInterp
                TypeInterp::Real(unsafe { Rc::from_raw(raw as *const RealInterp) })
            }
            TI::Custom(_) => TypeInterp::Str(Rc::clone(&self.str_interps[&type_id])),
        })
    }

    pub fn vocab(&self) -> &Vocabulary {
        &self.vocab
    }

    pub fn vocab_rc(&self) -> &Rc<Vocabulary> {
        &self.vocab
    }

    pub fn set_interp(
        &mut self,
        custom_type: CustomTypeRef,
        interp: TypeInterp,
    ) -> Result<(), SetTypeInterpError> {
        if !custom_type.vocab().exact_eq(self.vocab()) {
            return Err(VocabMismatchError.into());
        }
        if custom_type.super_type() != interp.base_type() {
            let declared_base = match custom_type {
                CustomTypeRef::Int(_) => BaseType::Int,
                CustomTypeRef::Real(_) => BaseType::Real,
                CustomTypeRef::Str(_) => BaseType::Str,
            };
            return Err(BaseTypeMismatchError {
                found: interp.base_type(),
                expected: declared_base,
            }
            .into());
        }
        self._set_interp(custom_type.type_id(), interp);
        Ok(())
    }

    pub fn _set_interp(&mut self, type_id: TypeSymbolIndex, interp: TypeInterp) {
        let cc_id = self.vocab().type_decl_to_cc(type_id);
        match interp {
            TypeInterp::Int(interp) => {
                Rc::make_mut(&mut self.cc).mut_interps()[cc_id] =
                    IntInterp::rc_to_cc(interp).into();
            }
            TypeInterp::Real(interp) => {
                Rc::make_mut(&mut self.cc).mut_interps()[cc_id] =
                    RealInterp::rc_to_cc(interp).into();
            }
            TypeInterp::Str(interp) => {
                Rc::make_mut(&mut self.cc).mut_interps()[cc_id] =
                    cc::structure::StrInterp::new(interp.len()).into();
                self.str_interps.insert(type_id, interp);
            }
        };
        self.complete[usize::from(type_id)] = true;
    }

    pub fn get_interp_from_str<'a>(
        &'a self,
        type_name: &str,
    ) -> Result<Option<TypeInterpRef<'a>>, TypeInterpFromStrError> {
        let type_ = self.vocab.parse_type(type_name)?;
        match type_ {
            TypeRef::Bool => Err(NoBuiltinTypeInterp.into()),
            TypeRef::Int => Err(NoBuiltinTypeInterp.into()),
            TypeRef::Real => Err(NoBuiltinTypeInterp.into()),
            TypeRef::IntType(int_type) => Ok(self._get_interp(int_type.0)),
            TypeRef::RealType(real_type) => Ok(self._get_interp(real_type.0)),
            TypeRef::StrType(str_type) => Ok(self._get_interp(str_type.0)),
        }
    }

    pub fn get_interp<'a>(
        &'a self,
        type_: CustomTypeRef<'a>,
    ) -> Result<Option<CustomTypeFull<'a>>, VocabMismatchError> {
        if !self.vocab.exact_eq(type_.vocab()) {
            return Err(VocabMismatchError);
        }
        match (self._get_interp(type_.type_id()), type_) {
            (Some(TypeInterpRef::Int(interp)), CustomTypeRef::Int(decl)) => Ok(Some(
                IntTypeFull {
                    type_decl_index: decl.0,
                    type_interps: self,
                    interp,
                }
                .into(),
            )),
            (Some(TypeInterpRef::Real(interp)), CustomTypeRef::Real(decl)) => Ok(Some(
                RealTypeFull {
                    type_decl_index: decl.0,
                    type_interps: self,
                    interp,
                }
                .into(),
            )),
            (Some(TypeInterpRef::Str(interp)), CustomTypeRef::Str(decl)) => Ok(Some(
                StrTypeFull {
                    type_decl_index: decl.0,
                    type_interps: self,
                    interp,
                }
                .into(),
            )),
            (None, _) => Ok(None),
            _ => unreachable!(),
        }
    }

    pub fn get_interp_cloned(
        &self,
        custom_type: CustomTypeRef,
    ) -> Result<Option<TypeInterp>, VocabMismatchError> {
        if !self.vocab.exact_eq(custom_type.vocab()) {
            return Err(VocabMismatchError);
        }
        Ok(self._get_interp_cloned(custom_type.type_id()))
    }

    pub fn is_complete(&self) -> bool {
        self.complete.iter().all(|f| *f)
    }

    pub fn try_complete(self) -> Result<TypeInterps, Self> {
        if self.is_complete() {
            Ok(TypeInterps(self))
        } else {
            Err(self)
        }
    }

    pub fn try_rc_into_complete(this: Rc<Self>) -> Result<Rc<TypeInterps>, Rc<Self>> {
        if this.is_complete() {
            // Safety:
            // Self is repr transparent of PartialTypeInterps.
            Ok(unsafe { Rc::from_raw(Rc::into_raw(this) as *const TypeInterps) })
        } else {
            Err(this)
        }
    }

    pub fn missing_type_error(&self) -> MissingTypeInterps {
        MissingTypeInterps {
            missing: self.iter_missing().map(|f| f.name().to_string()).collect(),
        }
    }

    /// Tries to convert `self` to a [TypeInterps].
    ///
    /// Returns a [MissingTypeInterpsError] on failure.
    ///
    /// See also [Self::try_complete], which returns this [PartialTypeInterps] instead of an actual
    /// error.
    pub fn try_err_complete(self) -> Result<TypeInterps, MissingTypeInterpsError> {
        self.try_into()
    }

    pub fn from_rc_complete(type_interps: Rc<TypeInterps>) -> Rc<Self> {
        // Safety:
        // type_interps is repr transparent of PartialTypeInterps.
        unsafe { Rc::from_raw(Rc::into_raw(type_interps) as *const Self) }
    }

    pub fn has_interp(&self, type_: CustomTypeRef) -> Result<bool, VocabMismatchError> {
        if !self.vocab().exact_eq(type_.vocab()) {
            return Err(VocabMismatchError);
        }
        Ok(self.complete[usize::from(type_.type_id())])
    }

    pub fn iter(&self) -> impl SIterator<Item = CustomTypeFull<'_>> {
        self.vocab
            .iter_types()
            .filter_map(|f| self.get_interp(f).unwrap())
    }

    pub fn iter_missing(&self) -> impl Iterator<Item = CustomTypeRef<'_>> + use<'_> {
        self.complete.iter().enumerate().filter(|f| !*f.1).map(|f| {
            let type_id = TypeSymbolIndex::from(f.0);
            self.vocab._get_type(type_id)
        })
    }

    pub fn merge(&mut self, other: &Self) -> Result<(), InterpMergeError> {
        if !self.vocab().exact_eq(other.vocab()) {
            return Err(VocabMismatchError.into());
        }
        let mut errors = Vec::new();
        for type_full in other.iter() {
            let interp = other
                .get_interp_cloned(type_full.to_ref())
                .expect("same vocab")
                .expect("has interp since we are iterating");
            if let Some(value) = self._get_interp(type_full.to_ref().type_id()) {
                if value != interp {
                    errors.push(type_full.to_ref().name().to_string());
                }
            }
        }
        if !errors.is_empty() {
            return Err(InconsistentInterpretations {
                symbol_names: errors,
            }
            .into());
        }
        for type_full in other.iter() {
            let interp = other
                .get_interp_cloned(type_full.to_ref())
                .expect("same vocab")
                .expect("has interp since we are iterating");
            if self._get_interp(type_full.to_ref().type_id()).is_some() {
                continue;
            }
            self.set_interp(type_full.to_ref(), interp)
                .expect("same vocabulary and as such correct base type");
        }
        Ok(())
    }
}

impl PartialTypeInterps {
    pub(crate) fn _swap_vocab(&mut self, vocabulary: Rc<Vocabulary>) {
        let mut start_point = Vocabulary::get_type_interps(vocabulary.clone());
        for bla in self.iter() {
            let type_ref = bla.to_ref();
            let custom_type = vocabulary
                .parse_custom_type(type_ref.name())
                .expect("vocabulary is a superset of self.vocab()");
            // If the start_point has it, the original must have the same interp
            if start_point._get_interp(custom_type.type_id()).is_some() {
                continue;
            }
            if let Some(interp) = self._get_interp_cloned(custom_type.type_id()) {
                start_point._set_interp(custom_type.type_id(), interp)
            }
        }
        *self = start_point;
    }
}

impl VocabSwap for PartialTypeInterps {
    fn swap_vocab(&mut self, vocabulary: Rc<Vocabulary>) -> Result<(), VocabSupersetError> {
        default_vocab_swap(self, self.vocab_rc().clone(), vocabulary)
    }

    fn vocab_swapper(
        &mut self,
        vocabulary_swapper: VocabSwapper,
    ) -> Result<(), VocabMismatchError> {
        if !vocabulary_swapper.get_old().exact_eq(self.vocab()) {
            return Err(VocabMismatchError);
        }
        self._swap_vocab(vocabulary_swapper.get_new_rc().clone());
        Ok(())
    }
}

#[allow(unused)]
#[repr(transparent)]
pub struct TypeInterps(pub(crate) PartialTypeInterps);

pub trait IntoPtr<I> {
    type Target: PtrRepr<I>;
    fn into_ptr(self) -> Self::Target;
}

impl<'a> IntoPtr<PartialTypeInterps> for &'a TypeInterps {
    type Target = &'a PartialTypeInterps;
    fn into_ptr(self) -> Self::Target {
        self.into()
    }
}

impl IntoPtr<PartialTypeInterps> for RcA<TypeInterps> {
    type Target = RcA<PartialTypeInterps>;
    fn into_ptr(self) -> Self::Target {
        TypeInterps::into_partial_rca(self)
    }
}

impl IntoPtr<PartialTypeInterps> for Rc<TypeInterps> {
    type Target = RcA<PartialTypeInterps>;
    fn into_ptr(self) -> Self::Target {
        TypeInterps::into_partial_rca(self.into())
    }
}

impl TryFrom<PartialTypeInterps> for TypeInterps {
    type Error = MissingTypeInterpsError;

    fn try_from(value: PartialTypeInterps) -> Result<Self, Self::Error> {
        if value.is_complete() {
            Ok(Self(value))
        } else {
            Err(value.missing_type_error().into())
        }
    }
}

impl From<TypeInterps> for PartialTypeInterps {
    fn from(value: TypeInterps) -> Self {
        value.into_partial()
    }
}

impl<'a> From<&'a TypeInterps> for &'a PartialTypeInterps {
    fn from(value: &'a TypeInterps) -> Self {
        // Safety:
        // This is safe since TypeInterps is repr(transparent) of PartialTypeInterps
        unsafe { core::mem::transmute::<&'a TypeInterps, &'a PartialTypeInterps>(value) }
    }
}

impl FodotOptions for TypeInterps {
    type Options<'b> = FormatOptions;
}

impl FodotDisplay for TypeInterps {
    fn fmt(
        fmt: Fmt<&Self, Self::Options<'_>>,
        f: &mut std::fmt::Formatter<'_>,
    ) -> std::fmt::Result {
        let mut iter = fmt.value.iter().peekable();
        while let Some(type_interp) = iter.next() {
            fmt.options.write_indent(f)?;
            write!(f, "{}.", fmt.with_format_opts(&type_interp))?;
            if iter.peek().is_some() {
                writeln!(f)?;
            }
        }
        Ok(())
    }
}

impl Display for TypeInterps {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.display())
    }
}

display_as_debug!(TypeInterps);

impl TypeInterps {
    pub(crate) fn cc(&self) -> &Rc<comp_core::structure::TypeInterps> {
        &self.0.cc
    }

    pub fn vocab(&self) -> &Vocabulary {
        &self.0.vocab
    }

    pub fn vocab_rc(&self) -> &Rc<Vocabulary> {
        &self.0.vocab
    }

    pub fn get_interp_from_str<'a>(
        &'a self,
        type_name: &str,
    ) -> Result<TypeInterpRef<'a>, TypeInterpFromStrError> {
        self.0.get_interp_from_str(type_name).map(|f| f.unwrap())
    }

    pub fn get_interp<'a>(
        &'a self,
        type_: CustomTypeRef<'a>,
    ) -> Result<CustomTypeFull<'a>, VocabMismatchError> {
        self.0.get_interp(type_).map(|f| f.unwrap())
    }

    pub fn iter(&self) -> impl SIterator<Item = CustomTypeFull<'_>> {
        self.0
            .vocab
            .iter_types()
            .map(|f| self.get_interp(f).unwrap())
    }

    pub fn into_partial(self) -> PartialTypeInterps {
        // Safety:
        // Self is repr transparent of PartialTypeInterps.
        unsafe { core::mem::transmute::<Self, PartialTypeInterps>(self) }
    }

    pub fn into_partial_rc(this: Rc<Self>) -> Rc<PartialTypeInterps> {
        // Safety:
        // Self is repr transparent of PartialTypeInterps.
        unsafe { Rc::from_raw(Rc::into_raw(this) as *const PartialTypeInterps) }
    }

    pub(crate) fn into_partial_rca(this: RcA<Self>) -> RcA<PartialTypeInterps> {
        // Safety:
        // Self is repr transparent of PartialTypeInterps.
        unsafe { RcA::from_raw(RcA::into_raw(this) as *const PartialTypeInterps) }
    }

    pub fn try_from_partial(partial: PartialTypeInterps) -> Result<Self, MissingTypeInterpsError> {
        partial.try_into()
    }
}

#[derive(Clone, Copy, PartialEq)]
pub enum TypeInterpRef<'a> {
    Int(&'a IntInterp),
    Real(&'a RealInterp),
    Str(&'a StrInterp),
}

impl PartialEq<TypeInterp> for TypeInterpRef<'_> {
    fn eq(&self, other: &TypeInterp) -> bool {
        match (self, other) {
            (Self::Int(left), TypeInterp::Int(right)) => {
                core::ptr::eq(*left, right.as_ref()) || *left == right.as_ref()
            }
            (Self::Real(left), TypeInterp::Real(right)) => {
                core::ptr::eq(*left, right.as_ref()) || *left == right.as_ref()
            }
            (Self::Str(left), TypeInterp::Str(right)) => {
                core::ptr::eq(*left, right.as_ref()) || *left == right.as_ref()
            }
            _ => false,
        }
    }
}

impl PartialEq<TypeInterpRef<'_>> for TypeInterp {
    fn eq(&self, other: &TypeInterpRef<'_>) -> bool {
        <TypeInterpRef as PartialEq<TypeInterp>>::eq(other, self)
    }
}

impl<'a> TypeInterpRef<'a> {
    pub fn unwrap_int(self) -> &'a IntInterp {
        match self {
            Self::Int(value) => value,
            _ => panic!("unwrap on _TypeInterpRef"),
        }
    }

    pub fn unwrap_real(self) -> &'a RealInterp {
        match self {
            Self::Real(value) => value,
            _ => panic!("unwrap on _TypeInterpRef"),
        }
    }

    pub fn unwrap_str(self) -> &'a StrInterp {
        match self {
            Self::Str(value) => value,
            _ => panic!("unwrap on _TypeInterpRef"),
        }
    }
}

/// A [Type](crate::fodot::vocabulary::Type) bundled with a [TypeInterps] reference.
#[derive(Clone)]
pub enum TypeFull<'a> {
    Bool,
    Int,
    Real,
    IntType(IntTypeFull<'a>),
    RealType(RealTypeFull<'a>),
    Str(StrTypeFull<'a>),
}

impl<'a> TypeFull<'a> {
    pub fn as_type(&self) -> TypeRef<'a> {
        match self {
            Self::Bool => TypeRef::Bool,
            Self::Int => TypeRef::Int,
            Self::Real => TypeRef::Real,
            Self::IntType(value) => {
                TypeRef::IntType(IntType(value.type_decl_index, value.type_interps.vocab()))
            }
            Self::RealType(value) => {
                TypeRef::RealType(RealType(value.type_decl_index, value.type_interps.vocab()))
            }
            Self::Str(value) => {
                TypeRef::StrType(StrType(value.type_decl_index, value.type_interps.vocab()))
            }
        }
    }

    pub fn into_type(self) -> TypeRef<'a> {
        match self {
            Self::Bool => TypeRef::Bool,
            Self::Int => TypeRef::Int,
            Self::Real => TypeRef::Real,
            Self::IntType(value) => {
                TypeRef::IntType(IntType(value.type_decl_index, value.type_interps.vocab()))
            }
            Self::RealType(value) => {
                TypeRef::RealType(RealType(value.type_decl_index, value.type_interps.vocab()))
            }
            Self::Str(value) => {
                TypeRef::StrType(StrType(value.type_decl_index, value.type_interps.vocab()))
            }
        }
    }
}

impl<'a> TypeRef<'a> {
    pub fn with_interps(
        self,
        type_interps: &'a TypeInterps,
    ) -> Result<TypeFull<'a>, VocabMismatchError> {
        match self {
            Self::Bool => Ok(TypeFull::Bool),
            Self::Int => Ok(TypeFull::Int),
            Self::Real => Ok(TypeFull::Real),
            Self::IntType(type_) => type_.with_interps(type_interps).map(|f| f.into()),
            Self::RealType(type_) => type_.with_interps(type_interps).map(|f| f.into()),
            Self::StrType(type_) => type_.with_interps(type_interps).map(|f| f.into()),
        }
    }

    pub fn with_partial_interps(
        self,
        type_interps: &'a PartialTypeInterps,
    ) -> Result<TypeFull<'a>, WithPartialInterpsError> {
        match self {
            Self::Bool => Ok(TypeFull::Bool),
            Self::Int => Ok(TypeFull::Int),
            Self::Real => Ok(TypeFull::Real),
            Self::IntType(type_) => type_.with_partial_interps(type_interps).map(|f| f.into()),
            Self::RealType(type_) => type_.with_partial_interps(type_interps).map(|f| f.into()),
            Self::StrType(type_) => type_.with_partial_interps(type_interps).map(|f| f.into()),
        }
    }
}

/// A [CustomType](crate::fodot::vocabulary::CustomType) bundled with a [TypeInterps] reference.
#[non_exhaustive]
#[derive(Clone)]
pub enum CustomTypeFull<'a> {
    Int(IntTypeFull<'a>),
    Real(RealTypeFull<'a>),
    Str(StrTypeFull<'a>),
}

impl FodotOptions for CustomTypeFull<'_> {
    type Options<'b> = FormatOptions;
}

impl FodotDisplay for CustomTypeFull<'_> {
    fn fmt(
        fmt: Fmt<&Self, Self::Options<'_>>,
        f: &mut std::fmt::Formatter<'_>,
    ) -> std::fmt::Result {
        match fmt.value {
            Self::Int(value) => FodotDisplay::fmt(fmt.with_opts(value), f),
            Self::Real(value) => FodotDisplay::fmt(fmt.with_opts(value), f),
            Self::Str(value) => FodotDisplay::fmt(fmt.with_opts(value), f),
        }
    }
}

impl Display for CustomTypeFull<'_> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.display())
    }
}

impl PartialEq<TypeInterp> for CustomTypeFull<'_> {
    fn eq(&self, other: &TypeInterp) -> bool {
        match (self, other) {
            (Self::Int(left), TypeInterp::Int(right)) => left.interp() == right.as_ref(),
            (Self::Real(left), TypeInterp::Real(right)) => left.interp() == right.as_ref(),
            (Self::Str(left), TypeInterp::Str(right)) => left.interp() == right.as_ref(),
            _ => false,
        }
    }
}

impl<'a> CustomTypeFull<'a> {
    /// Returns the contained [CustomTypeFull::Int].
    ///
    /// # panics
    ///
    /// If self is not a [CustomTypeFull::Int] variant.
    pub fn unwrap_int(self) -> IntTypeFull<'a> {
        match self {
            Self::Int(value) => value,
            _ => panic!("unwrap on non int type!"),
        }
    }

    /// Returns the contained [CustomTypeFull::Real].
    ///
    /// # panics
    ///
    /// If self is not a [CustomTypeFull::Real] variant.
    pub fn unwrap_real(self) -> RealTypeFull<'a> {
        match self {
            Self::Real(value) => value,
            _ => panic!("unwrap on non real type!"),
        }
    }

    /// Returns the contained [CustomTypeFull::Str].
    ///
    /// # panics
    ///
    /// If self is not a [CustomTypeFull::Str] variant.
    pub fn unwrap_str(self) -> StrTypeFull<'a> {
        match self {
            Self::Str(value) => value,
            _ => panic!("unwrap on non str type!"),
        }
    }

    pub fn to_ref(&self) -> CustomTypeRef<'a> {
        match self {
            Self::Int(value) => value.to_ref().into(),
            Self::Real(value) => value.to_ref().into(),
            Self::Str(value) => value.to_ref().into(),
        }
    }
}

/// A [IntType] bundled with a [TypeInterps] reference and the type's [IntInterp].
#[derive(Clone)]
pub struct IntTypeFull<'a> {
    pub(crate) type_decl_index: TypeSymbolIndex,
    pub(crate) type_interps: &'a PartialTypeInterps,
    pub(crate) interp: &'a IntInterp,
}

impl<'a> From<IntTypeFull<'a>> for TypeFull<'a> {
    fn from(value: IntTypeFull<'a>) -> Self {
        Self::IntType(value)
    }
}

impl<'a> From<IntTypeFull<'a>> for CustomTypeFull<'a> {
    fn from(value: IntTypeFull<'a>) -> Self {
        Self::Int(value)
    }
}

impl<'a> IntTypeFull<'a> {
    pub fn name(&self) -> &'a str {
        self.to_ref().name_ref()
    }

    /// Returns the reference to the [IntInterp] of the type.
    pub fn interp(&self) -> &'a IntInterp {
        self.interp
    }

    /// Returns true if the [Int] value is contained in the custom type.
    pub fn contains(&self, value: Int) -> bool {
        self.interp.contains(value)
    }

    /// Parses a &[str] to an [Int] that is contained in this type.
    pub fn parse_value(&self, value: &str) -> Result<Int, ParseIntSubTypeError> {
        let value = parse_int_value(value)?;
        if self.contains(value) {
            Ok(value)
        } else {
            Err(MissingTypeElementError.into())
        }
    }

    pub fn to_ref(&self) -> IntTypeRef<'a> {
        IntType(self.type_decl_index, self.type_interps.vocab())
    }
}

/// A [RealType] bundled with a [TypeInterps] reference and the type's [RealInterp].
#[derive(Clone)]
pub struct RealTypeFull<'a> {
    pub(crate) type_decl_index: TypeSymbolIndex,
    pub(crate) type_interps: &'a PartialTypeInterps,
    pub(crate) interp: &'a RealInterp,
}

impl<'a> From<RealTypeFull<'a>> for TypeFull<'a> {
    fn from(value: RealTypeFull<'a>) -> Self {
        Self::RealType(value)
    }
}

impl<'a> From<RealTypeFull<'a>> for CustomTypeFull<'a> {
    fn from(value: RealTypeFull<'a>) -> Self {
        Self::Real(value)
    }
}

impl<'a> RealTypeFull<'a> {
    pub fn name(&self) -> &'a str {
        self.to_ref().name_ref()
    }

    /// Returns the reference to the [RealInterp] of the type.
    pub fn interp(&self) -> &'a RealInterp {
        self.interp
    }

    /// Returns true if the [Real] value is contained in the custom type.
    pub fn contains(&self, value: Real) -> bool {
        self.interp.contains(value)
    }

    /// Parses a [str] to an [Real] that is contained in this type.
    pub fn parse_value(&self, value: &str) -> Result<Real, ParseRealSubTypeError> {
        let value = parse_real_value(value)?;
        if self.contains(value) {
            Ok(value)
        } else {
            Err(MissingTypeElementError.into())
        }
    }

    pub fn to_ref(&self) -> RealTypeRef<'a> {
        RealType(self.type_decl_index, self.type_interps.vocab())
    }
}

/// A [StrType] bundled with a [TypeInterps] reference and the type's [StrInterp].
#[derive(Clone)]
pub struct StrTypeFull<'a> {
    pub(crate) type_decl_index: TypeSymbolIndex,
    pub(crate) type_interps: &'a PartialTypeInterps,
    pub(crate) interp: &'a StrInterp,
}

impl<'a> From<StrTypeFull<'a>> for TypeFull<'a> {
    fn from(value: StrTypeFull<'a>) -> Self {
        Self::Str(value)
    }
}

impl<'a> From<StrTypeFull<'a>> for CustomTypeFull<'a> {
    fn from(value: StrTypeFull<'a>) -> Self {
        Self::Str(value)
    }
}

impl<'a> StrTypeFull<'a> {
    pub fn name(&self) -> &'a str {
        self.to_ref().name_ref()
    }

    /// Returns the reference to the [StrInterp] of the type.
    pub fn interp(&self) -> &'a StrInterp {
        self.interp
    }

    /// Parses a [str] to an [StrElement] that is contained in this type.
    pub fn parse_value(&self, value: &str) -> Result<StrElement<'a>, MissingTypeElementError> {
        if let Some(value) = self.interp.0.get(value) {
            Ok(StrElement {
                value,
                type_decl_index: self.type_decl_index,
                type_interps: self.type_interps,
            })
        } else {
            Err(MissingTypeElementError)
        }
    }

    pub fn to_ref(&self) -> StrTypeRef<'a> {
        StrType(self.type_decl_index, self.type_interps.vocab())
    }
}

impl<'a> IntTypeRef<'a> {
    pub fn with_interps(
        self,
        type_interp: &'a TypeInterps,
    ) -> Result<IntTypeFull<'a>, VocabMismatchError> {
        match type_interp.get_interp(self.into())? {
            CustomTypeFull::Int(value) => Ok(value),
            _ => unreachable!(),
        }
    }

    pub fn with_partial_interps(
        self,
        type_interp: &'a PartialTypeInterps,
    ) -> Result<IntTypeFull<'a>, WithPartialInterpsError> {
        match type_interp.get_interp(self.into())? {
            Some(CustomTypeFull::Int(value)) => Ok(value),
            None => Err(MissingTypeInterps {
                missing: vec![self.name().to_string()],
            }
            .into()),
            _ => unreachable!(),
        }
    }
}

impl<'a> RealTypeRef<'a> {
    pub fn with_interps(
        self,
        type_interp: &'a TypeInterps,
    ) -> Result<RealTypeFull<'a>, VocabMismatchError> {
        match type_interp.get_interp(self.into())? {
            CustomTypeFull::Real(value) => Ok(value),
            _ => unreachable!(),
        }
    }

    pub fn with_partial_interps(
        self,
        type_interp: &'a PartialTypeInterps,
    ) -> Result<RealTypeFull<'a>, WithPartialInterpsError> {
        match type_interp.get_interp(self.into())? {
            Some(CustomTypeFull::Real(value)) => Ok(value),
            None => Err(MissingTypeInterps {
                missing: vec![self.name().to_string()],
            }
            .into()),
            _ => unreachable!(),
        }
    }
}

impl<'a> StrTypeRef<'a> {
    pub fn with_interps(
        self,
        type_interp: &'a TypeInterps,
    ) -> Result<StrTypeFull<'a>, VocabMismatchError> {
        match type_interp.get_interp(self.into())? {
            CustomTypeFull::Str(value) => Ok(value),
            _ => unreachable!(),
        }
    }

    pub fn with_partial_interps(
        self,
        type_interp: &'a PartialTypeInterps,
    ) -> Result<StrTypeFull<'a>, WithPartialInterpsError> {
        match type_interp.get_interp(self.into())? {
            Some(CustomTypeFull::Str(value)) => Ok(value),
            None => Err(MissingTypeInterps {
                missing: vec![self.name().to_string()],
            }
            .into()),
            _ => unreachable!(),
        }
    }
}

#[duplicate_item(
    ty_name;
    [IntTypeFull];
    [RealTypeFull];
    [StrTypeFull];
)]
mod interp_ref_display {
    #![doc(hidden)]
    use super::*;

    impl FodotOptions for ty_name<'_> {
        type Options<'b> = FormatOptions;
    }

    impl FodotDisplay for ty_name<'_> {
        fn fmt(
            fmt: Fmt<&Self, Self::Options<'_>>,
            f: &mut std::fmt::Formatter<'_>,
        ) -> std::fmt::Result {
            write!(f, "{} ", fmt.value.name())?;
            fmt.options.write_def_eq(f)?;
            write!(f, " {}", fmt.with_format_opts(fmt.value.interp))
        }
    }

    impl Display for ty_name<'_> {
        fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
            write!(f, "{}", self.display())
        }
    }

    display_as_debug!(ty_name<'a>, gen: ('a));
}

impl<'a> From<TypeFull<'a>> for TypeStr {
    fn from(value: TypeFull<'a>) -> Self {
        value.into_type().into()
    }
}

#[cfg(test)]
mod test {
    use crate::fodot::{
        structure::{StrInterp, TypeInterp},
        vocabulary::{Real, VocabSwap, Vocabulary},
    };
    use sli_collections::rc::Rc;

    use super::{IntInterp, RealInterp};

    #[test]
    fn partial_type_interps_vocab_swap_1() {
        let mut vocab1 = Vocabulary::new();
        vocab1.parse("type A").unwrap();
        let mut vocab2 = Vocabulary::new();
        vocab2.parse("type A p: -> A").unwrap();
        let (_, mut type_interps) = vocab1.complete_vocab();
        let vocab2 = Rc::new(vocab2);
        type_interps.swap_vocab(vocab2).unwrap();
    }

    #[test]
    fn partial_type_interps_vocab_swap_2() {
        let mut vocab1 = Vocabulary::new();
        vocab1.parse("type A").unwrap();
        let mut vocab2 = Vocabulary::new();
        vocab2.parse("type A p: -> A").unwrap();
        let (vocab1, mut type_interps) = vocab1.complete_vocab();
        let type_a = vocab1.parse_custom_type("A").unwrap();
        type_interps
            .set_interp(
                type_a,
                TypeInterp::Str(Rc::new(["a", "b", "c"].into_iter().collect())),
            )
            .unwrap();
        let vocab2 = Rc::new(vocab2);
        let type_a = vocab2.parse_custom_type("A").unwrap();
        type_interps.swap_vocab(vocab2.clone()).unwrap();
        let a_interp = type_interps
            .get_interp(type_a)
            .unwrap()
            .unwrap()
            .unwrap_str();
        assert!(
            a_interp
                .interp()
                .iter()
                .map(|f| f.as_ref())
                .eq(["a", "b", "c"])
        );
    }

    #[test]
    fn type_interps_merge_1() {
        let mut vocab = Vocabulary::new();
        vocab.parse("type A <: Int type B <: Real type C").unwrap();
        let (vocab, type_interps) = vocab.complete_vocab();
        let mut type_interps1 = type_interps.clone();
        let mut type_interps2 = type_interps.clone();
        let a = vocab.parse_custom_type("A").unwrap();
        let b = vocab.parse_custom_type("B").unwrap();
        let c = vocab.parse_custom_type("C").unwrap();
        type_interps1
            .set_interp(
                a,
                IntInterp::try_from_iterator([1, 2, 3, 4, 5].into_iter())
                    .unwrap()
                    .into(),
            )
            .unwrap();
        type_interps2
            .set_interp(
                b,
                RealInterp::from_iter([Real::try_from(2.2f32).unwrap()].into_iter()).into(),
            )
            .unwrap();
        type_interps1
            .set_interp(c, StrInterp::from_iter(["a", "b", "c"].into_iter()).into())
            .unwrap();
        type_interps2
            .set_interp(c, StrInterp::from_iter(["a", "b", "c"].into_iter()).into())
            .unwrap();
        type_interps1.merge(&type_interps2).unwrap();
        assert!(
            type_interps1
                .get_interp(a)
                .unwrap()
                .unwrap()
                .unwrap_int()
                .interp()
                .into_iter()
                .eq([1, 2, 3, 4, 5])
        );
        assert!(
            type_interps1
                .get_interp(b)
                .unwrap()
                .unwrap()
                .unwrap_real()
                .interp()
                .into_iter()
                .cloned()
                .eq([Real::try_from(2.2f32).unwrap()].into_iter())
        );
        assert!(
            type_interps1
                .get_interp(c)
                .unwrap()
                .unwrap()
                .unwrap_str()
                .interp()
                .into_iter()
                .map(|f| f.as_ref())
                .eq(["a", "b", "c"].into_iter())
        );
    }

    #[test]
    fn type_interps_merge_2() {
        let mut vocab = Vocabulary::new();
        vocab.parse("type A <: Int type B <: Real type C").unwrap();
        let (vocab, type_interps) = vocab.complete_vocab();
        let mut type_interps1 = type_interps.clone();
        let mut type_interps2 = type_interps.clone();
        let a = vocab.parse_custom_type("A").unwrap();
        let b = vocab.parse_custom_type("B").unwrap();
        let c = vocab.parse_custom_type("C").unwrap();
        type_interps1
            .set_interp(
                a,
                IntInterp::try_from_iterator([1, 2, 3, 4, 5].into_iter())
                    .unwrap()
                    .into(),
            )
            .unwrap();
        type_interps2
            .set_interp(
                b,
                RealInterp::from_iter([Real::try_from(2.2f32).unwrap()].into_iter()).into(),
            )
            .unwrap();
        type_interps2
            .set_interp(c, StrInterp::from_iter(["a", "b", "c"].into_iter()).into())
            .unwrap();
        type_interps1
            .set_interp(c, StrInterp::from_iter(["a", "b"].into_iter()).into())
            .unwrap();
        type_interps1.merge(&type_interps2).unwrap_err();
    }
}
