"""Create a bunch of themes from config files. Use with care :-)"""
from __future__ import unicode_literals

import codecs
from contextlib import contextmanager
import glob
import json
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

# Get the themes from the master branch, and put them in themes

src = os.path.join('nikola-master', 'nikola', 'data', 'themes')
for root, dirs, files in os.walk(src):
    dst_path = os.path.join('themes', os.path.relpath(root, src))
    if not os.path.isdir(dst_path):
        os.makedirs(dst_path)
    for fname in files:
        fdst_path = os.path.join(dst_path, fname)
        shutil.copy2(os.path.join(root, fname), fdst_path)

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
    try:
        shutil.rmtree(os.path.join(path, "themes", theme))
    except:
        pass
    shutil.copytree(os.path.join("themes",theme), os.path.join(path, "themes", theme))
    while os.path.isfile(os.path.join(path, 'themes', theme, 'parent')):
        theme = open(os.path.join(path, 'themes', theme, 'parent')).readline().strip()
        try:
            shutil.rmtree(os.path.join(path, "themes", theme))
        except:
            pass
        shutil.copytree(os.path.join("themes",theme), os.path.join(path, "themes", theme))

BASE_URL = "http://themes.nikola.ralsina.com.ar/"
themes_dict = {}
for theme in glob.glob('themes/*/'):
    t_name = os.path.basename(theme[:-1])
    themes_dict[t_name] = BASE_URL + t_name + ".zip"
with open(os.path.join("files", "themes.json"), "wb+") as outf:
    json.dump(themes_dict, outf, sort_keys=True)

for theme in glob.glob('themes/*/'):
    if "site-planetoid" in theme:
        continue  # Not a demoable theme
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

with cd('themes'):
    for theme in glob.glob('*/'):
        theme = theme[:-1]
        subprocess.check_call('zip -r ../sites/{0}.zip {0}'.format(theme), shell=True)

metadata_bit = string.Template("""<!--
.. title: ${theme}
.. slug: ${theme}
.. date: 2013/03/25 16:37:04
.. tags:
.. link:
.. description:
-->""")


voting_js="""
<div class="rw-js-container">
    <script type="text/javascript">
        // Async Rating-Widget initialization.
        function RW_Async_Init(){
            RW.init({
                uid: "EAC95C5D0E24D59DB8E03DE8D8BDB348",
                huid: "100434",
                options: {
                    type: "nero",
                    style: "thumbs"
                }
            });
            RW.render();
        }

        // Append Rating-Widget JavaScript library.
        if (typeof(RW) == "undefined"){
            (function(){
                var rw = document.createElement("script");
                rw.type = "text/javascript"; rw.async = true;
                rw.src = "http://js.rating-widget.com/external.min.js?t=js";
                var s = document.getElementsByTagName("script")[0];
                s.parentNode.insertBefore(rw, s);
            })();
        }

    </script>
</div>
"""


theme_bit = string.Template("""
<div class="span5" style="padding: 30px; margin: 10px; border: solid 1px #c4c4c4; border-radius: 5px;">
<h2>${theme}</h2>
${variants}&nbsp;<div class="btn-group"><a href="${demo}" class="btn">View Demo</a><a href="${download}" class="btn">Download</a></div>
<div style="text-align: center; padding: 5px;">
<img src="${image}" style="height: 250px;">
<br>
</div>
<div class="rw-ui-container rw-urid-${vote}"></div>
</div>
""")

def v_id(s):
    return int(''.join('%03d'% ord(x) for x in s)) % 100000

for site in glob.glob('sites/*/'):
    theme = site.split(os.sep)[-2]
    md_bit = metadata_bit.substitute(theme=theme)
    bit = theme_bit.substitute(theme = theme, image = theme+".png", demo = theme+"/output/index.html", variants='', download=theme+'.zip',
                               vote=v_id(theme))
    with codecs.open(os.path.join('pages', theme + '.html'), "wb+", "utf8") as outf:
        outf.write(md_bit)
        outf.write(bit)
        outf.write(voting_js)

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

    bit = theme_bit.substitute(theme = theme, image = theme+".png", demo = theme+"/output/index.html", variants=variants, download=theme+'.zip', vote=v_id(theme))
    index_bits.append(bit)

for theme in themes:
    bit = theme_bit.substitute(theme = theme, image = theme+".png", demo = theme+"/output/index.html", variants='', download=theme+'.zip', vote=v_id(theme))
    index_bits.append(bit)

with codecs.open(os.path.join('pages','index.html'), 'wb+', 'utf8') as outf:
    outf.write(index_md)
    outf.write('\n\n'.join(sorted(index_bits)))
    outf.write(voting_js)

