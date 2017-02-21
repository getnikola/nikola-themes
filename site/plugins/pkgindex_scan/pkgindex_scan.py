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

"""Post scanner for package indexes."""

from __future__ import unicode_literals

import glob
import sys
import os

from nikola import utils
from nikola.post import Post
from nikola.plugin_categories import PostScanner

LOGGER = utils.get_logger('pkgindex_scan', utils.STDERR_HANDLER)


class PackageIndexScanner(PostScanner):
    """Scanner for package indexes."""

    name = "pkgindex_scan"

    def scan(self):
        """Scan posts in a package index."""
        if 'PKGINDEX_CONFIG' not in self.site.config:
            return []
        config = self.site.config['PKGINDEX_CONFIG']
        compiler = self.site.get_compiler('sample' + config['extension'])
        if not self.site.quiet:
            print("Scanning package index posts...", end='', file=sys.stderr)
        timeline = []
        self.site.pkgindex_entries = {}
        for topdir, dirsettings in self.site.config['PKGINDEX_DIRS'].items():
            destination, template_name = dirsettings
            self.site.pkgindex_entries[topdir] = []
            for pkgdir in glob.glob(topdir + "/*"):
                if not os.path.isdir(pkgdir):
                    # Ignore non-directories
                    continue
                post = Post(
                    os.path.join(pkgdir, 'README.md'),
                    self.site.config,
                    destination,
                    False,
                    self.site.MESSAGES,
                    template_name,
                    compiler
                )
                post.is_two_file = True
                timeline.append(post)
                self.site.pkgindex_entries[topdir].append(post)

        if 'special_entries' in config:
            for source_path, destination, template_name, topdir in config['special_entries']:
                post = Post(
                    source_path,
                    self.site.config,
                    destination,
                    False,
                    self.site.MESSAGES,
                    template_name,
                    compiler
                )
                post.is_two_file = True
                timeline.append(post)
                self.site.pkgindex_entries[topdir].append(post)

        return timeline
