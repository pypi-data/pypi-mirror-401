use clap::{Parser, Subcommand, ValueEnum};
use itertools::Itertools;
use sli_lib::fodot::TryIntoCtx;
use sli_lib::fodot::knowledge_base::KnowledgeBase;
use sli_lib::fodot::structure::Args;
use sli_lib::fodot::theory::Inferenceable;
use sli_lib::fodot::vocabulary::Vocabulary;
use sli_lib::solver::Z3Solver;
use sli_lib::solver::{InterpMethod, Solver, SolverIter, TimeMeasurements, Timings};
use std::ffi::OsString;
use std::fmt::{self, Display};
use std::io::Read;
use std::time::Duration;
use std::{process::exit, time::Instant};

#[derive(Debug, Parser)]
#[command(name = "sli", version = sli_lib::VERSION, about, long_about = None)]
struct Cli {
    #[command(subcommand)]
    sub_commands: SubCommands,
}

#[derive(Debug, Copy, Clone, PartialEq, Eq, PartialOrd, Ord, ValueEnum)]
enum InterpMode {
    /// Use satisfying set interpretation.
    Satset,
    /// Use naive interpretation.
    Naive,
    /// Don't reduce.
    NoReduc,
}

#[derive(Debug, Subcommand)]
enum SubCommands {
    #[command(flatten)]
    Inference(Inferences),
    /// Execute a procedure in a knowledge base
    Exec {
        #[arg(long, default_value = "main")]
        /// Default procedure main to execute
        procedure: String,
        #[arg(long, default_value = "python3", env = "SLI_PYTHON_INTERPRETER")]
        /// Execute the procedure with the given python interpreter
        interpreter: String,
        /// Path to knowledge base to use.
        ///
        /// With no FILE, or when FILE is -, read standard input.
        file: Option<String>,
    },
}

#[derive(Debug, Subcommand)]
enum Inferences {
    /// Model expansion
    Expand {
        #[arg(long, default_value_t = 2)]
        /// Amount of models to expand
        models: usize,
        #[command(flatten)]
        options: InferenceOptions,
    },
    /// Backbone propagation
    Propagate {
        #[arg(long)]
        /// Also shows given assignments instead of only new assignments.
        all: bool,
        #[command(flatten)]
        options: InferenceOptions,
    },
    /// Complete propagation of a single applied symbol
    #[command(visible_alias = "get-range")]
    PossibleValues {
        /// Applied symbol to propagate.
        applied_symbol: String,
        #[arg(long, value_enum, default_value_t = GetRangeFormat::True)]
        /// What kind of range to display.
        kind: GetRangeFormat,
        #[command(flatten)]
        options: InferenceOptions,
    },
}

#[derive(Debug, Copy, Clone, PartialEq, Eq, PartialOrd, Ord, ValueEnum)]
enum GetRangeFormat {
    /// Show possibly trues.
    True,
    /// Show certainly falses.
    False,
}

#[derive(Debug, Parser, Clone)]
struct InferenceOptions {
    /// Path to knowledge base to use.
    ///
    /// With no FILE, or when FILE is -, read standard input.
    file: Option<String>,
    /// Blocks to apply the inference task on, these must be logical blocks.
    ///
    /// Can be used multiple times, merges all given blocks together.
    ///
    /// When no blocks are given then an inference task is executed if the given knowledge base
    /// contains only one vocabulary block, one theory block and one structure block.
    #[arg(short, long)]
    block: Vec<String>,
    #[arg(long, global = true)]
    /// Print smtlib grounding.
    smt: bool,
    #[arg(long, global=true, value_enum, default_value_t = InterpMode::Satset)]
    /// Processing step.
    interp_mode: InterpMode,
    #[arg(long, global = true)]
    /// Print timings of each step.
    print_timings: bool,
}

impl Inferences {
    fn options(&self) -> &InferenceOptions {
        match self {
            Self::Expand { options, .. }
            | Self::Propagate { options, .. }
            | Self::PossibleValues { options, .. } => options,
        }
    }
}

pub enum InferenceTask<'a> {
    Expand,
    Propagate,
    GetRange { pfunc: &'a str, args: Vec<&'a str> },
}

