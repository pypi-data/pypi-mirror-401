//! Data structure used to aggregate errors from parsing.

use super::SliError;
use crate::{
    ast::{self, LinesIter, Span},
    fodot::fmt::{FodotDisplay, FodotOptions, FormatOptions},
};
use itertools::Itertools;
use std::fmt::Display;
use std::{
    error::Error,
    fmt::{Debug, Write},
};

/// A span with some text.
#[allow(unused)]
#[derive(Debug, Clone)]
pub struct LabeledSpan {
    label: String,
    span: Span,
}

impl LabeledSpan {
    pub fn new(label: String, span: Span) -> Self {
        Self { label, span }
    }
}

/// An error with a corresponding span.
#[derive(Debug, Clone)]
pub struct IDPError {
    error: SliError,
    span: Option<Span>,
    secondary_labels: Vec<LabeledSpan>,
    #[allow(unused)]
    #[cfg(all(debug_assertions, feature = "std"))]
    backtrace: backtrace::Backtrace,
}

impl IDPError {
    pub fn new_with_span(error: SliError, span: Span) -> Self {
        Self {
            error,
            span: Some(span),
            secondary_labels: Default::default(),
            #[cfg(all(debug_assertions, feature = "std"))]
            backtrace: backtrace::Backtrace(std::backtrace::Backtrace::capture().into()),
        }
    }

    pub fn new(error: SliError) -> Self {
        Self {
            error,
            span: Default::default(),
            secondary_labels: Default::default(),
            #[cfg(all(debug_assertions, feature = "std"))]
            backtrace: backtrace::Backtrace(std::backtrace::Backtrace::capture().into()),
        }
    }

    pub fn with_span(mut self, span: Span) -> Self {
        self.span = Some(span);
        self
    }

    pub fn add_label(mut self, label: LabeledSpan) -> Self {
        self.secondary_labels.push(label);
        self
    }

    pub fn set_labels(&mut self, labels: Vec<LabeledSpan>) {
        self.secondary_labels = labels;
    }

    pub fn span(&self) -> Option<&Span> {
        self.span.as_ref()
    }

    fn display_with_source(
        &self,
        f: &mut core::fmt::Formatter<'_>,
        source: &dyn ast::Source,
        new_lines: &NewLineMap,
    ) -> core::fmt::Result {
        writeln!(f, "{}", self.error)?;
        if let Some(span) = self.span {
            write_span_with_message(&span, f, source, new_lines, None)?;
        }
        if !self.secondary_labels.is_empty() {
            writeln!(f)?;
        }
        let mut labels = self.secondary_labels.iter().peekable();
        while let Some(label) = labels.next() {
            writeln!(f, "note: {}", &label.label)?;
            write_span_with_message(&label.span, f, source, new_lines, None)?;
            if labels.peek().is_some() {
                writeln!(f)?;
            }
        }
        Ok(())
    }
}

fn write_span_with_message(
    span: &Span,
    f: &mut core::fmt::Formatter<'_>,
    source: &dyn ast::Source,
    new_lines: &NewLineMap,
    message: Option<fn(&mut core::fmt::Formatter) -> core::fmt::Result>,
) -> core::fmt::Result {
    let begin_line = new_lines.til_prev_new_line(span.start);
    let end_line = new_lines.til_next_new_line(span.end);
    let begin_line_nr = begin_line.map(|f| new_lines.line_number(f)).unwrap_or(0) + 1;
    let is_multi_line = begin_line
        .map(|f| new_lines.til_next_new_line(f) != end_line)
        .unwrap_or(false);
    let diag_span = Span {
        start: begin_line.unwrap_or(0),
        end: end_line.unwrap_or(source.len()),
    };

    if is_multi_line {
        let end_line_nr = end_line
            .map(|f| new_lines.line_number(f))
            .unwrap_or_else(|| new_lines.new_lines.len())
            + 1;
        let max_digit_count = end_line_nr.ilog10() + 1;
        let mut lines = LinesIter::new(source, &diag_span)
            .zip(begin_line_nr..)
            .peekable();
        let mut last_span = None;
        while let Some((line, line_nr)) = lines.next() {
            let this_digit_count = line_nr.ilog10() + 1;
            write!(f, "{line_nr} ")?;
            write!(
                f,
                "{:^<1$}",
                "",
                (max_digit_count - this_digit_count) as usize
            )?;
            write!(f, "| ")?;
            source.write_slice(&line, f)?;
            if lines.peek().is_some() {
                writeln!(f)?;
            } else {
                last_span = Some(line);
            }
        }
        let last_span = last_span.expect("we confirmed there is more than 1 line");
        writeln!(f)?;
        let mut width_writer = WidthWriter::new(VoidWriter);
        _ = source.write_slice(
            &Span {
                start: last_span.start,
                end: span.end,
            },
            &mut width_writer,
        );
        let width = width_writer.accum;
        write!(
            f,
            "{: <2$} \\{:_<3$}^",
            "", "", max_digit_count as usize, width,
        )?;
        if let Some(message) = message {
            f.write_char(' ')?;
            message(f)?;
        }
    } else {
        let digit_count = begin_line_nr.ilog10() + 1;
        write!(f, "{begin_line_nr} ")?;
        const PREAMBLE: &str = "| ";
        write!(f, "{}", PREAMBLE)?;
        source.write_slice(&diag_span, f)?;
        let mut width_writer = WidthWriter::new(VoidWriter);
        _ = source.write_slice(
            &Span {
                start: diag_span.start,
                end: span.start,
            },
            &mut width_writer,
        );
        let chars_pre = width_writer.accum;
        write!(f, "\n{: <1$} {2}", "", digit_count as usize, PREAMBLE)?;
        write!(f, "{: <1$}", "", chars_pre)?;
        let length = span.end - span.start;
        let mut width_writer = WidthWriter::new(VoidWriter);
        _ = source.write_slice(span, &mut width_writer);
        let chars_in = width_writer.accum;
        if length == 0 {
            write!(f, "{:^<1$}", "", 1)?;
        } else {
            write!(f, "{:^<1$}", "", chars_in)?;
        }
        if let Some(message) = message {
            f.write_char(' ')?;
            message(f)?;
        }
    }
    Ok(())
}

