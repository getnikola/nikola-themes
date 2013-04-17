"""Create a bunch of themes from config files. Use with care :-)"""
from __future__ import unicode_literals

import codecs
from contextlib import contextmanager
import glob
import os
import shutil
import string
import subprocess
import time

import requests

def read_data(fname):
    with codecs.open(fname, "rb+", "utf-8") as inf:
        data = []
        for line in inf:
            l = line.strip()
            if l and not l.startswith("#"):
                data.append(l)
    return data

swatches = read_data("bootswatch_themes.txt")
themes = read_data("themes.txt")
b_themes = read_data("bootstrap_themes.txt")

## Get the themes from the master branch, and put them in themes

#src = os.path.join('nikola-master', 'nikola', 'data', 'themes')
#for root, dirs, files in os.walk(src):
    #dst_path = os.path.join('themes', os.path.relpath(root, src))
    #if not os.path.isdir(dst_path):
        #os.makedirs(dst_path)
        #for fname in files:
            #fdst_path = os.path.join(dst_path, fname)
            #shutil.copy2(os.path.join(root, fname), fdst_path)

# Create bootswatch-derived themes for bootstrap themes
for swatch in swatches:
    url = '/'.join(('http://bootswatch.com', swatch, 'bootstrap.min.css'))
    min_bs = requests.get(url).text

    url = '/'.join(('http://bootswatch.com', swatch, 'bootstrap.css'))
    bs = requests.get(url).text

    for parent in b_themes:
        name = "{0}_{1}".format(parent, swatch)
        if os.path.isdir(os.path.join('themes', name, 'assets', 'css')):
            continue  # Don't rebuild these all the time
        try:
            os.makedirs(os.path.join('themes', name, 'assets', 'css'))
        except:
            pass
        print "Downloading: ", url
        with open(os.path.join('themes', name, 'assets', 'css', 'bootstrap.min.css'),
                    'wb+') as output:
            output.write(min_bs)
        with open(os.path.join('themes', name, 'assets', 'css', 'bootstrap.css'),
                    'wb+') as output:
            output.write(bs)
        with open(os.path.join('themes', name, 'parent'), 'wb+') as output:
            output.write(parent)

def setup_demo(theme):
    """Create demo site with a theme."""
    path = os.path.join('sites', theme)
    print "Setting up:", path
    if not os.path.isdir(path):
        os.system("nikola init --demo {0}".format(path))
        os.system("sed --in-place \"s/# THEME = 'site'/THEME = '{0}'/\" {1}/conf.py".format(theme, path))
    shutil.rmtree(os.path.join(path, "themes", theme))
    shutil.copytree(os.path.join("themes",theme), os.path.join(path, "themes", theme))
    while os.path.isfile(os.path.join(path, 'themes', theme, 'parent')):
        theme = open(os.path.join(path, 'themes', theme, 'parent')).readline().strip()
        shutil.rmtree(os.path.join(path, "themes", theme))
        shutil.copytree(os.path.join("themes",theme), os.path.join(path, "themes", theme))

for theme in glob.glob('themes/*/'):
    print "Theme:", theme
    setup_demo(os.path.basename(theme[:-1]))

@contextmanager
def cd(path):
    old_dir = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(old_dir)

# Build each site
for site in glob.glob('sites/*/'):
    with cd(site):
        try:
            subprocess.check_call(["nikola", "build"])
        except Exception:
            print "Error building theme:", site
            continue
        p = subprocess.Popen(["nikola", "serve"])
        time.sleep(2)
        print "Snapshotting: ", site
        snap = os.path.join('..', site.split(os.sep)[-2]) + '.png'
        subprocess.check_call(["capty", "http://localhost:8000", snap])
        p.kill()
        time.sleep(1)

for theme in glob.glob('themes/*/'):
    theme = theme.split('/')[-2]
    subprocess.check_call('zip -r sites/{0}.zip themes/{0}'.format(theme), shell=True)

metadata_bit = string.Template("""<!--
.. title: ${theme}
.. slug: ${theme}
.. date: 2013/03/25 16:37:04
.. tags:
.. link:
.. description:
-->""")

theme_bit = string.Template("""
<div class="span5" style="padding: 30px; margin: 10px; border: solid 1px #c4c4c4; border-radius: 5px;">
<h2>${theme}</h2>
${variants}&nbsp;<div class="btn-group"><a href="${demo}" class="btn">View Demo</a><a href="${download}" class="btn">Download</a></div>
<div style="text-align: center; padding: 5px;">
<img src="${image}" style="height: 250px;">
<br>
</div>
</div>
""")

for site in glob.glob('sites/*/'):
    theme = site.split(os.sep)[-2]
    md_bit = metadata_bit.substitute(theme=theme)
    bit = theme_bit.substitute(theme = theme, image = theme+".png", demo = theme+"/output/index.html", variants='', download=theme+'.zip')
    with codecs.open(os.path.join('pages', theme + '.html'), "wb+", "utf8") as outf:
        outf.write(md_bit)
        outf.write(bit)

index_md = """<!--
.. title: Nikola Theme Gallery
.. slug: index
.. date: 2013/03/25 16:37:04
.. tags:
.. link:
.. description:
-->"""
index_bits = []

for theme in b_themes:
    variants = '''
  <div class="btn-group">
  <button class="btn">Variants</button>
  <button class="btn dropdown-toggle" data-toggle="dropdown">
    <span class="caret"></span>
  </button>
    <ul class="dropdown-menu">'''+\
        '\n'.join('<li><a href="{0}.html">{0}</a></li>'.format(theme+'_'+swatch)  for swatch in swatches)+\
    '</ul></div>'

    bit = theme_bit.substitute(theme = theme, image = theme+".png", demo = theme+"/output/index.html", variants=variants, download=theme+'.zip')
    index_bits.append(bit)

for theme in themes:
    bit = theme_bit.substitute(theme = theme, image = theme+".png", demo = theme+"/output/index.html", variants='', download=theme+'.zip')
    index_bits.append(bit)

with codecs.open(os.path.join('pages','index.html'), 'wb+', 'utf8') as outf:
    outf.write(index_md)
    outf.write('\n\n'.join(sorted(index_bits)))