struct ErrValue {
    err: Option<Box<dyn Display>>,
    code: i32,
}

impl<T: Display + 'static> From<T> for ErrValue {
    fn from(value: T) -> Self {
        Self {
            err: Some(Box::new(value)),
            code: 1,
        }
    }
}

impl ErrValue {
    fn from_code(code: i32) -> Self {
        Self { err: None, code }
    }
}

pub fn main(do_exit: bool) -> i32 {
    let cli = if do_exit {
        Ok(Cli::parse())
    } else {
        Cli::try_parse()
    };
    _main_catch(cli, do_exit)
}

pub fn main_from<I, T>(do_exit: bool, args: I) -> i32
where
    I: IntoIterator<Item = T>,
    T: Into<OsString> + Clone,
{
    let cli = if do_exit {
        Ok(Cli::parse_from(args))
    } else {
        Cli::try_parse_from(args)
    };
    _main_catch(cli, do_exit)
}

fn _main_catch(cli: Result<Cli, clap::Error>, do_exit: bool) -> i32 {
    let cli = match cli {
        Ok(value) => value,
        Err(value) => {
            eprintln!("sli: {}", value);
            return value.exit_code();
        }
    };
    match _main(cli, do_exit) {
        Ok(_) => exit(0),
        Err(value) => {
            if let Some(err) = value.err {
                eprintln!("sli: {}", err);
            }
            exit(value.code);
        }
    }
}

