use sli_collections::rc::Rc;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
#[non_exhaustive]
pub enum ProcedureLang {
    Python,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Procedure {
    pub lang: ProcedureLang,
    pub name: Rc<str>,
    pub args: Box<[Box<str>]>,
    pub content: Box<str>,
}
