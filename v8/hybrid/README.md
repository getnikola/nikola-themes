The Hybrid theme is based on the Hyde theme which is a port of the [Hyde theme by mdo](http://hyde.getpoole.com/) combined with features from the Zen theme family:

* ForkAwesome font icons are supported
* fancydates JS plugin is used
* navigation links can be text only or icon only or combined 
* turn blog title and description in navigation bar on/off
* Hyde color schemes are supported

Specify preferences via GLOBAL_CONTEXT variable in the config:

```
    GLOBAL_CONTEXT = {
        "hyde_subtheme": "theme-base-08",
        "sidebar_title": False,
        "navigation": "icon",
    }
```

## Color schemes

* use predefined color scheme by replacing 08 with one of 09, 0a, 0b, 0c, 0d, 0e, 0f
* custom color scheme: edit subtheme name to "theme-custom" and define your colors in ``hybrid.css`` (*background-color* and *color* attribute)
* see ``conf.py.sample`` for details

## Title in sidebar

* set "sidebar_title" to *False* for the Zen look
* set "sidebar_title" to *True* to show blog title and description

## Navigation links

* set "navigation" to *"icon"* for the Zen experience
* set "navigation" to *"text"* for the Hyde experience
* do not set variable for Hybrid view


You can read a tutorial about how to create/port new theme [at Nikola's site](https://getnikola.com/creating-a-theme.html)

(*Note:* The `.sidebar` class was renamed to `.hsidebar` to avoid conflicts with reST.)

License is MIT

Known Issues:

* Not all features of Nikola are tested.
* Galleries will work better when [Issue #1764](https://github.com/getnikola/nikola/issues/1764) is fixed.
* Submenus in navigation links are not supported
