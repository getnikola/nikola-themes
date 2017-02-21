# -*- coding: utf-8 -*-

# Copyright © 2016-2017, Chris Warrick and Roberto Alsina.

# Permission is hereby granted, free of charge, to any
# person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the
# Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the
# Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice
# shall be included in all copies or substantial portions of
# the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
# OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""Post compiler for package indexes."""

from __future__ import unicode_literals

import configparser
import io
import os
import pygments
from nikola import utils
from nikola.plugin_categories import PageCompiler
from pygments.lexers import PythonLexer


def dirname_as_title(post, pkg_dir, config):
    """Use the directory name as title."""
    return {'title': os.path.basename(pkg_dir)}


def _version_from_path(path):
    if path.startswith('../'):
        path = path[3:]
    return int(path.split('/')[0].split('v')[-1])


def _cp_try_get(config, section, option):
    try:
        return config.get(section, option)
    except (configparser.NoOptionError, configparser.NoSectionError):
        return None


def parse_plugin_file(post, pkg_dir, config):
    plugin = os.path.basename(pkg_dir)
    data = {}
    data['name'] = plugin
    conf_sample = os.path.join(pkg_dir, 'conf.py.sample')
    ini = os.path.join(pkg_dir, plugin + '.plugin')
    reqpy = os.path.join(pkg_dir, 'requirements.txt')
    reqnonpy = os.path.join(pkg_dir, 'requirements-nonpy.txt')
    reqplugins = os.path.join(pkg_dir, 'requirements-plugins.txt')

    if os.path.exists(ini):
        try:
            c = configparser.ConfigParser()
            c.read(ini)
            data['author'] = c.get('Documentation', 'Author')
            data['version'] = c.get('Documentation', 'Version')
            data['description'] = c.get('Documentation', 'Description')
            data['website'] = _cp_try_get(c, 'Documentation', 'Website')
            data['minver'] = _cp_try_get(c, 'Nikola', 'MinVersion')
            data['maxver'] = _cp_try_get(c, 'Nikola', 'MaxVersion')

            category = c.get('Nikola', 'PluginCategory')
            data['category'] = category

            if data['minver']:
                minver = data['minver'].split('.')[0]
            else:
                minver = _version_from_path(pkg_dir)
                data['minver'] = minver
            if data['maxver']:
                maxver = data['maxver'].split('.')[0]
            else:
                maxver = config['versions_supported'][-1]

            data['allver'] = list(range(int(minver), int(maxver) + 1))

            tags = ['plugin', category]
            if category == 'CompilerExtension':
                data['compiler'] = c.get('Nikola', 'Compiler')
                tags.append(data['compiler'])
            for version in data['allver']:
                tags.append('v{0}'.format(version))
            data['tags'] = ','.join(tags)

            data['tests'] = _cp_try_get(c, 'Core', 'Tests')
        except Exception as e:
            raise Exception('Exception while reading plugin config "{0}": {1}'.format(ini, e)) from e
    else:
        raise ValueError('Plugin {0} has no .plugin file in the main '
                         'directory.'.format(plugin))

    if os.path.exists(conf_sample):
        with io.open(conf_sample, 'r', encoding='utf-8') as f:
            data['confpy'] = pygments.highlight(
                f.read(),
                PythonLexer(), utils.NikolaPygmentsHTML(plugin + '_conf_sample', linenos=False))
    else:
        data['confpy'] = None

    if os.path.exists(reqpy):
        with io.open(reqpy, 'r', encoding='utf-8') as f:
            data['pyreqs'] = f.readlines()
    else:
        data['pyreqs'] = []

    if os.path.exists(reqnonpy):
        with io.open(reqnonpy, 'r', encoding='utf-8') as f:
            r = f.readlines()

        data['nonpyreqs'] = [i.strip().split('::') for i in r]
    else:
        data['nonpyreqs'] = []

    if os.path.exists(reqplugins):
        with io.open(reqplugins, 'r', encoding='utf-8') as f:
            data['pluginreqs'] = f.readlines()
    else:
        data['pluginreqs'] = []

    data['reqcount'] = len(data['pyreqs']) + len(data['nonpyreqs']) + len(data['pluginreqs'])

    return data