impl FodotOptions for IDPError {
    type Options<'a> = FormatOptions;
}

impl FodotDisplay for IDPError {
    fn fmt(
        fmt: crate::fodot::fmt::Fmt<&Self, Self::Options<'_>>,
        f: &mut std::fmt::Formatter<'_>,
    ) -> std::fmt::Result {
        if let Some(span) = fmt.value.span {
            write!(f, "from {} to {}: ", span.start, span.end)?;
        }
        write!(f, "{}", fmt.with_format_opts(&fmt.value.error))
    }
}

impl Display for IDPError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.display())
    }
}

impl Error for IDPError {}

#[derive(Debug, Clone)]
/// A builder for [Diagnostics].
pub struct DiagnosticsBuilder {
    errors: Vec<IDPError>,
}

impl Default for DiagnosticsBuilder {
    fn default() -> Self {
        Self::new()
    }
}

impl DiagnosticsBuilder {
    pub fn new() -> Self {
        Self {
            errors: Default::default(),
        }
    }

    pub fn add_error(&mut self, error: IDPError) {
        self.errors.push(error)
    }

    pub fn errors(&self) -> &[IDPError] {
        &self.errors
    }

    pub fn append_builder(&mut self, errors: &mut DiagnosticsBuilder) {
        self.errors.append(&mut errors.errors);
    }

    pub fn append_diag(&mut self, mut errors: Diagnostics) {
        self.errors.append(&mut errors.errors);
    }

    pub fn finish(self) -> Result<Diagnostics, DiagnosticsBuilder> {
        if !self.errors.is_empty() {
            Ok(Diagnostics {
                errors: self.errors,
            })
        } else {
            Err(self)
        }
    }

    pub fn finish_with(mut self, error: IDPError) -> Diagnostics {
        self.errors.push(error);
        Diagnostics {
            errors: self.errors,
        }
    }
}

/// A collection of [IDPError]s.
///
/// always contains at least one error.
#[derive(Debug, Clone)]
pub struct Diagnostics {
    errors: Vec<IDPError>,
}

impl Diagnostics {
    pub fn new(first_error: IDPError) -> Self {
        Self {
            errors: vec![first_error],
        }
    }

    pub fn add_error(&mut self, error: IDPError) {
        self.errors.push(error)
    }

    pub fn errors(&self) -> &[IDPError] {
        &self.errors
    }

    pub fn into_builder(self) -> DiagnosticsBuilder {
        DiagnosticsBuilder {
            errors: self.errors,
        }
    }

    pub fn with_source<'a>(&'a self, source: &'a dyn ast::Source) -> SourceDiagnostics<'a> {
        SourceDiagnostics {
            printer: SourceErrorPrinter {
                source,
                new_line_map: NewLineMap::new(source),
            },
            diag: self,
        }
    }
}

impl From<Diagnostics> for DiagnosticsBuilder {
    fn from(value: Diagnostics) -> Self {
        value.into_builder()
    }
}

impl Display for Diagnostics {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.errors().iter().format("\n"))
    }
}

/// A [Diagnostics] combined with a [ast::Source].
///
/// Used for pretty printing errors.
#[derive(Debug, Clone)]
pub struct SourceDiagnostics<'a> {
    printer: SourceErrorPrinter<'a>,
    diag: &'a Diagnostics,
}

impl<'a> SourceDiagnostics<'a> {
    pub fn take_printer(self) -> SourceErrorPrinter<'a> {
        self.printer
    }
}

#[derive(Clone)]
pub struct SourceErrorPrinter<'a> {
    source: &'a dyn ast::Source,
    new_line_map: NewLineMap,
}

impl Debug for SourceErrorPrinter<'_> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let SourceErrorPrinter {
            source: _,
            new_line_map,
        } = self;
        f.debug_struct("SourceErrorPrinter")
            .field("source", &"...")
            .field("new_line_map", &new_line_map)
            .finish()
    }
}

impl<'a> SourceErrorPrinter<'a> {
    pub fn new(source: &'a dyn ast::Source) -> Self {
        Self {
            source,
            new_line_map: NewLineMap::new(source),
        }
    }

