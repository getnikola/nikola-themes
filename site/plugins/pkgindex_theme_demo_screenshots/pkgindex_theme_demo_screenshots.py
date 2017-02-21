# -*- coding: utf-8 -*-

# Copyright © 2016-2017, Chris Warrick.

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

"""Demo and screenshot generation for package indexes."""

from __future__ import unicode_literals

import os
import sys
import io
import shutil
import subprocess
from contextlib import contextmanager
from nikola.plugin_categories import Task
from nikola import utils
from PIL import Image

try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin  # NOQA


@contextmanager
def cd(path):
    old_dir = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(old_dir)


def build_demo(theme, themes_dir, demo_source, demo_destination):
    demo_destination = os.path.abspath(demo_destination)
    if os.path.isdir(demo_source):
        shutil.rmtree(demo_source)
    if os.path.isdir(demo_destination):
        shutil.rmtree(demo_destination)
    sys.stderr.write('=> Building {}...\n'.format(theme))
    subprocess.check_call(["nikola", "init", "-qd", demo_source], stdout=subprocess.PIPE)
    os.symlink(os.path.abspath(themes_dir), os.path.abspath("/".join([demo_source, "themes"])))

    conf_path = "/".join([demo_source, "conf.py"])
    # Get custom required settings from the theme
    themes = utils.get_theme_chain(theme, themes_dirs=[themes_dir, 'themes'])
    extra_conf_path = utils.get_asset_path('conf.py.sample', themes)
    extra_conf = ''
    if extra_conf_path:
        extra_conf = io.open(extra_conf_path, 'r', encoding="utf-8").read()

    with io.open(conf_path, "a", encoding="utf-8") as conf:
        conf.write(u"\n\n{2}\n\nTHEME = '{0}'\n\nUSE_BUNDLES = False\n\nOUTPUT_FOLDER = '{1}'\n\nSOCIAL_BUTTONS_CODE = ''\nUSE_BASE_TAG = False\n".format(theme, demo_destination, extra_conf))

    with cd(demo_source):
        subprocess.check_call(["nikola", "build"], stdout=subprocess.PIPE)

    sys.stderr.write('=> Done building {}\n'.format(theme))


def take_screenshot(index, destination):
    """Take a screenshot of the demo site and save as destination."""
    subprocess.check_call(['phantomjs', '../scripts/take_screenshot.js', index, '1024', '768', destination])
    subprocess.call(['optipng', destination])


def make_thumbnail(src, dest):
    """Make a thumbnail of the screenshot."""
    im = Image.open(src)
    im = im.crop((0, 0, 1024, 768))
    im.thumbnail((400, 300))
    im.save(dest)
    subprocess.call(['optipng', dest])


class PackageIndexThemeDS(Task):
    """Generate demos and screenshots for themes."""
    name = "pkgindex_theme_demo_screenshots"

    def gen_tasks(self):
        if 'PKGINDEX_CONFIG' not in self.site.config:
            return
        self.kw = {
            'output_folder': self.site.config['OUTPUT_FOLDER'],
            'filters': self.site.config['FILTERS'],
            'pkgindex_dirs': self.site.config['PKGINDEX_DIRS'],
            'pkgindex_handlers': self.site.config['PKGINDEX_HANDLERS'],
            'pkgindex_config': self.site.config['PKGINDEX_CONFIG'],
            'base_url': self.site.config['BASE_URL'],
        }
        yield self.group_task()
        self.site.scan_posts()

        demo_deps = {}
        for dir, posts in self.site.pkgindex_entries.items():
            demo_deps[dir] = []
            for post in posts:
                directory = os.path.dirname(post.source_path)
                pkg_name = os.path.basename(directory)
                output_dir = post.folder_relative + '/' + pkg_name
                if output_dir in self.kw['pkgindex_config']['demo_screenshots_map']:
                    # the map is effectively an ignore list
                    continue

                demo_source = os.path.join(
                    'demo_sites',
                    self.kw['pkgindex_dirs'][dir][0],
                    pkg_name
                )
                demo_destination = os.path.join(
                    self.kw['output_folder'],
                    self.kw['pkgindex_dirs'][dir][0],
                    pkg_name, 'demo'
                )
                png_destination = os.path.join(
                    self.kw['output_folder'],
                    self.kw['pkgindex_dirs'][dir][0],
                    pkg_name + '.png'
                )
                png_thumbnail_destination = os.path.join(
                    self.kw['output_folder'],
                    self.kw['pkgindex_dirs'][dir][0],
                    pkg_name + '.thumbnail.png'
                )

                index = os.path.join(demo_destination, 'index.html')

                demo_deps[dir].append(demo_destination)
                # Prefix to slice out from names
                d = len(directory) - len(pkg_name)
                zip_files = []
                file_dep = []
                # Get list of dependencies and files to zip
                for root, dirs, files in os.walk(directory):
                    for file in files:
                        if file.endswith(('.pyc', '.DS_Store')):
                            continue
                        zip_files.append((os.path.join(root, file),
                                          os.path.join(root[d:], file)))
                        file_dep.append(os.path.join(root, file))
                file_dep_png = file_dep + [index]

                yield utils.apply_filters({
                    'basename': self.name,
                    'name': demo_destination,
                    'file_dep': file_dep,
                    'targets': [index],
                    'actions': [(build_demo, (pkg_name, dir, demo_source, demo_destination))],
                    'clean': True,
                    'uptodate': [utils.config_changed(self.kw, 'pkgindex_demo:' + demo_destination)],
                }, self.kw['filters'])

                yield utils.apply_filters({
                    'basename': self.name,
                    'name': png_destination,
                    'file_dep': file_dep_png,
                    'targets': [png_destination],
                    'actions': [(take_screenshot, (index, png_destination))],
                    'clean': True,
                    'uptodate': [utils.config_changed(self.kw, 'pkgindex_screenshot:' + png_destination)],
                }, self.kw['filters'])

                yield utils.apply_filters({
                    'basename': self.name,
                    'name': png_thumbnail_destination,
                    'file_dep': [png_destination],
                    'targets': [png_thumbnail_destination],
                    'actions': [(make_thumbnail, (png_destination, png_thumbnail_destination))],
                    'clean': True,
                    'uptodate': [utils.config_changed(self.kw, 'pkgindex_screenshot_thumbnail:' + png_destination)],
                }, self.kw['filters'])
