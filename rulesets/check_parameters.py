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

from cmk.rulesets.v1 import Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    InputHint,
    Integer,
    LevelDirection,
    LevelsType,
    migrate_to_integer_simple_levels,
    SimpleLevels,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, Topic, HostCondition


def _parameter_form_ovpnusers():
    return Dictionary(
        elements={
            "users": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Levels for number of OpenVPN Users"),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Integer(),
                    migrate=migrate_to_integer_simple_levels,
                    prefill_levels_type=DefaultValue(LevelsType.NONE),
                    prefill_fixed_levels=InputHint(value=(0, 0)),
                ),
                required=False,
            ),
        }
    )


rule_spec_ovpnusers = CheckParameters(
    name="ovpn_users",
    topic=Topic.NETWORKING,
    parameter_form=_parameter_form_ovpnusers,
    title=Title("OpenVPN Users"),
    condition=HostCondition(),
)


def _parameter_form_ovpnlicusage():
    return Dictionary(
        elements={
            "used_lic": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Levels for total number of OpenVPN Licenses"),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Integer(),
                    migrate=migrate_to_integer_simple_levels,
                    prefill_levels_type=DefaultValue(LevelsType.NONE),
                    prefill_fixed_levels=InputHint(value=(0, 0)),
                ),
                required=False,
            ),
            "total_lic": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Levels for used number of OpenVPN Licenses"),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Integer(),
                    migrate=migrate_to_integer_simple_levels,
                    prefill_levels_type=DefaultValue(LevelsType.NONE),
                    prefill_fixed_levels=InputHint(value=(0, 0)),
                ),
                required=False,
            ),
        }
    )


rule_spec_ovpnlicense = CheckParameters(
    name="ovpn_licusage",
    topic=Topic.NETWORKING,
    parameter_form=_parameter_form_ovpnlicusage,
    title=Title("OpenVPN License usage"),
    condition=HostCondition(),
)
