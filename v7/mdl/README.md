# Nikola MDL Mako Template

This theme is based from [Material Design Lite](http://www.getmdl.io/)
templates. It gets the idea from the [blog example](http://www.getmdl.io/templates/blog/index.html). This theme is for
[Nikola](https://getnikola.com/) static site generator and used Mako templates.
The RSS feed icon is getting from
[Community Icons](https://materialdesignicons.com/icon/rss-box)

## Installation

To install:

Enter the command line below at the console

```
$ nikola install_theme mdl
```

Edit ``conf.py`` for setting these values below:

* ``THEME = "mdl"``

Refer to
[Customizing Your Site](https://getnikola.com/handbook.html#customizing-your-site)
for more information. If ``post_type`` is used, it accepts a dictionary value,
where ``key`` is the post meta type and value is the icon name from
[Google Material Design Icons](https://www.google.com/design/icons/). There is
an example in ``Customization`` section.

## Style development

You can skip this section if the theme is going to be used as it is. As the
final ``styles.css`` is generated and placed in ``assets/css`` folder.

The css file is generated using [SASS](http://sass-lang.com/) compiler. If you
have it installed, you can generate the final ``styles.css`` file by calling
``make`` as there is a ``Makefile`` that contains the generation commands.

If you want to add custom styles in custom.scss or custom.css, set ``mdl__custom_css`` to ``True``. Both files are git-ignored.

## JavaScript development

If you want to add custom JavaScript in custom.js, set ``mdl__custom_js`` to ``True``. The custom.js file is git-ignored.

## Components

Here are the components that used in this theme

* Buttons (mdl-button) on site buttons
* Cards (mdl-card) on post, story and gallery
* Layout (mdl-layout) on site layout
* Navigation (mdl-navigation) on top and drawer navigations
* Grid (mdl-grid) on site grid
* Footer (mdl-mega-footer or mdl-mini-footer)
* List (mdl-list)
* Menus (mdl-menu) on more button in navigation
* Text Fields (mdl-textfield) not in the theme but you might need it on search
  box
* Tooltips (mdl-tooltip) not in the theme but you might need it on search box

## Customization

It supports some variables in the config file (conf.py). Below are the default
values except ``post_type``, where is ``{}``:

```python
    GLOBAL_CONTEXT = {
        "mdl__version": "1.3.0",
        "mdl__color_scheme": "indigo-pink",
        "mdl__roboto_font": False,
        "mdl__late_load_css": False,
        "mdl__cachebusting": "1",
        "mdl__fixed_header": False,
        "mdl__fixed_drawer": False,
        "mdl__no_drawer_button": False,
        "mdl__no_desktop_drawer_button": False,
        "mdl__multiple_header": False,
        "mdl__header_scroll": False,
        "mdl__header_waterfall": False,
        "mdl__header_waterfall_hide_top": False,
        "mdl__header_transparent": False,
        "mdl__header_seamed": False,
        "mdl__footer": "",
        "mdl__navigation_large_screen_only": False,
        "mdl__drawer_small_screen_only": False,
        "mdl__custom_css": False,
        "mdl__custom_js": False,
        "drawer_title": "",
        "drawer_logo_url": "",
        "drawer_show_title": "",
        "drawer_description": "",
        "drawer_note": "",
        "title_row_middle": False,
        "navigation_row_middle": False,
        "breadcrumb_separator": ">",
        "post_type": {
            "text": "format_align_justify",
        },
        "top_nav_header": False,
        "more_button_header": [
            ("/mobile/", "Mobile Site", "Mobile"),
        ],
        "image_plugin": "colorbox",
    }
```

* ``mdl__version`` is ``Material Design Lite`` version number
* ``mdl__color_scheme`` is
  [colour scheme](http://www.getmdl.io/customize/index.html) from
  ``Material Design Lite``
* ``mdl__roboto_font`` is a flag whether Roboto font is used, refer to
  [styles documentation](http://www.getmdl.io/styles/index.html)
* ``mdl__late_load_css`` is a flag whether CSS styles are deferred, refer to
  [Optimize CSS Delivery](https://developers.google.com/speed/docs/insights/OptimizeCSSDelivery)
* ``mdl__cachebusting`` is a flag solving the cache problem for CSS and JavaScript files.

### Layout

Additional optional MDL classes for outer div element:

* When ``mdl__fixed_header`` is ``True``, class ``mdl-layout--fixed-header``
  is applied for making the header always visible, even in small screens
* When ``mdl__fixed_drawer`` is ``True``, class ``mdl-layout--fixed-drawer``
  is applied for making the drawer always visible and open in larger screens
* When ``mdl__no_drawer_button`` is ``True``, class
  ``mdl-layout--no-drawer-button`` is applied for not displaying a drawer
  button
* When ``mdl__no_desktop_drawer_button`` is ``True``, class
  ``mdl-layout--no-desktop-drawer-button`` is applied for not displaying a
  drawer button in desktop mode

### Header

* When ``mdl__multiple_header`` is ``True``, logo and title will be first line
  and top navigation will move to second line
* When ``title_row_middle`` is ``True``, title row (or first line in multiple
  header lines) will position in the middle

Additional optional MDL classes for header element:

* When ``mdl__header_scroll`` is ``True``, class ``mdl-layout__header--scroll``
  is applied for making the header scroll with the content and mutually
  exclusive with ``mdl__fixed_header``
* When ``mdl__header_waterfall`` is ``True``, class
  ``mdl-layout__header--waterfall`` is applied for allowing a "waterfall"
  effect with multiple header lines
* When ``mdl__header_waterfall_hide_top`` is ``True``, class
  ``mdl-layout__header--waterfall-hide-top`` is applied for hiding the top
  rather than the bottom rows on a waterfall header
* When ``mdl__header_transparent`` is ``True``, class
  ``mdl-layout__header--transparent`` is applied for making header transparent
  (draws on top of layout background)
* When ``mdl__header_seamed`` is ``True``, class ``mdl-layout__header--seamed``
  is applied for using a header without a shadow

### footer

* By default, ``mdl__footer`` is empty. But it could be also either
  ``mdl-mega-footer`` or ``mdl-mini-footer`` or even any custom classes, refer
  to [footer documentation]
  (http://www.getmdl.io/components/index.html#layout-section/footer)

### Navigation

* When ``mdl__navigation_large_screen_only`` is ``True``, it hides navigation
  row in multiple header lines on smaller screens
* When ``navigation_row_middle`` is ``True``, navigation row (second line) in
  multiple header lines will position in the middle

### Drawer

* When ``mdl__drawer_small_screen_only`` is ``True``, it hides drawer on larger
  screens
* ``drawer_title`` is the title in the drawer and it could be set the same as
  ``BLOG_TITLE``
* ``drawer_logo_url`` is the logo url in the drawer and final output is
  <img src="drawer_logo_url" alt="drawer_title">
* The default of ``drawer_show_title`` is ``False``. It hides the drawer title
  (for example, if drawer logo already contains the text).  
* ``drawer_description`` is more HTML text between ``drawer_title`` and drawer
  navigation
* ``drawer_note`` is more HTML text after drawer navigation

### Others

* When [Post Types](https://getnikola.com/handbook.html#post-types) feature in
  [Nikola](https://getnikola.com/) is used, ``post_type`` can used to style
  different type of posts.
* When ``top_nav_header`` is true, navigation will visible when top header is
  appeared on wider screen.
* When ``more_button_header`` is true, more button at top menu header will visible
  after search button. It is a tuple list, where
  ``("URL", "title", "menu name")`` as format.
* String value ``image_plugin`` is either empty string, ``lightbox`` or
  ``colorbox``. It it is empty string, no image plugin will be used. If it is
  ``colorbox``, [colorbox](http://www.jacklmoore.com/colorbox/) script is used
  to view full images. It is the same image library as
  [Nikola](https://getnikola.com/) used. If it is ``lightbox``,
  [lightbox](http://lokeshdhakar.com/projects/lightbox2/) script is used to view
  full images in gallery pages.
* Add meta 'type' and 'hidetitle' to 'story' page.
* Add meta 'no-card-shadow' and 'no-card-media' to 'post' and 'story' pages.

## Depreciated GLOBAL_CONTEXT

* ``mdl_version`` is replaced with ``mdl__version``
* ``color_scheme`` is replaced with ``mdl__color_scheme``
* ``roboto_font`` is replaced with ``mdl__roboto_font``
* ``mega_footer`` (boolean type) is replaced with ``mdl__footer`` (string type)

## Depreciated classes

* ``theme-blog`` is replaced with ``site``
* ``theme-blog__posts`` is replaced with ``site-posts``
* ``theme-blog__post`` is replaced with ``site-post``
* ``theme-blog__gallery`` is replaced with ``site-gallery``
* ``theme-blog__page`` is replaced with ``site-page``
* ``theme-blog__listing`` is replaced with ``site-listing``
* ``theme-card`` is replaced with ``site-card``
* ``theme-nav`` is replaced with ``site-navigation``
* ``theme-nav__button`` is replaced with ``site-navigation__button``
* ``previous`` is replaced with ``site-navigation__previous``
* ``next`` is replaced with ``site-navigation__next``
* ``theme-crumbs`` is replaced with ``site-breadcrumbs``
* ``searchform`` is replaced with ``site-header__search``

## New classes

* ``site-header``
* ``site-header__title-row``
* ``site-header__navigation-row``
* ``site-header__row-middle``
* ``site-header__navigation``
* ``site-header__more-button``
* ``site-title``
* ``site-drawer``
* ``site-drawer__title``
* ``site-drawer__description``
* ``site-drawer__navigation``
* ``site-drawer__note``
* ``metadata``
* ``site-post__author``
* ``site-post__date``
* ``site-post__total-comment``
* ``site-post__tag``
* ``site-post__source-link``
* ``site-post__source-link``
* ``site-page-list``
* ``site-page-list-post``
* ``site-page-story``
* ``site-page-tags``
* ``site-page-tag``
* ``site-footer``

## Known Issues

* Not all features of Nikola are tested
* ``slideshow`` is not working
* Submenus in navigation links are not supported
* ``THEME_COLOR`` is not used regardless the value
* Not meet WCAG 2.0 level AA

## Dependencies

* [Material Design Lite](https://getmdl.io)
* [jQuery](https://jquery.org)
* [Colorbox](http://www.jacklmoore.com/colorbox)
* [Lightbox](http://lokeshdhakar.com/projects/lightbox2)

## License

Material Design Lite [Apache License Version 2.0](https://github.com/google/material-design-lite/blob/master/LICENSE)

Google Material Design Icons - [Attribution 4.0 International](https://github.com/google/material-design-icons/blob/master/LICENSE)

RSS Feed Icons - [SIL Open Font License 1.1](http://scripts.sil.org/cms/scripts/page.php?item_id=OFL_web)

jQuery - [MIT License](https://jquery.org/license/)

Colorbox - [MIT License](http://opensource.org/licenses/mit-license.php)

Lightbox - [MIT License](https://github.com/lokesh/lightbox2/blob/master/LICENSE)

Templates - [Apache License Version 2.0](https://github.com/ivanteoh/nikola-mdl-mako/blob/master/LICENSE)
