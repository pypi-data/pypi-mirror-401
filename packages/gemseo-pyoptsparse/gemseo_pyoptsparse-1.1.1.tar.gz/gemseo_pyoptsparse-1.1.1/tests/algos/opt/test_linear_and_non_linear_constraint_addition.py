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

from unittest.mock import MagicMock
from unittest.mock import patch

import numpy as np
import pytest
from gemseo.algos.optimization_problem import OptimizationProblem
from gemseo.core.mdo_functions.mdo_function import MDOFunction
from gemseo.core.mdo_functions.mdo_linear_function import MDOLinearFunction
from numpy.testing import assert_array_equal

from gemseo_pyoptsparse.algos.opt._py_opt_sparse_optimization_problem import (
    PyOptSparseOptimizationProblem,
)


@pytest.fixture
def mock_opt_problem():
    problem = MagicMock(spec=OptimizationProblem)
    problem.design_space = MagicMock()
    problem.design_space.dimension = 2
    problem.objective = MagicMock()
    problem.objective.name = "dummy_obj"
    return problem


def test_add_linear_equality_constraint(mock_opt_problem):
    lin_eq = MagicMock(spec=MDOLinearFunction)
    lin_eq.coefficients = np.array([[2.0, 3.0]])
    lin_eq.value_at_zero = np.array([5.0])

    constraint = MagicMock()
    constraint.original = lin_eq
    constraint.f_type = MDOFunction.ConstraintType.EQ
    constraint.dim = 1
    constraint.name = "lin_eq"
    mock_opt_problem.constraints = [constraint]

    with patch("pyoptsparse.Optimization.addConGroup") as mock_add_con:
        PyOptSparseOptimizationProblem(
            problem=mock_opt_problem,
            starting_point=np.array([0.0, 0.0]),
            lower_bound=np.array([-1.0, -1.0]),
            upper_bound=np.array([1.0, 1.0]),
        )
        # Extract actual call arguments
        args, kwargs = mock_add_con.call_args
        assert args[0] == "lin_eq"
        assert args[1] == 1
        assert kwargs["lower"] == 0.0
        assert kwargs["upper"] == 0.0
        assert kwargs["linear"] is True
        assert list(kwargs["wrt"]) == ["inputs"]
        assert_array_equal(kwargs["jac"]["inputs"], np.array([[2.0, 3.0]]))


def test_add_linear_inequality_constraint(mock_opt_problem):
    lin_ineq = MagicMock(spec=MDOLinearFunction)
    lin_ineq.coefficients = np.array([[1.0, -1.0]])
    lin_ineq.value_at_zero = np.array([0.0])

    constraint = MagicMock()
    constraint.original = lin_ineq
    constraint.f_type = MDOFunction.ConstraintType.INEQ
    constraint.dim = 1
    constraint.name = "lin_ineq"
    mock_opt_problem.constraints = [constraint]

    with patch("pyoptsparse.Optimization.addConGroup") as mock_add_con:
        PyOptSparseOptimizationProblem(
            problem=mock_opt_problem,
            starting_point=np.array([0.0, 0.0]),
            lower_bound=np.array([-1.0, -1.0]),
            upper_bound=np.array([1.0, 1.0]),
        )
        args, kwargs = mock_add_con.call_args
        assert args[0] == "lin_ineq"
        assert args[1] == 1
        assert kwargs["upper"] == 0.0
        assert kwargs["lower"] is None
        assert kwargs["linear"] is True
        assert list(kwargs["wrt"]) == ["inputs"]
        assert_array_equal(kwargs["jac"]["inputs"], np.array([[1.0, -1.0]]))


def test_add_nonlinear_equality_constraint(mock_opt_problem):
    constraint = MagicMock()
    constraint.original = MagicMock()
    constraint.f_type = MDOFunction.ConstraintType.EQ
    constraint.dim = 1
    constraint.name = "nonlin_eq"
    mock_opt_problem.constraints = [constraint]

    with patch("pyoptsparse.Optimization.addConGroup") as mock_add_con:
        PyOptSparseOptimizationProblem(
            problem=mock_opt_problem,
            starting_point=np.array([0.0, 0.0]),
            lower_bound=np.array([-1.0, -1.0]),
            upper_bound=np.array([1.0, 1.0]),
        )
        args, kwargs = mock_add_con.call_args
        assert args[0] == "nonlin_eq"
        assert args[1] == 1
        assert kwargs["lower"] == 0.0
        assert kwargs["upper"] == 0.0
        wrt_value = kwargs["wrt"]
        if isinstance(wrt_value, str):
            wrt_value = [wrt_value]
        assert wrt_value == ["inputs"]
        assert "linear" not in kwargs


def test_add_nonlinear_inequality_constraint(mock_opt_problem):
    constraint = MagicMock()
    constraint.original = MagicMock()
    constraint.f_type = MDOFunction.ConstraintType.INEQ
    constraint.dim = 1
    constraint.name = "nonlin_ineq"
    mock_opt_problem.constraints = [constraint]

    with patch("pyoptsparse.Optimization.addConGroup") as mock_add_con:
        PyOptSparseOptimizationProblem(
            problem=mock_opt_problem,
            starting_point=np.array([0.0, 0.0]),
            lower_bound=np.array([-1.0, -1.0]),
            upper_bound=np.array([1.0, 1.0]),
        )
        args, kwargs = mock_add_con.call_args
        assert args[0] == "nonlin_ineq"
        assert args[1] == 1
        assert kwargs["upper"] == 0.0
        assert kwargs["lower"] is None
        wrt_value = kwargs["wrt"]
        if isinstance(wrt_value, str):
            wrt_value = [wrt_value]
        assert wrt_value == ["inputs"]
        assert "linear" not in kwargs


def test_no_linear_constraints(mock_opt_problem):
    # No linear constraints in the problem
    mock_opt_problem.constraints = []
    with patch("pyoptsparse.Optimization.addConGroup") as mock_add_con:
        PyOptSparseOptimizationProblem(
            problem=mock_opt_problem,
            starting_point=np.array([0.0, 0.0]),
            lower_bound=np.array([-1.0, -1.0]),
            upper_bound=np.array([1.0, 1.0]),
        )
        # Ensure no linear constraints added
        mock_add_con.assert_not_called()