def parse_theme_info(post, pkg_dir, config):
    theme = os.path.basename(pkg_dir)
    data = {}
    data['name'] = theme
    data['tags'] = 'theme'
    out_path = post.folder_relative + '/' + theme
    demo_dir = config['demo_screenshots_map'].get(out_path, out_path)
    data['previewimage'] = '/' + demo_dir + '.png'
    data['previewimage_thumbnail'] = '/' + demo_dir + '.thumbnail.png'
    data['demo_link'] = '/' + demo_dir + '/demo/'
    conf_sample = os.path.join(pkg_dir, 'conf.py.sample')
    engine = os.path.join(pkg_dir, 'engine')
    parent = os.path.join(pkg_dir, 'parent')

    if os.path.exists(conf_sample):
        with io.open(conf_sample, 'r', encoding='utf-8') as f:
            data['confpy'] = pygments.highlight(
                f.read(),
                PythonLexer(), utils.NikolaPygmentsHTML(theme + '_conf_sample', linenos=False))
    else:
        data['confpy'] = None

    if os.path.exists(engine):
        with io.open(engine, 'r', encoding='utf-8') as f:
            data['engine'] = f.read().strip()
    else:
        data['engine'] = 'mako'

    if os.path.exists(parent):
        with io.open(parent, 'r', encoding='utf-8') as f:
            data['parent'] = f.read().strip()
    elif theme == 'base':
        pass
    else:
        raise ValueError("Theme {0} has no parent.".format(theme))

    data['chain'] = utils.get_theme_chain(theme, [os.path.dirname(pkg_dir), 'themes'])
    data['chain'] = [os.path.basename(i) for i in reversed(data['chain'])]
    data['bootswatch'] = (('bootstrap' in data['chain'] or
                           'bootstrap-jinja' in data['chain'] or
                           'bootstrap3-jinja' in data['chain'] or
                           'bootstrap3' in data['chain']) and
                          'bootstrap3-gradients' not in data['chain'])

    return data


def add_category(post, pkg_dir, config, args):
    return {'category': args}


BUILTIN_HANDLERS = {
    'dirname_as_title': dirname_as_title,
    'parse_plugin_file': parse_plugin_file,
    'parse_theme_info': parse_theme_info,
    'add_category': add_category
}


def _parse_handler(handler):
    if callable(handler):
        return handler
    elif handler in BUILTIN_HANDLERS:
        return BUILTIN_HANDLERS[handler]
    else:
        raise ValueError("Unknown pkgindex handler {0!r}".format(handler))


class CompilePackageIndexEntries(PageCompiler):
    """Compile package indexes."""

    name = "pkgindex_compiler"
    friendly_name = "pkgindex_compiler"
    markdown_compiler = None
    pi_enabled = False

    def set_site(self, site):
        """Set site for the compiler."""
        # Workaround for plugins site (which includes those plugins, and makes
        # tests fail)
        if 'PKGINDEX_CONFIG' in site.config:
            self.config = site.config['PKGINDEX_CONFIG']
            self.pi_enabled = True
        super(CompilePackageIndexEntries, self).set_site(site)

    def read_metadata(self, post, file_metadata_regexp=None, unslugify_titles=False, lang=None):
        """Read the metadata from a post, and return a metadata dict."""
        if not self.pi_enabled:
            raise Exception("PKGINDEX_CONFIG not found")

        pkg_dir = os.path.split(post.source_path)[0]
        top_dir = post.folder_relative
        metadata = {'slug': os.path.basename(pkg_dir)}
        for handler in self.site.config['PKGINDEX_HANDLERS'][top_dir]:
            if isinstance(handler, tuple):
                function = _parse_handler(handler[0])
                metadata.update(function(post, pkg_dir, self.config, handler[1]))
            else:
                function = _parse_handler(handler)
                metadata.update(function(post, pkg_dir, self.config))

        return metadata

    def compile(self, source, dest, is_two_file=True, post=None, lang=None):
        """Compile to HTML (by passing through to Markdown compiler)."""
        if self.markdown_compiler is None:
            self.markdown_compiler = self.site.get_compiler('README.md')
        return self.markdown_compiler.compile(source, dest, is_two_file, post, lang)
