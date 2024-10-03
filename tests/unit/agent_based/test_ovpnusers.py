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
    ([['{'], ['"n_clients": 0,'], ['"ovpn_dco_available": false,'], ['"ovpn_dco_ver": "Kernel module not loaded"'], ['}']], 0),
    ([['{'], ['"n_clients": 24,'], ['"ovpn_dco_available": false,'], ['"ovpn_dco_ver": "Kernel module not loaded"'], ['}']], 24),
])
def test_parse_ovpnusers(section, result):
    assert openvpn.parse_ovpnusers(section) == result


@pytest.mark.parametrize('section, result', [
    (0, [Service()]),
    (24, [Service()]),
])
def test_discover_ovpnusers(section, result):
    assert list(openvpn.discover_ovpnusers(section)) == result


@pytest.mark.parametrize('params, section, result', [
    (
        {},
        24,
        [
            Result(state=State.OK, summary='VPN Users: 24'),
            Metric('users', 24.0)
        ]
    ),
    (
        {},
        0,
        [
            Result(state=State.OK, summary='VPN Users: 0'),
            Metric('users', 0.0)
        ]
    ),
    (
        {'users': ('fixed', (30, 40))},
        24,
        [
            Result(state=State.OK, summary='VPN Users: 24'),
            Metric('users', 24.0, levels=(30.0, 40.0))
        ]
    ),
    (
        {'users': ('fixed', (10, 40))},
        24,
        [
            Result(state=State.WARN, summary='VPN Users: 24 (warn/crit at 10/40)'),
            Metric('users', 24.0, levels=(10.0, 40.0))
        ]
    ),
    (
        {'users': ('fixed', (10, 20))},
        24,
        [
            Result(state=State.CRIT, summary='VPN Users: 24 (warn/crit at 10/20)'),
            Metric('users', 24.0, levels=(10.0, 20.0))
        ]
    ),
])
def test_check_ovpnusers(params, section, result):
    assert list(openvpn.check_ovpnusers(params, section)) == result
