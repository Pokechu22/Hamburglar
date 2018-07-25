#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
This program is free software. It comes without any warranty, to
the extent permitted by applicable law. You can redistribute it
and/or modify it under the terms of the Do What The Fuck You Want
To Public License, Version 2, as published by Sam Hocevar. See
http://sam.zoy.org/wtfpl/COPYING for more details.
"""

from .ignorefieldtopping import IgnoreFieldTopping


class BlocksTopping(IgnoreFieldTopping):
    KEY = "blocks.block"
    NAME = "Blocks"
    IGNORE = ('class', 'field', 'enum_class', 'declared_in', 'field_name', 'predicate', 'numeric_id', 'min_state_id', 'max_state_id')