fn _main(cli: Cli, do_exit: bool) -> Result<(), ErrValue> {
    let inference = match cli.sub_commands {
        SubCommands::Exec {
            procedure,
            interpreter,
            file,
        } => {
            let python_exec = "\
import sys
try:
\timport sli_lib
except ModuleNotFoundError:
\tprint(\
        (\
            \"error: module `sli_lib` is not installed in this Python interpreter.\\n\"\
            \"Consider installing the library or specifying a Python interpreter with the library installed using `--interpeter` or the `SLI_PYTHON_INTERPRETER` environment variable\"\
        )\
)
\texit(1)
sli_lib._exec(*sys.argv[1:])\
            ";
            let result = match std::process::Command::new(&interpreter)
                .arg("-c")
                .arg(python_exec)
                .arg(&procedure)
                .arg(file.as_deref().unwrap_or("-"))
                .spawn()
            {
                Ok(mut child) => child
                    .wait()
                    .expect("our child has been reaped by someone elses hands!!!"),
                Err(err) => {
                    eprintln!("Error: calling '{}', failed with '{}'", interpreter, err);
                    let exit_code = 1;
                    if do_exit {
                        exit(exit_code);
                    } else {
                        return Err(ErrValue::from_code(exit_code));
                    }
                }
            };
            if !result.success() {
                let exit_code = 1;
                if do_exit {
                    exit(exit_code);
                } else {
                    return Err(ErrValue::from_code(exit_code));
                }
            } else {
                exit(0);
            }
        }
        SubCommands::Inference(inference) => inference,
    };
    let mut time_measurer = TimeMeasurer::new();
    let parse_timer = time_measurer.parse.start();
    if let Inferences::PossibleValues { applied_symbol, .. } = &inference {
        if inference.options().file.is_none() && !applied_symbol.contains('(') {
            eprintln!(
                "Warning: get range applied symbol input '{}', looks like a path.",
                applied_symbol
            );
            eprintln!("Warning: Reading from stdin may not be your intention ...");
        }
    }
    let kb_source = match inference.options().file.as_deref() {
        Some("-") | None => {
            let mut buffer = String::new();
            std::io::stdin()
                .read_to_string(&mut buffer)
                .map_err(|f| format!("{}", f))?;
            buffer
        }
        Some(path) => std::fs::read_to_string(path).map_err(|f| format!("{}: {}", path, f))?,
    };
    let dyn_kb = &kb_source.as_str();
    let inferenceable = if inference.options().block.is_empty() {
        match Inferenceable::from_specification(&kb_source) {
            Ok(value) => value,
            Err(err) => {
                eprintln!("{}", err.with_source(dyn_kb));
                let exit_code = 1;
                if do_exit {
                    exit(exit_code);
                } else {
                    return Err(ErrValue::from_code(exit_code));
                }
            }
        }
    } else {
        let kb = match KnowledgeBase::new(&kb_source, Default::default()) {
            Ok(kb) => kb,
            Err(diag) => {
                eprintln!("{}", diag.with_source(dyn_kb));
                let exit_code = 1;
                if do_exit {
                    exit(exit_code);
                } else {
                    return Err(ErrValue::from_code(exit_code));
                }
            }
        };
        match kb.theory_from_blocks_diags(inference.options().block.iter().map(|f| f.as_str())) {
            Ok(value) => value,
            Err(err) => {
                eprintln!("{}", err.with_source(dyn_kb));
                let exit_code = 1;
                if do_exit {
                    exit(exit_code);
                } else {
                    return Err(ErrValue::from_code(exit_code));
                }
            }
        }
    };
    let ground_transform = match inference.options().interp_mode {
        InterpMode::Satset => InterpMethod::SatisfyingSetInterp,
        InterpMode::Naive => InterpMethod::NaiveInterp,
        InterpMode::NoReduc => InterpMethod::NoInterp,
    };
    let parse_time = parse_timer.end().as_secs_f32();
    if inference.options().print_timings {
        eprintln!("{} - parse done", parse_time);
    }

    let mut z3_solver =
        Z3Solver::initialize_with_timing(&inferenceable, ground_transform, &mut time_measurer);
    let ground_time = time_measurer.ground.get_time().as_secs_f32();
    let tranform_time = time_measurer.transform.get_time().as_secs_f32();
    if inference.options().print_timings {
        eprintln!("{} - transform done", tranform_time);
        eprintln!("{} - ground done", ground_time);
    }
    if inference.options().smt {
        println!("{:}", z3_solver.get_smtlib());
    }

    let solve_timer = time_measurer.solve.start();
    match &inference {
        Inferences::Expand {
            models: max_models, ..
        } => {
            let max_models = *max_models;
            let complete_model_iter = z3_solver.iter_models().complete().take(max_models);
            let mut number_models = 0;
            for (i, model) in complete_model_iter.enumerate() {
                println!("=== Model {} ===\n{}", i + 1, model);
                number_models = i + 1;
            }
            if number_models == 0 {
                println!("Theory is unsatisfiable.");
            } else if number_models != max_models {
                println!("No more models.");
            } else {
                println!("More models may be available.");
            }
        }
        Inferences::Propagate { all, .. } => {
            let consequences = if *all {
                z3_solver.propagate()
            } else {
                z3_solver.propagate_diff()
            };
            match consequences {
                Some(x) => println!("{}", x),
                None => println!("Theory is unsatisfiable."),
            };
        }
        Inferences::PossibleValues {
            applied_symbol,
            kind,
            ..
        } => {
            let (pfunc, args) = {
                let l_paran = applied_symbol
                    .find("(")
                    .ok_or("error when parsing applied symbol")?;
                let pfunc = applied_symbol[..l_paran].trim();
                let r_paran = applied_symbol
                    .find(")")
                    .ok_or("error when parsing applied symbol")?;
                if applied_symbol[r_paran..].trim() != ")" {
                    return Err("error when parsing applied symbol".into());
                }
                let args = applied_symbol[l_paran + 1..r_paran]
                    .split(',')
                    .map(|f| f.trim())
                    .collect::<Vec<_>>();
                let args = if let &[""] = args.as_slice() {
                    Vec::new()
                } else {
                    args
                };
                (pfunc, args)
            };
            let pfunc_rc = Vocabulary::parse_pfunc_rc(z3_solver.inferenceable().vocab_rc(), pfunc)
                .map_err(|f| format!("{}: {}", applied_symbol, f))?;
            let type_interps = z3_solver.inferenceable().type_interps_rc().clone();
            let args = args
                .iter()
                .copied()
                .try_into_ctx(
                    pfunc_rc
                        .domain()
                        .with_interps(type_interps.as_ref())
                        .unwrap(),
                )
                .map_err(|f| format!("{}: {}", applied_symbol, f))?;
            let cf = z3_solver
                .get_range(pfunc_rc, Args::clone(&args))
                .map_err(|f| format!("{}", f))?;
            if let Some(mut cf) = cf {
                let out = match kind {
                    GetRangeFormat::True => {
                        cf.negate();
                        true
                    }
                    GetRangeFormat::False => false,
                };
                println!(
                    "{}({}) {} {{{}}}",
                    pfunc,
                    args.iter().format(","),
                    sli_lib::fodot::fmt::SUPERSET_ASCII,
                    cf.iter()
                        .map(|arg| display_fn(move |f| write!(f, "{} -> {}", arg, out)))
                        .format(", ")
                );
            } else {
                println!("Theory is unsatisfiable");
            }
        }
    }
    let solve_time = solve_timer.end().as_secs_f32();

    if inference.options().print_timings {
        eprintln!(
            "\nParse: {} | Transform: {} | Ground: {} | Solve: {}",
            parse_time, tranform_time, ground_time, solve_time
        );
    }
    if do_exit {
        // exit makes it so we don't have to do any cleanup of resources ourselves which is faster
        exit(0);
    }
    Ok(())
}

#[derive(Debug, Clone, Copy, Default)]
pub enum Timer {
    #[default]
    None,
    Duration(Duration),
    Instant(Instant),
}

impl Timer {
    pub fn start_measurement(&mut self) {
        *self = Timer::Instant(Instant::now());
    }

    pub fn start(&mut self) -> TimerEnder {
        self.start_measurement();
        TimerEnder { timer: self }
    }

    pub fn end(&mut self) -> Duration {
        match self {
            Timer::Instant(inst) => {
                let elapsed = inst.elapsed();
                *self = Timer::Duration(elapsed);
                elapsed
            }
            _ => Default::default(),
        }
    }

    pub fn duration_or(&self, value: Duration) -> Duration {
        match self {
            Timer::Duration(dur) => *dur,
            _ => value,
        }
    }

    pub fn get_time(&self) -> Duration {
        self.duration_or(Default::default())
    }

    pub fn expect_instant(&self, msg: &str) -> Instant {
        match self {
            Timer::Instant(inst) => *inst,
            _ => panic!("{msg}"),
        }
    }
}

pub struct TimerEnder<'a> {
    timer: &'a mut Timer,
}

impl TimerEnder<'_> {
    /// End timing
    pub fn end(self) -> Duration {
        let ret = self.timer.end();
        std::mem::forget(self);
        ret
    }
}

