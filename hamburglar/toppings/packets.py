#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
This program is free software. It comes without any warranty, to
the extent permitted by applicable law. You can redistribute it
and/or modify it under the terms of the Do What The Fuck You Want
To Public License, Version 2, as published by Sam Hocevar. See
http://sam.zoy.org/wtfpl/COPYING for more details.
"""

from .topping import Topping


class PacketsTopping(Topping):
    KEY = "packets.packet"
    IGNORE = ('class', 'field', 'condition')

    def equal(self, entry1, entry2):
        if not type(entry1) == type(entry2):
            return False
        if isinstance(entry1, dict):
            if "operation" in entry1 and "operation" in entry2:
                if entry1["operation"] == entry2["operation"]:
                    if entry1["operation"] in ("store", "interfacecall"):
                        # These operations often change data based off of
                        # obfuscation - don't worry about them
                        return True

            for key in entry1.keys():
                if not key in self.IGNORE and (
                    not key in entry2 or
                    not self.equal(entry1[key], entry2[key])):
                    return False

            for key in entry2.keys():
                if not key in self.IGNORE and not key in entry1:
                    return False
        elif isinstance(entry1, list):
            if len(entry1) != len(entry2):
                return False
            for key in range(len(entry1)):
                if not self.equal(entry1[key], entry2[key]):
                    return False
        else:
            return entry1 == entry2

        return True
