# Copyright 2021 IRT Saint Exupéry, https://www.irt-saintexupery.com
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License version 3 as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest
from gemseo import configure_logger
from gemseo import create_discipline
from gemseo import create_scenario
from gemseo.algos.opt.factory import OptimizationLibraryFactory
from gemseo.problems.mdo.sellar.sellar_design_space import SellarDesignSpace
from gemseo.problems.mdo.sobieski.core.problem import SobieskiProblem
from gemseo.problems.optimization.rosenbrock import Rosenbrock

from gemseo_pyoptsparse.algos.opt._py_opt_sparse_functions import PyOptSparseFunctions
from gemseo_pyoptsparse.algos.opt.settings.slsqp import SLSQP_Settings
from gemseo_pyoptsparse.algos.opt.settings.snopt import SNOPT_Settings


@pytest.fixture(params=["user", "finite_differences"])
def sobieski_optim_problem(request):
    """Build sobieski optimization problem."""
    disciplines = create_discipline([
        "SobieskiPropulsion",
        "SobieskiAerodynamics",
        "SobieskiMission",
        "SobieskiStructure",
    ])
    design_space = SobieskiProblem().design_space
    scenario = create_scenario(
        disciplines,
        formulation_name="IDF",
        maximize_objective=True,
        objective_name="y_4",
        design_space=design_space,
    )
    scenario.set_differentiation_method(request.param)
    for constraint in ["g_1", "g_2", "g_3"]:
        scenario.add_constraint(constraint, "ineq")

    return scenario.formulation.optimization_problem


@pytest.fixture
def sellar_optim_problem():
    """Build Sellar optimizatio problem."""
    disciplines = create_discipline(["Sellar1", "Sellar2", "SellarSystem"])
    design_space = SellarDesignSpace()
    scenario = create_scenario(
        disciplines, formulation="MDF", objective_name="obj", design_space=design_space
    )
    scenario.set_differentiation_method("user")
    # scenario.set_differentiation_method("finite_differences")
    scenario.add_constraint("c_1", "ineq")
    scenario.add_constraint("c_2", "ineq")

    return scenario.formulation.optimization_problem


def test_standalone():
    """Test pyoptsparse as standalone.

    Just make sure it can be correctly executed.
    """
    import pyoptsparse

    def objfunc(xdict):
        x = xdict["xvars"]
        funcs = {}
        funcs["obj"] = -x[0] * x[1] * x[2]
        conval = [0] * 2
        conval[0] = x[0] + 2.0 * x[1] + 2.0 * x[2] - 72.0
        conval[1] = -x[0] - 2.0 * x[1] - 2.0 * x[2]
        funcs["con"] = conval
        fail = False

        return funcs, fail

    opt_prob = pyoptsparse.Optimization("TP037", objfunc)
    opt_prob.addVarGroup("xvars", 3, "c", lower=[0, 0, 0], upper=[42, 42, 42], value=10)
    opt_prob.addConGroup("con", 2, lower=None, upper=0.0)
    opt_prob.addObj("obj")
    opt = pyoptsparse.SLSQP(options={"IPRINT": -1})
    sol = opt(opt_prob, sens="FD")
    assert sol


@pytest.fixture
def pyopt_functions_no_jac():
    """Build and return a pyOptparseFunctions instance without jacobians."""
    pyopt_functions = PyOptSparseFunctions("inputs")
    pyopt_functions.add_function("obj", lambda x: 2 * x + 3)
    pyopt_functions.add_function("con1", lambda x: x[0] ** 2)
    pyopt_functions.add_function("con2", lambda x: np.sqrt(x))
    return pyopt_functions


@pytest.fixture
def pyopt_functions_with_jac():
    """Build and return a pyOptparseFunctions instance with jacobians."""
    pyopt_functions = PyOptSparseFunctions("inputs")
    pyopt_functions.add_function("obj", lambda x: 2 * x + 3, lambda x: 2)
    pyopt_functions.add_function("con1", lambda x: x[0] ** 2, lambda x: 2 * x[0])
    pyopt_functions.add_function(
        "con2", lambda x: np.sqrt(x), lambda x: 0.5 / np.sqrt(x)
    )
    return pyopt_functions


@pytest.mark.parametrize(
    ("input_data", "ref"),
    [
        (
            {"inputs": np.array([1, 4, 9])},
            (
                {
                    "obj": np.array([5, 11, 21]),
                    "con1": np.array([1]),
                    "con2": np.array([1, 2, 3]),
                },
                False,
            ),
        ),
        (
            {"inputs": np.array([-1, 4, 9])},
            (
                {
                    "obj": np.array([1, 11, 21]),
                    "con1": np.array([1]),
                    "con2": np.array([np.nan, 2, 3]),
                },
                True,
            ),
        ),
    ],
)
def test_pyopt_functions_call(pyopt_functions_no_jac, input_data, ref):
    """Test that pyOptSparseFuctions is correctly called without jacobians."""
    output, is_fail = pyopt_functions_no_jac.compute_outputs(input_data)

    assert is_fail == ref[1]
    for name, value in output.items():
        assert value == pytest.approx(ref[0][name], nan_ok=True)


