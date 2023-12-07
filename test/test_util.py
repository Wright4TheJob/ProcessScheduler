# Copyright (c) 2020-2021 Thomas Paviot (tpaviot@gmail.com)
#
# This file is part of ProcessScheduler.
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.

import random

from processscheduler.util import (
    calc_parabola_from_three_points,
    sort_no_duplicates,
    sort_duplicates,
    clean_buffer_states,
)

import z3


def test_calc_parabola_from_three_points():
    a, b, c = calc_parabola_from_three_points([0, 1, 2], [0, 2, 4])
    assert [a, b, c] == [0, 2, 0]
    d, e, f = calc_parabola_from_three_points([0, 1, 2], [0, 1, 4])
    assert [d, e, f] == [1, 0, 0]


def test_sort_no_duplicates():
    """sort an array of 20 different integers"""
    lst_to_sort = random.sample(range(-100, 100), 20)
    sorted_variables, assertions = sort_no_duplicates(lst_to_sort)
    s = z3.Solver()
    s.add(assertions)
    result = s.check()
    assert result == z3.sat
    solution = s.model()
    sorted_integers = [solution[v].as_long() for v in sorted_variables]
    assert sorted(lst_to_sort) == sorted_integers


def test_sort_duplicates():
    """sort an array of 20 integers with only 10 differen"""
    lst_to_sort = random.sample(range(-100, 100), 10) * 2
    sorted_variables, assertions = sort_duplicates(lst_to_sort)
    s = z3.Solver()
    s.add(assertions)
    result = s.check()
    assert result == z3.sat
    solution = s.model()
    sorted_integers = [solution[v].as_long() for v in sorted_variables]
    assert sorted(lst_to_sort) == sorted_integers


def test_clean_buffer_states():
    assert clean_buffer_states([100, 21, 21, 21], [7, 7, 7]) == ([100, 21], [7])
