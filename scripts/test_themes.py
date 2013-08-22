#!/usr/bin/env python

"""Make sanity checks on the provided themes."""

from __future__ import unicode_literals, print_function
import glob
import hashlib

import colorama

from nikola import utils

def error(msg):
    print(colorama.Fore.RED + "ERROR:" + msg)

def theme_list():
    return [theme.split('/')[-1] for theme in glob.glob("themes/*")]

def sanity_check(theme=None):
    if theme is None:  # Check them all
        for theme in theme_list():
            sanity_check(theme)
        return
    themes = utils.get_theme_chain(theme)
    engine = utils.get_template_engine(themes)

    # Inheritance checks

    # All themes must inherit from base
    if themes[-1] != 'base':
        error("theme {0} doesn't inherit from base".format(theme))
    # All jinja themes must inherit from base-jinja
    if engine == "jinja" and "base-jinja" not in themes:
        error("theme {0} is jinja-based and doesn't inherit from base-jinja".format(theme))
    # All mako themes must NOT inherit from base-jinja
    if engine == "mako" and "base-jinja" in themes:
        error("theme {0} is mako-based and inherits from base-jinja".format(theme))

    # Detect exact template duplication in theme chain
    for fname in glob.glob("/".join(["themes", theme, "templates", "*.tmpl"])):  # templates
        with open(fname) as inf:
            baseline = hashlib.sha224(inf.read()).hexdigest()
        fname = "/".join(fname.split("/")[2:])
        fname2 = utils.get_asset_path(fname, themes[1:])
        with open(fname2) as inf:
            new_hash = hashlib.sha224(inf.read()).hexdigest()
        if baseline == new_hash:
            error("theme {0} has a redundant template: {1} is identical to {2}".format(theme, fname, fname2))



if __name__ == "__main__":
    import commandline
    colorama.init()
    commandline.run_as_main(sanity_check)