@pytest.mark.parametrize(
    ("input_data", "ref"),
    [
        (
            {"inputs": np.array([1, 4, 9])},
            (
                {
                    "obj": np.array([2]),
                    "con1": np.array([2]),
                    "con2": np.array([0.5, 0.25, 0.5 * 1 / 3]),
                },
                False,
            ),
        ),
        (
            {"inputs": np.array([-1, 4, 9])},
            (
                {
                    "obj": np.array([2]),
                    "con1": np.array([-2]),
                    "con2": np.array([np.nan, 0.25, 0.5 * 1 / 3]),
                },
                True,
            ),
        ),
    ],
)
def test_pyopt_functions_jac(pyopt_functions_with_jac, input_data, ref):
    """Test that pyOptSparseFuctions jacobian is correctly called."""
    output, is_fail = pyopt_functions_with_jac.compute_jacobian(input_data)

    assert is_fail == ref[1]
    for name, value in output.items():
        assert value["inputs"] == pytest.approx(ref[0][name], nan_ok=True)


def test_pyopt_functions_with_bad_input_name(pyopt_functions_no_jac):
    """Test that an error is raised if pyOptSparseFunctions is called with a bad input
    name."""
    with pytest.raises(KeyError, match="'inputs'"):
        pyopt_functions_no_jac.compute_outputs({"var": np.array([1, 2, 3])})


@pytest.fixture(
    params=[
        (
            SLSQP_Settings,
            {"options_file": "options.out", "IFILE": "slsqp.out", "IPRINT": 1},
        ),
        (
            SNOPT_Settings,
            {
                "options_file": "options.out",
                "Print file": "print.out",
                "Summary file": "sum.out",
                "iPrint": 1,
                "iSumm": 1,
            },
        ),
    ]
)
def settings_model_for_rosenbrock(tmp_path, request):
    """Different algo to be tested.

    Generated files are mocked to be written into the tmp_path.

    Returns:
        The model of the algo.
    """  # noqa: D205, D212, D415
    options = {
        "max_iter": 100,
        "normalize_design_space": False,
        "ftol_rel": 1e-9,
        "ftol_abs": 1e-9,
        "xtol_rel": 1e-9,
        "xtol_abs": 1e-9,
    }
    for name, value in request.param[1].items():
        options[name] = str(tmp_path / value) if isinstance(value, str) else value
    return request.param[0](**options)


@pytest.mark.parametrize("use_pydantic_options", [True, False])
def test_rosenbrock_problem(settings_model_for_rosenbrock, use_pydantic_options):
    """Test Rosenbrock problem."""
    configure_logger()
    rosen_problem = Rosenbrock()

    set_options = settings_model_for_rosenbrock.model_dump(
        exclude_unset=True, by_alias=True
    )

    if use_pydantic_options:
        result = OptimizationLibraryFactory().execute(
            rosen_problem, settings_model=settings_model_for_rosenbrock
        )
    else:
        result = OptimizationLibraryFactory().execute(
            rosen_problem,
            algo_name=settings_model_for_rosenbrock._TARGET_CLASS_NAME,
            **set_options,
        )

    assert result.x_opt == pytest.approx(rosen_problem.get_solution()[0], 2.0e-6)
    assert result.f_opt == pytest.approx(rosen_problem.get_solution()[1])

    # Test that files generated by the algo exists.
    for value in set_options.values():
        if isinstance(value, str):
            assert Path(value).exists()


@pytest.mark.parametrize(
    ("algo", "option", "value"),
    [
        ("PYOPTSPARSE_SLSQP", "MAXIT", 10),
        ("PYOPTSPARSE_SLSQP", "ACC", 1e-3),
        ("PYOPTSPARSE_SNOPT", "Major feasibility tolerance", 1e-3),
        ("PYOPTSPARSE_SNOPT", "Major iterations limit", 100),
        ("PYOPTSPARSE_SNOPT", "Iterations limit", 100),
    ],
)
def test_validator_forced_options_not_ok(algo, option, value):
    """Test the validation of non-correct fixed settings to Rosenbrock problem.

    Those settings cannot be changed by the user.
    """
    rosen_problem = Rosenbrock()

    with pytest.raises(ValueError):
        OptimizationLibraryFactory().execute(
            rosen_problem,
            algo_name=algo,
            **{option: value},
        )


@pytest.mark.parametrize("use_pydantic_options", [True, False])
def test_sobieski_snopt(sobieski_optim_problem, use_pydantic_options):
    """Test SNOPT on Sobieski problem.

    Also test that database is stored with internal SNOPT variables.
    """

    options = {
        "max_iter": 50,
        "normalize_design_space": True,
        "ftol_rel": 1e-9,
        "xtol_rel": 1e-9,
        "ftol_abs": 1e-9,
        "xtol_abs": 1e-9,
        "options_file": None,
        "Save major iteration variables": ["Hessian", "slack"],
    }

    if use_pydantic_options:
        result = OptimizationLibraryFactory().execute(
            sobieski_optim_problem,
            settings_model=SNOPT_Settings(**options),
        )
    else:
        result = OptimizationLibraryFactory().execute(
            sobieski_optim_problem,
            algo_name=SNOPT_Settings._TARGET_CLASS_NAME,
            **options,
        )

    sobieski_ref = SobieskiProblem()
    database = sobieski_optim_problem.database

    assert abs(result.f_opt) == pytest.approx(sobieski_ref.optimum_range, rel=1e-4)
    assert result.x_opt[[6, 7, 8, 9, 0, 1, 2, 3, 4, 5]] == pytest.approx(
        sobieski_ref.optimum_design, rel=1e-1
    )

    # Check that internal variables are correctly stored into the database.
    assert len(database.get_function_history("feasibility")) == 7
    assert len(database.get_function_history("optimality")) == 7
    assert len(database.get_function_history("Hessian")) == 7
    assert len(database.get_function_history("slack")) == 7
