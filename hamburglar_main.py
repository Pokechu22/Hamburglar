#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
This program is free software. It comes without any warranty, to
the extent permitted by applicable law. You can redistribute it
and/or modify it under the terms of the Do What The Fuck You Want
To Public License, Version 2, as published by Sam Hocevar. See
http://sam.zoy.org/wtfpl/COPYING for more details.
"""

def usage():
    print("Example usage:")
    print("Burger/munch.py -c 1.5.jar 1.6.jar | Hamburglar/hamburglar.py")


def import_toppings():
    """
    Attempts to load all available toppings.
    """
    import os

    this_dir = os.path.dirname(__file__)
    toppings_dir = os.path.join(this_dir, "hamburglar", "toppings")
    from_list = ["topping"]

    # Traverse the toppings directory and import everything.
    for root, dirs, files in os.walk(toppings_dir):
        for file_ in files:
            if not file_.endswith(".py"):
                continue
            elif file_.startswith("__"):
                continue

            from_list.append(file_[:-3])

    imports = __import__("hamburglar.toppings", fromlist=from_list)

    toppings = imports.topping.Topping.__subclasses__()
    subclasses = toppings
    while len(subclasses) > 0:
        newclasses = []
        for subclass in subclasses:
            newclasses += subclass.__subclasses__()
        subclasses = newclasses
        toppings += subclasses

    return toppings

def compare(toppings, a, b):
    # Compare versions
    aggregate = {}

    for topping in toppings:
        if topping.KEY == None:
            continue
        keys = topping.KEY.split(".")
        obj1 = a
        obj2 = b
        target = aggregate
        skip = False
        for key in keys:
            if not (key in obj1 and key in obj2):
                skip = True
                break
            obj1 = obj1[key]
            obj2 = obj2[key]
        if skip:
            continue
        for key in keys[:-1]:
            if not key in target:
                target[key] = {}
            target = target[key]

        target[keys[-1]] = topping().filter(obj1, obj2)

    return aggregate

def main():
    import getopt
    import sys
    import json

    try:
        opts, args = getopt.gnu_getopt(
            sys.argv[1:],
            "o:c",
            [
                "output=",
                "compact"
            ]
        )
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(1)

    # Default options
    output = sys.stdout
    compact = False

    for o, a in opts:
        if o in ("-o", "--output"):
            output = open(a, "w")
        elif o in ("-c", "--compact"):
            compact = True

    toppings = import_toppings()

    if len(args) > 0:
        # Load JSON objects from files
        versions = []
        for path in args:
            try:
                versions += json.load(open(path, "r"))
            except:
                print("Error: Can't load " + path)
                sys.exit(3)
    else:
        # Load JSON objects from stdin
        if sys.stdin.isatty():
            print("Error: The Hamburglar needs to be fed burgers\n")
            usage()
            sys.exit(3)

        try:
            versions = json.load(sys.stdin)
        except ValueError as err:
            print("Error: Invalid input (" + str(err) + ")\n")
            usage()
            sys.exit(5)

    if len(versions) < 2:
        print("Error: The Hamburglar needs more burgers\n")
        usage()
        sys.exit(2)
    elif len(versions) > 2:
        print("Error: Burger overload\n")
        usage()
        sys.exit(2)

    # Compare versions
    result = compare(toppings, versions[0], versions[1])

    # Output results
    if not compact:
        json.dump(result, output, sort_keys=True, indent=4)
    else:
        json.dump(result, output)

if __name__ == '__main__':
    main()
