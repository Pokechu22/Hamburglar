#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
This program is free software. It comes without any warranty, to
the extent permitted by applicable law. You can redistribute it
and/or modify it under the terms of the Do What The Fuck You Want
To Public License, Version 2, as published by Sam Hocevar. See
http://sam.zoy.org/wtfpl/COPYING for more details.
"""

from .ignorefieldtopping import Topping


class RecipesTopping(Topping):
    KEY = "recipes"

    def _item_str(self, item):
        name = ""
        metadata = None
        count = 1
        type = ""
        if "name" in item:
            name = item["name"]
        if "metadata" in item:
            metadata = item["metadata"]
        if "count" in item:
            count = item["count"]
        if "type" in item:
            type = item["type"]
        return "%s_%s:%sx%s" % (type, name, metadata, count)

    def filter(self, object1, object2):
        changed = {}

        def make_map(recipes):
            """Makes a temporary map with unique keys per-recipe from a list"""
            rec_map = {}
            for rec in recipes:
                key = ""
                if rec["type"] == "shape":
                    for row in rec["shape"]:
                        for item in row:
                            if item:
                                key += self._item_str(item)
                                key += ","
                else:
                    for item in rec["ingredients"]:
                        key += self._item_str(item)
                        key += ","
                rec_map[key] = rec
            return rec_map

        for id in object1:
            if id not in object2:
                changed[id] = [object1[id], None]
                continue

            obj = object1[id]
            if isinstance(obj, dict):
                obj = [obj]

            obj2 = make_map(object2[id])
            obj1 = make_map(obj)

            changed1 = []
            changed2 = []

            for key in obj1:
                if key == "id": continue

                if key not in obj2:
                    changed1.append(obj1[key])
                    continue
                if not self.equal(obj1[key], obj2[key]):
                    changed1.append(obj1[key])
                    changed2.append(obj2[key])

            for key in obj2:
                if key == "id": continue

                if key not in obj1:
                    changed2.append(obj2[key])

            if len(changed1) + len(changed2) != 0:
                changed[id] = [changed1, changed2]

        for id in object2:
            if id not in object1:
                changed[id] = [None, object2[id]]
                continue

        return changed

    def equal(self, rec1, rec2):
        def items_equal(i1, i2, strictmeta = True):
            if not i1 and not i2:
                # Both are None in cases of, say, rails.
                return True
            elif not i1 or not i2:
                # But one being None and the other not is a difference.
                return False

            if ("count" in i1) != ("count" in i2):
                return False
            elif "count" in i1 and i1["count"] != i2["count"]:
                return False
            if ("metadata" in i1) and not ("metadata" in i2):
                if strictmeta or i1["metadata"] != 0:
                    return False
            elif ("metadata" in i2) and not ("metadata" in i1):
                if strictmeta or i2["metadata"] != 0:
                    return False
            elif "metadata" in i1 and i1["metadata"] != i2["metadata"]:
                return False
            if ("name" in i1) != ("name" in i2):
                return False
            elif "name" in i1 and i1["name"] != i2["name"]:
                return False

            return True

        if not items_equal(rec1["makes"], rec2["makes"], strictmeta=False):
            return False

        if rec1["type"] != rec2["type"]:
            return False

        if rec1["type"] == "shape":
            sh1 = rec1["shape"]
            sh2 = rec2["shape"]
            if len(sh1) != len(sh2):
                return False
            for i in range(len(sh1)):
                if len(sh1[i]) != len(sh2[i]):
                    return False
                for j in range(len(sh1[i])):
                    if not items_equal(sh1[i][j], sh2[i][j]):
                        return False
        else:
            # Doesn't handle duplicates...
            i1 = [self._item_str(x) for x in rec1["ingredients"]]
            i2 = [self._item_str(x) for x in rec2["ingredients"]]
            for item in i1:
                if item not in i2:
                    return False
        return True
