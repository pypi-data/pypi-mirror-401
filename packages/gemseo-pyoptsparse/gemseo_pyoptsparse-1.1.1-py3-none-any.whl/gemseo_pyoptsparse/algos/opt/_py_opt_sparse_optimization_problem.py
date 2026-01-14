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

"""Definition of the PyOptSparse optimization problem for |g|."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Final

from gemseo.core.mdo_functions.mdo_function import MDOFunction
from gemseo.core.mdo_functions.mdo_linear_function import MDOLinearFunction
from pyoptsparse import Optimization

from gemseo_pyoptsparse.algos.opt._py_opt_sparse_functions import PyOptSparseFunctions

if TYPE_CHECKING:
    from gemseo import OptimizationProblem
    from gemseo.typing import RealArray

    from gemseo_pyoptsparse.algos.opt.py_opt_sparse import OptProblemJacType


class PyOptSparseOptimizationProblem(Optimization):
    """An interface to the PyOptSparse optimization from an
    :class:`.OptimizationProblem`.

    In the current implementation, the sparsity of the problem is not taken into
    account, which means that it is assumed that all functions (objective and
    constraints) depend on all inputs. The input design variables defined in |g| are
    thus gathered into a single vector that is passed to the PyOptSparse functions.
    """  # noqa: D205

    __jac: OptProblemJacType | None
    """The Jacobian of the functions of optimization problem."""

    __INPUT_VAR_NAME: Final[str] = "inputs"
    """The name of the group containing all input design variables for PyOptSparse."""

    def __init__(
        self,
        problem: OptimizationProblem,
        starting_point: RealArray,
        lower_bound: RealArray,
        upper_bound: RealArray,
    ) -> None:
        """
        Args:
            problem: The optimization problem.
            starting_point: The initial values of the design variables.
            lower_bound: The lower bounds of the design variables.
            upper_bound: The upper bounds of the design variables.
        """  # noqa: D205, D212, D415
        functions = self.__build_functions(problem)
        super().__init__(
            "PyOptSparse optimization problem from GEMSEO",
            objFun=functions.compute_outputs,
        )
        self.__jac = functions.compute_jacobian if functions.has_jac else None
        self.addVarGroup(
            self.__INPUT_VAR_NAME,
            len(starting_point),
            "c",
            starting_point,
            lower=lower_bound,
            upper=upper_bound,
        )
        self.addObj(problem.objective.name)

        self.__add_linear_constraints(problem)
        self.__add_nonlinear_constraints(problem)

    @property
    def jac(self) -> OptProblemJacType:
        """The Jacobian of the functions of optimization problem.

        It includes objective and constraints.
        """
        return self.__jac

    @staticmethod
    def __build_functions(
        problem: OptimizationProblem,
    ) -> PyOptSparseFunctions:
        """Build PyOptSparse functions from the |g| optimization problem.

        Args:
            problem: The |g| optimization problem.

        Returns:
            The functions to be used with the PyOptSparse optimization problem.
        """
        functions = PyOptSparseFunctions(
            PyOptSparseOptimizationProblem.__INPUT_VAR_NAME
        )
        obj = problem.objective
        jac = obj.jac if obj.has_jac else None
        functions.add_function(obj.name, obj.func, jac)
        for constraint in problem.constraints:
            jac = constraint.jac if constraint.has_jac else None
            if not isinstance(constraint.original, MDOLinearFunction):
                functions.add_function(constraint.name, constraint.func, jac)

        return functions

    def __add_linear_constraints(self, problem: OptimizationProblem) -> None:
        """Add linear constraints to PyOptSparse.

        Args:
            problem: The optimization problem.
        """
        for constraint in problem.constraints:
            if not isinstance(constraint.original, MDOLinearFunction):
                continue

            lin_func = constraint.original
            coefficients = lin_func.coefficients

            if constraint.f_type == MDOFunction.ConstraintType.EQ:
                lower = upper = 0.0
            else:
                lower, upper = None, 0.0

            self.addConGroup(
                constraint.name,
                constraint.dim,
                lower=lower,
                upper=upper,
                linear=True,
                wrt=[self.__INPUT_VAR_NAME],
                jac={self.__INPUT_VAR_NAME: coefficients},
            )

    def __add_nonlinear_constraints(self, problem: OptimizationProblem) -> None:
        """Add non-linear constraints to PyOptSparse.

        Args:
           problem: The optimization problem.
        """
        for constraint in problem.constraints:
            if isinstance(constraint.original, MDOLinearFunction):
                continue

            if constraint.f_type == MDOFunction.ConstraintType.INEQ:
                lower = None
                upper = 0.0
            else:
                lower = upper = 0.0

            self.addConGroup(
                constraint.name,
                constraint.dim,
                lower=lower,
                upper=upper,
                wrt=self.__INPUT_VAR_NAME,
            )
