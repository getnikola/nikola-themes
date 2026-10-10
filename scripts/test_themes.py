#!/usr/bin/env python

"""Make sanity checks on the provided themes."""

import filecmp
import sys
from pathlib import Path

from nikola import utils


def error(msg):
    print("\x1b[31;1mERROR:", msg)


def warning(msg):
    print("\x1b[33;1mWARNING:", msg)


def theme_list():
    return sorted(['base', 'base-jinja', 'bootstrap', 'bootstrap-jinja', 'bootstrap3', 'bootstrap3-jinja'] + [theme.name for theme in Path().glob("v*/*")])


def sanity_check(theme=None):
    if theme is None:  # Check them all
        for theme in theme_list():
            sanity_check(theme)
        return
    themes = utils.get_theme_chain(theme, themes_dirs=['v7', 'v8'])
    themes_bn = [Path(i).name for i in themes]
    engine = utils.get_template_engine(themes)

    # Inheritance checks

    # All themes must inherit from base
    if themes_bn[-1] != 'base':
        error(f"theme {theme} doesn't inherit from base")
    # All jinja themes must inherit from base-jinja
    if engine == "jinja" and "base-jinja" not in themes_bn:
        error(f"theme {theme} is jinja-based and doesn't inherit from base-jinja")
    # All mako themes must NOT inherit from base-jinja
    if engine == "mako" and "base-jinja" in themes_bn:
        error(f"theme {theme} is mako-based and inherits from base-jinja")

    # Detect exact asset duplication in theme chain
    theme_dir = Path("v7", theme)
    for path in theme_dir.rglob("*"):
        if not path.is_file():
            continue
        asset = path.relative_to(theme_dir).as_posix()
        r, p1, p2 = is_asset_duplicated(asset, themes)
        if r:
            error(f"duplicated asset: {p1} {p2}")

    # Detect deprecated names and anonymous namespaces
    for path in (theme_dir / "templates").rglob("*"):
        if not path.is_file():
            continue
        data = path.read_text(encoding="utf-8")
        for k, exceptions in blacklist:
            if k in data and path.name not in exceptions:
                error(f"theme '{theme}' contains deprecated name '{k}' in {path}")

    # Ensure the theme has a README.md
    if utils.get_asset_path('README.md', themes) is None:
        error(f"theme '{theme}' has no README.md")

    # Ensure the theme has a meta file
    if utils.get_asset_path(theme + '.theme', themes) is None:
        warning(f"theme '{theme}' has no {theme}.theme meta file")


def is_asset_duplicated(path, themes):
    # First get the path for the asset with whole theme chain
    p1 = utils.get_asset_path(path, themes)
    # Get the path for asset with truncated theme chain
    p2 = utils.get_asset_path(path, themes[1:])
    # Ignore some files that may be duplicated
    if any(i in path for i in ('README.md', 'engine', 'AUTHORS.txt', 'conf.py.sample')):
        return False, p1, p2
    # Compare
    if p1 and p2:
        return filecmp.cmp(p1, p2, False), p1, p2
    else:
        return False, p1, p2


blacklist = (
    ["${analytics}", []],
    ["{{analytics}}", []],
    ["disqus_", ['comments_helper.tmpl', 'disqus_helper.tmpl']],
    ["addthis", []],
    ["namespace file=", []],
)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        sanity_check()
    else:
        for a in sys.argv[1:]:
            sanity_check(a)