impl Drop for TimerEnder<'_> {
    fn drop(&mut self) {
        self.timer.end();
    }
}

#[derive(Debug, Default)]
pub struct TimeMeasurer {
    parse: Timer,
    transform: Timer,
    ground: Timer,
    solve: Timer,
}

impl TimeMeasurer {
    pub fn new() -> Self {
        Default::default()
    }
}

impl Timings for TimeMeasurer {
    fn start_measurement(&mut self, measure: TimeMeasurements) {
        match measure {
            TimeMeasurements::Transform => self.transform.start_measurement(),
            TimeMeasurements::Grounding => self.ground.start_measurement(),
        }
    }

    fn end_measurement(&mut self, measure: TimeMeasurements) {
        match measure {
            TimeMeasurements::Transform => {
                self.transform.end();
            }
            TimeMeasurements::Grounding => {
                self.ground.end();
            }
        }
    }
}

pub(crate) fn display_fn(f: impl FnOnce(&mut fmt::Formatter<'_>) -> fmt::Result) -> impl Display {
    struct WithFormatter<F>(core::cell::Cell<Option<F>>);

    impl<F> Display for WithFormatter<F>
    where
        F: FnOnce(&mut fmt::Formatter<'_>) -> fmt::Result,
    {
        fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
            (self.0.take()).unwrap()(f)
        }
    }

    WithFormatter(core::cell::Cell::new(Some(f)))
}

#[test]
fn verify_cli() {
    use clap::CommandFactory;
    Cli::command().debug_assert();
}
