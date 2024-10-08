#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#
# Checks for the OpenVPN Access Server.
#
# Copyright (C) 2024 Lamberto Grippi <lamberto.grippi@scs.ch>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#

import pytest  # type: ignore[import]
from cmk.agent_based.v2 import (
    Metric,
    Result,
    Service,
    State,
)
from cmk.base.plugins.agent_based import openvpn


@pytest.mark.parametrize('section, result', [
    ([['['], ['0,'], ['2'], [']']], [0, 2]),
    ([['['], ['2,'], ['2'], [']']], [2, 2]),
])
def test_parse_ovpnlicense(section, result):
    assert openvpn.parse_ovpnlicense(section) == result


@pytest.mark.parametrize('section, result', [
    ([0, 2], [Service()]),
    ([2, 2], [Service()]),
])
def test_discover_ovpnlicense(section, result):
    assert list(openvpn.discover_ovpnlicense(section)) == result


@pytest.mark.parametrize('params, section, result', [
    (
        {},
        [3, 10],
        [
            Result(state=State.OK, summary='Used licenses: 3'),
            Metric('used', 3.0, boundaries=(0.0, 10.0)),
            Result(state=State.OK, summary='Total licenses: 10'),
            Metric('total', 10.0),
        ]
    ),
    (
        {},
        [0, 10],
        [
            Result(state=State.OK, summary='Used licenses: 0'),
            Metric('used', 0.0, boundaries=(0.0, 10.0)),
            Result(state=State.OK, summary='Total licenses: 10'),
            Metric('total', 10.0),
        ]
    ),
    (
        {'used_lic': ('fixed', (5, 8))},
        [7, 10],
        [
            Result(state=State.WARN, summary='Used licenses: 7 (warn/crit at 5/8)'),
            Metric('used', 7.0, levels=(5.0, 8.0), boundaries=(0.0, 10.0)),
            Result(state=State.OK, summary='Total licenses: 10'),
            Metric('total', 10.0),
        ]
    ),
])
def test_check_ovpnlicense(params, section, result):
    assert list(openvpn.check_ovpnlicense(params, section)) == result
