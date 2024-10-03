#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-
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

from cmk.graphing.v1 import (
    metrics,
    graphs,
    perfometers,
    translations,
)


translation_ovpnusers = translations.Translation(
    name="ovpn_users",
    check_commands=[translations.PassiveCheck("ovpn_users")],
    translations={
        "users": translations.RenameTo("ovpn_users"),
    }
)

metric_ovpnusers = metrics.Metric(
    name="ovpn_users",
    title=metrics.Title("Concurrent VPN Users"),
    unit=metrics.Unit(metrics.DecimalNotation(""), metrics.StrictPrecision(0)),
    color=metrics.Color.ORANGE,
)

perfometer_ovpnusers = perfometers.Perfometer(
    name="ovpn_users",
    focus_range=perfometers.FocusRange(perfometers.Closed(0), perfometers.Open(10)),
    segments=["ovpn_users"],
)


translation_ovplicense = translations.Translation(
    name="ovpn_licusage",
    check_commands=[translations.PassiveCheck("ovpn_licusage")],
    translations={
        "used": translations.RenameTo("ovpn_used_license"),
        "total": translations.RenameTo("ovpn_total_license"),
    }
)

metric_ovplicense_used = metrics.Metric(
    name="ovpn_used_license",
    title=metrics.Title("Used OpenVPN Licenses"),
    unit=metrics.Unit(metrics.DecimalNotation(""), metrics.StrictPrecision(0)),
    color=metrics.Color.DARK_ORANGE,
)

metric_ovplicense_total = metrics.Metric(
    name="ovpn_total_license",
    title=metrics.Title("Total OpenVPN Licenses"),
    unit=metrics.Unit(metrics.DecimalNotation(""), metrics.StrictPrecision(0)),
    color=metrics.Color.ORANGE,
)

graph_licenses = graphs.Graph(
    name="ovpn_licenses",
    title=graphs.Title('Licenses'),
    compound_lines=["ovpn_used_license"],
    simple_lines=["ovpn_total_license"],
)

perfometer_ovplicense = perfometers.Stacked(
    name="ovpn_licusage",
    upper=perfometers.Perfometer(
        name="ovpn_total_license",
        focus_range=perfometers.FocusRange(perfometers.Closed(0), perfometers.Open(10)),
        segments=["ovpn_total_license"],
    ),
    lower=perfometers.Perfometer(
        name="ovpn_used_license",
        focus_range=perfometers.FocusRange(perfometers.Closed(0), perfometers.Open(10)),
        segments=["ovpn_used_license"],
    ),
)
