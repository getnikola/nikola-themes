# -*- coding: utf-8 -*-

# Copyright © 2016-2020, Chris Warrick.

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

"""ZIP (and JSON) generation for package indexes."""

from __future__ import unicode_literals

import os
import zipfile
import json
from nikola.plugin_categories import Task
from nikola import utils

try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin  # NOQA


def make_zip(files, destination):
    """Make a zip with files and save as destination."""
    utils.makedirs(os.path.dirname(destination))
    with zipfile.ZipFile(destination, 'w', zipfile.ZIP_DEFLATED) as z:
        for filename, arcname in files:
            z.write(filename, arcname)


def write_json(data, destination):
    """Write Python object to a JSON file."""
    with open(destination, 'w', encoding='utf-8') as fh:
        json.dump(data, fh, sort_keys=True, indent=4)


class PackageIndexZip(Task):
    """Generate ZIP files for package indexes."""
    name = "pkgindex_zip"

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

        zip_json = {}
        zip_deps = {}
        for dir in self.site.pkgindex_entries:
            utils.makedirs(os.path.join(
                self.kw['output_folder'],
                self.kw['pkgindex_dirs'][dir][0]
            ))
            zip_json[dir] = {}
            zip_deps[dir] = []

        for dir, posts in self.site.pkgindex_entries.items():
            for post in posts:
                directory = os.path.dirname(post.source_path)
                pkg_name = os.path.basename(directory)
                if pkg_name in self.kw['pkgindex_config'].get('zip_ignore', []):
                    continue
                destination = os.path.join(
                    self.kw['output_folder'],
                    self.kw['pkgindex_dirs'][dir][0],
                    pkg_name + '.zip'
                )
                output_dest = '/'.join((
                    self.kw['pkgindex_dirs'][dir][0],
                    pkg_name + '.zip'
                ))
                for d in post.meta('allver'):
                    zip_json['v{0}'.format(d)][pkg_name] = urljoin(self.kw['base_url'], output_dest)
                    zip_deps['v{0}'.format(d)].append(destination)
                # Prefix to slice out from names
                d = len(directory) - len(pkg_name)
                zip_files = []
                file_dep = []
                # Get list of dependencies and files to zip
                for root, dirs, files in os.walk(directory):
                    for file in files:
                        if file.endswith(('.pyc', '.DS_Store')) or file == '.git':
                            continue
                        zip_files.append((os.path.join(root, file),
                                          os.path.join(root[d:], file)))
                        file_dep.append(os.path.join(root, file))
                yield utils.apply_filters({
                    'basename': self.name,
                    'name': destination,
                    'file_dep': file_dep,
                    'targets': [destination],
                    'actions': [(make_zip, (zip_files, destination))],
                    'clean': True,
                    'uptodate': [utils.config_changed(self.kw, 'pkgindex_zip:' + destination)],
                }, self.kw['filters'])

        # Generate JSON file of {slug: path_to_zip}
        for dir, data in zip_json.items():
            destination = os.path.join(
                self.kw['output_folder'],
                self.kw['pkgindex_dirs'][dir][0],
                self.kw['pkgindex_config']['json_filename']
            )
            yield utils.apply_filters({
                'basename': self.name,
                'name': destination,
                'file_dep': zip_deps[dir],
                'targets': [destination],
                'actions': [(write_json, (data, destination))],
                'clean': True,
                'uptodate': [utils.config_changed(self.kw, 'pkgindex_zip:' + destination)],
            }, self.kw['filters'])
