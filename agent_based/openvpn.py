#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#
# Checks based on the Phion-MIB for the Barracuda CloudGen Firewall.
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

import json

from cmk.agent_based.v2 import (
    AgentSection, 
    CheckPlugin, 
    Service, 
    Result, 
    State, 
    Metric, 
    check_levels
)


def parse_ovpnusers(string_table):
    if string_table:
        flatten_string_table = ["".join(item) for item in string_table]
        json_str = json.loads("".join(flatten_string_table))
        return json_str["n_clients"]
    return {}


def discover_ovpnusers(section):
    if section is not None:
        yield Service()


def check_ovpnusers(params, section):
    if section is not None:
        yield from check_levels(
            section,
            levels_upper=params.get("users", None),
            label="VPN Users",
            metric_name="users",
            render_func=lambda v: "%d" % v
        )


def parse_ovpnlicense(string_table):
    if string_table:
        flatten_string_table = ["".join(item) for item in string_table]
        json_str = json.loads("".join(flatten_string_table))
        return(json_str)
    return []


def discover_ovpnlicense(section):
    if section is not None:
        yield Service()        


def check_ovpnlicense(params, section):
    if section is not None:
        yield from check_levels(
            section[0],
            levels_upper=params.get("used_lic", None),
            label="Used licenses",
            metric_name="used",
            render_func=lambda v: "%d" % v
        )

        yield from check_levels(
            section[1],
            levels_upper=params.get("total_lic", None),
            label="Total licenses",
            metric_name="total",
            render_func=lambda v: "%d" % v
        )


agent_section_ovpnusers = AgentSection(
    name = "ovpn_users",
    parse_function = parse_ovpnusers,
)

check_plugin_ovpnusers = CheckPlugin(
    name = "ovpn_users",
    service_name = "OpenVPN Users",
    discovery_function = discover_ovpnusers,
    check_function = check_ovpnusers,
    check_ruleset_name="ovpn_users",
    check_default_parameters={},
)

agent_section_ovpnlicense = AgentSection(
    name = "ovpn_licusage",
    parse_function = parse_ovpnlicense,
)

check_plugin_ovpnlicense = CheckPlugin(
    name = "ovpn_licusage",
    service_name = "OpenVPN License Usage",
    discovery_function = discover_ovpnlicense,
    check_function = check_ovpnlicense,
    check_ruleset_name="ovpn_licusage",
    check_default_parameters={},
)