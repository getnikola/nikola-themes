# -*- coding: utf-8 -*-

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
        self.site.pkgindex_by_name = {}
        self.site.pkgindex_multiver = {}
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
                for d in post.meta.values():
                    d['is_special_entry'] = False
                timeline.append(post)
                self.site.pkgindex_entries[topdir].append(post)
                self._update_name_multiver(post)

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
                for d in post.meta.values():
                    d['is_special_entry'] = True
                timeline.append(post)
                self.site.pkgindex_entries[topdir].append(post)
                self._update_name_multiver(post)

        # But wait, we need to change tags on multiver stuff!
        # This is kinda... hacky...
        maxver = config['versions_supported'][-1]
        for versions in self.site.pkgindex_multiver.values():
            versions = sorted(versions, key=lambda post: post.meta('dirver'))
            v2p = {}
            for post in versions:
                dirver = post.meta('dirver')
                for v in range(dirver, maxver + 1):
                    v2p[v] = post

            p2v = {}
            for v, p in v2p.items():
                if p in p2v:
                    p2v[p].append(v)
                else:
                    p2v[p] = [v]

            for post, versions in p2v.items():
                # And finally, update tags.
                tags = post._tags[self.site.default_lang]
                tags = [i for i in tags if not (i.startswith('v') and i[1:].isdigit())]
                tags += ['v{0}'.format(i) for i in versions]
                tags.append('multiver')
                post._tags[self.site.default_lang] = tags
                post.meta['en']['tags'] = tags
                post.meta['en']['multiver'] = True
                post.meta['en']['allver'] = versions
                if not post.meta['en']['maxver'] and versions[-1] != maxver:
                    post.meta['en']['maxver'] = versions[-1]

        # And generate self.site.pkgindex_by_version
        self.site.pkgindex_by_version = {i: [] for i in config['versions_supported']}
        for l in self.site.pkgindex_entries.values():
            for post in l:
                for version in post.meta['en']['allver']:
                    self.site.pkgindex_by_version[version] = post

        return timeline

    def supported_extensions(self):
        """Return a list of supported file extensions, or None if such a list isn't known beforehand."""
        if 'PKGINDEX_CONFIG' not in self.site.config:
            return None
        return [self.site.config['PKGINDEX_CONFIG']['extension']]

    def _update_name_multiver(self, post):
        name = post.meta('slug')

        if name in self.site.pkgindex_by_name:
            self.site.pkgindex_by_name[name].append(post)
            multiver = True
        else:
            self.site.pkgindex_by_name[name] = [post]
            multiver = False

        if multiver:
            self.site.pkgindex_multiver[name] = self.site.pkgindex_by_name[name]
