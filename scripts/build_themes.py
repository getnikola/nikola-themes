#!/usr/bin/env python

"""Make sanity checks on the provided themes."""

from __future__ import unicode_literals, print_function
import codecs
from contextlib import contextmanager
import glob
import json
import os
import shutil
import subprocess

import colorama
from progressbar import ProgressBar

from nikola import utils

BASE_URL = "http://themes.getnikola.com/v6/"

def error(msg):
    print(colorama.Fore.RED + "ERROR:" + msg)

def theme_list():
    return sorted(['base', 'bootstrap', 'bootstrap3'] + [theme.split('/')[-1] for theme in glob.glob("themes/*")])

def build_theme(theme=None):
    if theme is None:  # Check them all
        print("\nBuilding all themes\n")
        progress = ProgressBar()
        for theme in progress(theme_list()):
            build_theme(theme)
        return
    init_theme(theme)

    try:
        with cd("/".join(["sites", theme])):
            subprocess.check_call(["nikola", "build"], stdout=subprocess.PIPE)
    except:
        error("can't build theme {0}".format(theme))
        raise

    if not os.path.isdir(os.path.join("output", "v6")):
        os.mkdir(os.path.join("output", "v6"))

    if os.path.isdir('themes/'+theme):
        with cd('themes/'):
            subprocess.check_call('zip -r ../output/v6/{0}.zip {0}'.format(theme), stdout=subprocess.PIPE, shell=True)
    subprocess.check_call('capty output/v6/{0}/index.html output/v6/{0}.jpg'.format(theme), stdout=subprocess.PIPE, shell=True)

    themes_dict = {}
    for theme in glob.glob('themes/*/'):
        t_name = os.path.basename(theme[:-1])
        themes_dict[t_name] = BASE_URL + t_name + ".zip"
    with open(os.path.join("output", "v6", "themes.json"), "wb+") as outf:
        json.dump(themes_dict, outf, indent=4, ensure_ascii=True, sort_keys=True)


def init_theme(theme):
    t_path = "/".join(["sites", theme])
    o_path = os.path.abspath("/".join(["output", "v6", theme]))
    if os.path.isdir(t_path):
        shutil.rmtree(t_path)
    if os.path.isdir(o_path):
        shutil.rmtree(o_path)
    subprocess.check_call(["nikola", "init", "--demo", t_path], stdout=subprocess.PIPE)
    os.symlink(os.path.abspath("themes"), os.path.abspath("/".join([t_path, "themes"])))

    conf_path = "/".join([t_path,"conf.py"])
    # Get custom required settings from the theme
    themes = utils.get_theme_chain(theme)
    extra_conf_path = utils.get_asset_path('conf.py.sample', themes)
    extra_conf = ''
    if extra_conf_path:
        extra_conf = open(extra_conf_path, 'r').read()

    with codecs.open(conf_path, "a", "utf-8") as conf:
        conf.write("\n\n{2}\n\nTHEME = '{0}'\n\nOUTPUT_FOLDER = '{1}'\n\nSOCIAL_BUTTONS_CODE = ''\n".format(theme, o_path, extra_conf))

@contextmanager
def cd(path):
    old_dir = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(old_dir)

if __name__ == "__main__":
    import commandline
    colorama.init()
    commandline.run_as_main(build_theme)
