# -*- coding: utf-8 -*-

"""Generate package indexes (meta-plugin).

This plugin depends on pkgindex_compiler, pkgindex_scan and pkgindex_zip, which implement the real functionality."""

from __future__ import unicode_literals

from nikola.plugin_categories import ConfigPlugin


class PackageIndex(ConfigPlugin):
    """Generate package indexes (meta-plugin)."""

    name = "pkgindex"
