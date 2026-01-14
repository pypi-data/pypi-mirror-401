use rstest::rstest;
use sli_lib::{
    fodot::{
        structure::{PartialStructure, Precision},
        theory::Inferenceable,
    },
    solver::{Solver, SolverIter, Z3Solver},
};

const MAX_MODELS: usize = 50;

fn check_precision(idp_spec: &str) {
    let inferenceable = Inferenceable::from_specification(idp_spec).unwrap();
    let mut z3_solver = Z3Solver::initialize(&inferenceable);
    let complete_model_iter = z3_solver.iter_models().complete();
    let empty = PartialStructure::new(inferenceable.structure().type_interps_rc().clone());
    for (i, model) in complete_model_iter.take(MAX_MODELS).enumerate() {
        if i > 0 {
            assert!(model.as_ref().is_strictly_more_precise(&empty));
            assert!(empty.is_strictly_less_precise(model.as_ref()));

            assert!(
                inferenceable
                    .structure()
                    .is_strictly_less_precise(model.as_ref())
            );
            assert!(
                model
                    .as_ref()
                    .is_strictly_more_precise(inferenceable.structure())
            );
        } else {
            assert!(model.as_ref().is_more_precise(&empty));
            assert!(empty.is_less_precise(model.as_ref()));

            assert!(inferenceable.structure().is_less_precise(model.as_ref()));
            assert!(model.as_ref().is_more_precise(inferenceable.structure()));
        }
    }

    let mut z3_solver = Z3Solver::initialize(&inferenceable);
    let glob_model_iter = z3_solver.iter_models();
    for (i, model) in glob_model_iter.take(MAX_MODELS).enumerate() {
        if i > 0 {
            assert!(model.as_ref().is_strictly_more_precise(&empty));
            assert!(empty.is_strictly_less_precise(model.as_ref()));

            assert!(
                inferenceable
                    .structure()
                    .is_strictly_less_precise(model.as_ref())
            );
            assert!(
                model
                    .as_ref()
                    .is_strictly_more_precise(inferenceable.structure())
            );
        } else {
            assert!(model.as_ref().is_more_precise(&empty));
            assert!(empty.is_less_precise(model.as_ref()));

            assert!(inferenceable.structure().is_less_precise(model.as_ref()));
            assert!(model.as_ref().is_more_precise(inferenceable.structure()));
        }
    }
}

#[rstest]
fn precision(
    #[files("tests/test_files/**/*.idp")]
    #[mode = str]
    idp_spec: &str,
) {
    check_precision(idp_spec);
}
