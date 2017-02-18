#!/usr/bin/env python

"""Build themes."""

from __future__ import unicode_literals, print_function
import io
import tempfile
from contextlib import contextmanager
import glob
import json
import os
import sys
import shutil
import subprocess
import colorama

from nikola import utils

# s/v7/vX/ to upgrade
BASE_URL = "https://themes.getnikola.com/v7/"
# See index.html — use for identical themes
NO_SCREENSHOTS_AND_DEMOS = ['zen-jinja', 'zen-ipython', 'bootstrap3-jinja', 'bootstrap3-gradients-jinja', 'bootblog-jinja', 'base-jinja']


def error(msg):
    print(colorama.Fore.RED + "ERROR:" + msg)


def theme_list():
    return sorted(['base', 'base-jinja', 'bootstrap3', 'bootstrap3-jinja'] + [theme.split('/')[-1] for theme in glob.glob("v7/*")])


def build_theme(theme=None):
    if theme is None:  # Check them all
        print("\nBuilding all themes\n")
        tl = theme_list()
        ltl = len(tl)
        for i, theme in enumerate(tl):
            print('--- Building theme "{0}" ({1}/{2}) ---'.format(theme, i + 1, ltl))
            build_theme(theme)
        return
    init_theme(theme)

    if theme in NO_SCREENSHOTS_AND_DEMOS:
        print(">> Skipping building demo site for", theme)
    else:
        print(">> Building demo site for", theme)
        try:
            with cd("/".join(["sites", theme])):
                subprocess.check_call(["nikola", "build"], stdout=subprocess.PIPE)
        except:
            error("can't build theme {0}".format(theme))
            raise

    if not os.path.isdir(os.path.join("output", "v7")):
        os.mkdir(os.path.join("output", "v7"))

    if os.path.isdir('v7/' + theme):
        with cd('v7/'):
            # If there is a .git file, move it away for a while (Issues #72 and #76)
            if os.path.exists(os.path.join(theme, '.git')):
                has_tmp = True
                tmpdir = tempfile.mkdtemp()
                shutil.move(os.path.join(theme, '.git'), os.path.join(tmpdir, 'git-bkp'))
            else:
                has_tmp = False

            print(">> Creating ZIP file for", theme)
            subprocess.check_call('zip -r ../output/v7/{0}.zip {0}'.format(theme), stdout=subprocess.PIPE, shell=True)
            if has_tmp:
                shutil.move(os.path.join(tmpdir, 'git-bkp'), os.path.join(theme, '.git'))
                os.rmdir(tmpdir)

    if theme in NO_SCREENSHOTS_AND_DEMOS:
        print(">> Skipping creating screenshot for", theme)
    else:
        try:
            print(">> Creating screenshot with PhantomJS for", theme)
            subprocess.check_call('phantomjs scripts/take_screenshot.js output/v7/{0}/index.html 1024 768 output/v7/{0}.png'.format(theme), stdout=subprocess.PIPE, shell=True)
        except subprocess.CalledProcessError:
            print(">> Creating screenshot with Capty (!) for", theme)
            subprocess.check_call('capty output/v7/{0}/index.html output/v7/{0}.png'.format(theme), stdout=subprocess.PIPE, shell=True)

        try:
            print(">> Optimizing screenshot for", theme)
            subprocess.check_call('optipng output/v7/{0}.png'.format(theme), stdout=subprocess.PIPE, shell=True)
        except subprocess.CalledProcessError:
            pass

    themes_dict = {}
    for theme in glob.glob('v7/*/'):
        t_name = os.path.basename(theme[:-1])
        themes_dict[t_name] = BASE_URL + t_name + ".zip"
    with io.open(os.path.join("output", "v7", "themes.json"), "w+", encoding="utf-8") as outf:
        json.dump(themes_dict, outf, indent=4, ensure_ascii=True, sort_keys=True)


def init_theme(theme):
    t_path = "/".join(["sites", theme])
    o_path = os.path.abspath("/".join(["output", "v7", theme]))
    if os.path.isdir(t_path):
        shutil.rmtree(t_path)
    if os.path.isdir(o_path):
        shutil.rmtree(o_path)
    subprocess.check_call(["nikola", "init", "-qd", t_path], stdout=subprocess.PIPE)
    os.symlink(os.path.abspath("v7"), os.path.abspath("/".join([t_path, "themes"])))

    conf_path = "/".join([t_path, "conf.py"])
    # Get custom required settings from the theme
    themes = utils.get_theme_chain(theme, themes_dirs=['v7', 'themes'])
    extra_conf_path = utils.get_asset_path('conf.py.sample', themes)
    extra_conf = ''
    if extra_conf_path:
        extra_conf = io.open(extra_conf_path, 'r', encoding="utf-8").read()

    with io.open(conf_path, "a", encoding="utf-8") as conf:
        conf.write(u"\n\n{2}\n\nTHEME = '{0}'\n\nUSE_BUNDLES = False\n\nOUTPUT_FOLDER = '{1}'\n\nSOCIAL_BUTTONS_CODE = ''\nUSE_BASE_TAG = False\n".format(theme, o_path, extra_conf))


@contextmanager
def cd(path):
    old_dir = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(old_dir)

if __name__ == "__main__":
    colorama.init()
    if len(sys.argv) == 1:
        build_theme()
    else:
        for a in sys.argv[1:]:
            build_theme(a)