    pub fn fmt_diagnostics<'b>(self, diag: &'b Diagnostics) -> SourceDiagnostics<'b>
    where
        'a: 'b,
    {
        SourceDiagnostics {
            printer: self,
            diag,
        }
    }

    pub fn fmt_error<'b>(&'b self, error: &'b IDPError) -> SourceErrorFmt<'b> {
        SourceErrorFmt {
            error,
            printer: self,
        }
    }
}

pub struct SourceErrorFmt<'a> {
    error: &'a IDPError,
    printer: &'a SourceErrorPrinter<'a>,
}

impl Display for SourceErrorFmt<'_> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        self.error
            .display_with_source(f, self.printer.source, &self.printer.new_line_map)
    }
}

/// A mapping of source newlines.
#[derive(Debug, Clone)]
struct NewLineMap {
    new_lines: Box<[usize]>,
    is_dos: bool,
}

impl NewLineMap {
    fn new(source: &dyn ast::Source) -> Self {
        let Some(first) = source.next_char_pos(0, '\n') else {
            return NewLineMap {
                new_lines: [].into(),
                is_dos: false,
            };
        };
        let mut new_lines = vec![first];
        let is_dos = source.prev_char(first) == Some('\r');
        let Some(mut cur) = first.checked_add(1) else {
            return NewLineMap {
                new_lines: new_lines.into(),
                is_dos,
            };
        };
        while let Some(next) = source.next_char_pos(cur, '\n') {
            new_lines.push(next);
            if let Some(cur_new) = next.checked_add(1) {
                cur = cur_new;
            } else {
                return NewLineMap {
                    new_lines: new_lines.into(),
                    is_dos,
                };
            };
        }

        NewLineMap {
            new_lines: new_lines.into(),
            is_dos,
        }
    }

    fn til_next_new_line(&self, pos: usize) -> Option<usize> {
        let res = self.new_lines.partition_point(|&f| f < pos);
        if res < self.new_lines.len() {
            Some(self.new_lines[res] - self.till_value())
        } else {
            None
        }
    }

    fn til_prev_new_line(&self, pos: usize) -> Option<usize> {
        let res = self.new_lines.partition_point(|&f| f < pos);
        if res < self.new_lines.len() {
            Some(self.new_lines[res.checked_sub(1)?] + 1)
        } else {
            None
        }
    }

    fn line_number(&self, pos: usize) -> usize {
        self.new_lines.partition_point(|&f| f < pos)
    }

    fn till_value(&self) -> usize {
        if self.is_dos { 1 } else { 0 }
    }
}

impl Display for SourceDiagnostics<'_> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let mut errors = self.diag.errors.iter().peekable();
        while let Some(error) = errors.next() {
            write!(f, "error: {}", self.printer.fmt_error(error))?;
            if errors.peek().is_some() {
                writeln!(f)?;
                writeln!(f)?;
            }
        }
        Ok(())
    }
}

pub(crate) fn to_ordinal_numeral(value: usize) -> String {
    match value {
        1 => "first".to_string(),
        2 => "second".to_string(),
        3 => "third".to_string(),
        rest => format!("{}th", rest),
    }
}

/// A writer that keeps track of the width that has been written.
///
/// Uses [unicode_width] as width of Unicode characters.
pub struct WidthWriter<W: core::fmt::Write> {
    pub writer: W,
    pub accum: usize,
}

impl<W: core::fmt::Write> WidthWriter<W> {
    pub fn new(writer: W) -> Self {
        Self { writer, accum: 0 }
    }
}

impl<W: core::fmt::Write> core::fmt::Write for WidthWriter<W> {
    fn write_str(&mut self, s: &str) -> std::fmt::Result {
        self.accum += unicode_width::UnicodeWidthStr::width(s);
        self.writer.write_str(s)?;
        Ok(())
    }

    fn write_char(&mut self, c: char) -> std::fmt::Result {
        self.accum += unicode_width::UnicodeWidthChar::width(c).unwrap_or(0);
        self.writer.write_char(c)?;
        Ok(())
    }
}

/// A writer that discards anything that is being written to it.
///
/// Useful when used together with a [WidthWriter].
pub struct VoidWriter;

impl core::fmt::Write for VoidWriter {
    fn write_str(&mut self, _: &str) -> std::fmt::Result {
        Ok(())
    }

    fn write_char(&mut self, _: char) -> std::fmt::Result {
        Ok(())
    }

    fn write_fmt(&mut self, _: std::fmt::Arguments<'_>) -> std::fmt::Result {
        Ok(())
    }
}

#[cfg(all(debug_assertions, feature = "std"))]
mod backtrace {
    use std::fmt::Display;

    #[derive(Debug)]
    pub struct Backtrace(pub Option<std::backtrace::Backtrace>);

    impl Display for Backtrace {
        fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
            if let Some(backtrace) = &self.0 {
                write!(f, "{}", backtrace)?;
            }
            Ok(())
        }
    }

    impl Clone for Backtrace {
        fn clone(&self) -> Self {
            Self(None)
        }
    }
}
