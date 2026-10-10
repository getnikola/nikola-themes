# Copyright © 2016-2019, Chris Warrick.

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

import json
import shutil
import subprocess
import sys
from contextlib import chdir
from pathlib import Path

from nikola import utils
from nikola.plugin_categories import Task
from PIL import Image

LOREM_BASE = 'lorem-ipsum.rst'
IGNORED_SUFFIXES = ('.pyc', '.DS_Store')


def theme_files(theme_dir):
    """List the files of a theme, as strings for doit."""
    return [
        str(path) for path in Path(theme_dir).rglob('*')
        if path.is_file() and not path.name.endswith(IGNORED_SUFFIXES) and path.name != '.git'
    ]


def build_demo(theme, themes_dir, demo_source, demo_destination):
    demo_source = Path(demo_source)
    demo_destination = Path(demo_destination).absolute()
    for path in (demo_source, demo_destination):
        if path.is_dir():
            shutil.rmtree(path)
    sys.stderr.write(f'=> Building {theme}...\n')
    subprocess.check_call(['nikola', 'init', '-qd', demo_source], stdout=subprocess.PIPE)
    (demo_source / 'themes').absolute().symlink_to(Path(themes_dir).absolute())

    # Get custom required settings from the theme
    themes = utils.get_theme_chain(theme, themes_dirs=[themes_dir, 'themes'])
    engine_path = utils.get_asset_path('engine', themes)
    extra_conf_path = utils.get_asset_path('conf.py.sample', themes)
    extra_conf = ''
    if extra_conf_path:
        extra_conf = Path(extra_conf_path).read_text(encoding='utf-8')
    if engine_path and Path(engine_path).read_text(encoding='utf-8').strip() == 'jinja':
        shutil.copy('book-jinja.tmpl', demo_source / 'templates' / 'book.tmpl')

    with (demo_source / 'conf.py').open('a', encoding='utf-8') as conf:
        conf.write(
            f"\n\nTHEME = '{theme}'\n"
            'USE_BUNDLES = False\n'
            f'OUTPUT_FOLDER = {json.dumps(str(demo_destination))}\n'
            "SOCIAL_BUTTONS_CODE = ''\n"
            'USE_BASE_TAG = False\n'
            f'\n{extra_conf}\n'
        )

    shutil.copy(LOREM_BASE, demo_source / 'posts' / 'lorem-ipsum.rst')

    with chdir(demo_source):
        subprocess.check_call(['nikola', 'build'], stdout=subprocess.PIPE)

    sys.stderr.write(f'=> Done building {theme}\n')


def take_screenshot(index, destination):
    """Take a screenshot of the demo site and save as destination."""
    subprocess.check_call(['node', 'take_screenshot.js', index, '1024', '768', destination])
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
    name = 'pkgindex_theme_demo_screenshots'

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
            'revision': '2',
        }
        yield self.group_task()
        self.site.scan_posts()

        output_folder = Path(self.kw['output_folder'])
        for index_dir, posts in self.site.pkgindex_entries.items():
            index_output = self.kw['pkgindex_dirs'][index_dir][0]
            for post in posts:
                directory = Path(post.source_path).parent
                pkg_name = directory.name
                version = post.folder_relative.split('v')[-1]
                if int(version) not in self.kw['pkgindex_config']['build_demos_for']:
                    continue
                if f'{post.folder_relative}/{pkg_name}' in self.kw['pkgindex_config']['demo_screenshots_map']:
                    # the map is effectively an ignore list
                    continue

                # doit task names and dependencies are kept as strings
                demo_source = str(Path('demo_sites') / index_output / pkg_name)
                demo_destination = str(output_folder / index_output / pkg_name / 'demo')
                png_destination = str(output_folder / index_output / f'{pkg_name}.png')
                png_thumbnail_destination = str(output_folder / index_output / f'{pkg_name}.thumbnail.png')
                index = str(Path(demo_destination) / 'index.html')

                # those are separate variables to avoid cyclic dependencies
                file_dep = theme_files(directory) + [LOREM_BASE]
                file_dep_png = file_dep + [index]

                yield utils.apply_filters({
                    'basename': self.name,
                    'name': demo_destination,
                    'file_dep': file_dep,
                    'targets': [index],
                    'actions': [(build_demo, (pkg_name, index_dir, demo_source, demo_destination))],
                    'clean': True,
                    'uptodate': [utils.config_changed(self.kw, f'pkgindex_demo:{demo_destination}')],
                }, self.kw['filters'])

                yield utils.apply_filters({
                    'basename': self.name,
                    'name': png_destination,
                    'file_dep': file_dep_png,
                    'targets': [png_destination],
                    'actions': [(take_screenshot, (index, png_destination))],
                    'clean': True,
                    'uptodate': [utils.config_changed(self.kw, f'pkgindex_screenshot:{png_destination}')],
                }, self.kw['filters'])

                yield utils.apply_filters({
                    'basename': self.name,
                    'name': png_thumbnail_destination,
                    'file_dep': [png_destination],
                    'targets': [png_thumbnail_destination],
                    'actions': [(make_thumbnail, (png_destination, png_thumbnail_destination))],
                    'clean': True,
                    'uptodate': [utils.config_changed(self.kw, f'pkgindex_screenshot_thumbnail:{png_destination}')],
                }, self.kw['filters'])
