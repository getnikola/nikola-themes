#!/usr/bin/env python

"""Make sanity checks on the provided themes."""

from __future__ import unicode_literals, print_function
import codecs
from contextlib import contextmanager
import glob
import os
import shutil
import subprocess

import colorama
from progressbar import ProgressBar

from nikola import utils

def error(msg):
    print(colorama.Fore.RED + "ERROR:" + msg)

def theme_list():
    return [theme.split('/')[-1] for theme in glob.glob("themes/*")]

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
        error("can' t build theme {0}".format(theme))
        raise

    subprocess.check_call('zip -r sites/{0}.zip themes/{0}'.format(theme), stdout=subprocess.PIPE, shell=True)


def init_theme(theme):
    t_path = "/".join(["sites", theme])
    o_path = os.path.abspath("/".join(["output", theme]))
    if os.path.isdir(t_path):
        shutil.rmtree(t_path)
    if os.path.isdir(o_path):
        shutil.rmtree(o_path)
    subprocess.check_call(["nikola", "init", "--demo", t_path], stdout=subprocess.PIPE)
    os.symlink(os.path.abspath("themes"), os.path.abspath("/".join([t_path, "themes"])))

    conf_path = "/".join([t_path,"conf.py"])
    with codecs.open(conf_path, "a", "utf-8") as conf:
        conf.write("\n\nTHEME = '{0}'\n\nOUTPUT_FOLDER = '{1}'\n\n".format(theme, o_path))

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
