Well, I call this theme nikola-bnw(brave new world). No special
meaning. It is hosted on [Github](https://github.com/lotabout/nikola-bnw.git).

# How to use it
1. Download this repository and put it under '/themes/' folder.
2. Modify your conf.py and set THEME = "nikola-bnw".
3. Disable bundles in `conf.py`: `USE_BUNDLES = False`
4. Done!

Note that this theme use `less` as the pre-processor of CSS. So in
order to make this theme work, you have to
1. Install [less plugin](https://plugins.getnikola.com/#less) by
   `nikola plugin -i less`
2. And you have to install external tool [less](http://lesscss.org/)
   by yourself. (`npm install -g less`)

Update: I've generated the css written by `less`, so you don't need to
install `less` now, just do:
1. Modify your `confiy.py` and set `USE_BUNDLES = True`.
2. Done!

Also note that the theme use `flexbox` CSS attribute, so make sure to
use modern browser if it is not working well.

# Another way to Install it
The theme had been added to
[Nikola Theme Gallary](https://themes.getnikola.com/), so you can install
it by:
1. `nikola install_theme bnw`
2. Modify your conf.py and set `THEME = "bnw"`
3. Modify your `confiy.py` and set `USE_BUNDLES = True`.
4. Done!

# Tweak
## Footer
The footer can include several icons(email, github, twitter, rss) according to
your settings. Put the settings in `GLOBAL_CONTEXT` variable in `conf.py`.
Example:
```
GLOBAL_CONTEXT = {
    'email': 'lotabout@gmail.com',
    'twitter': 'lotabout',
    'github': 'lotabout',
}
```

## Color Theme
Thanks to `less`, the color of the theme can be easily changed. All
you need to do is open `nikola-bnw/less/bnw.less` and modify the 4
colors being used:
```
// primary-color: for background
// secondary-color: navbar-links
// third-color: for navbar
// accent-color: for font.
@primary-color: #FCF7F7;
@secondary-color: #ECE1DE;
@third-color: #6B5364;
@accent-color: #304860;
```
Change them to whatever you like.

# Screencast
Well, the index page
![](https://github.com/lotabout/nikola-bnw/blob/master/images-for-readme/index-page.png)

The Post Page(half)
![](https://github.com/lotabout/nikola-bnw/blob/master/images-for-readme/post-page.png)

# LICENSE
MIT License
