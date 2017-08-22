cadair-nikola-theme
===================

Cadair's Nikola theme

This theme is based around a simple homepage with a pretty picture
in a bootstrap3 jumbotron. It also includes the IPython css so it should work
ok with IPython notebooks.

Preview: http://i.imgur.com/wCcE7kx.png

## Customising

If you create a sub-theme of this theme and create a template which is a copy
of `homepage_helper.tmpl` you can customise the image credit text and if you
place a new file under `assets/img/home_banner.jpg` you can customise the
jumbotron image.
There is also the option to put custom code on the right hand side of the Nav
Bar using the `GLOBAL_CONTEXT` varible in `conf.py` define a key in the
dictionary with the name `'cadair_social_links'`. 
