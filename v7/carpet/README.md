# Carpet

Nikola theme based from [Bulma](http://bulma.io/). [Nikola](https://getnikola.com/)
is a static site and blog generator. Template is using
[Mako](http://www.makotemplates.org/) syntax and
[Font Awesome 4](http://fontawesome.io/) icons.

## Installation

To install:

Enter the command line below at the console

```
$ nikola install_theme carpet
```

Edit ``conf.py`` for setting these values below:

* ``THEME = "carpet"``

Default extra global context values:

```python
GLOBAL_CONTEXT = {
     "carpet__unlink_blog_brand": False,
     "carpet__show_hero": False,
     "carpet__show_hero_title": False,
     "carpet__hero_post_title": False,
     "carpet__hero_size": "",
     "carpet__hero_footer": "",
     "carpet__late_load_css": False,
     "carpet__breadcrumb_home": "",
     "carpet__breadcrumb_separator": "",
     "carpet__post_type": {},
     "carpet__head_prefix": "",
     "carpet__body_prefix": "",
     "carpet__content_prefix": "",
     "carpet__content_suffix": "",
     "carpet__cookie_message": ""
}
```

Extra Metadata

* hero-class
* show-hero
* hero-title
* hero-description

## Blog brand

By default, the blog brand is a link for either blog logo or/and blog title by
having values on **[configuration file](https://getnikola.com/conf.html)**. For
example,

```python
BLOG_TITLE = AUTHOR_NAME
LOGO_URL = "/logo.png"
SHOW_BLOG_TITLE = True
```

If you don't want them to be a link, set ``carpet__unlink_blog_brand`` to
**True**.

## Hero

This theme supports Hero feature from [Bulma](http://bulma.io/). If you
like to turn on the feature, set ``carpet__show_hero`` to **True**.

### Custom Hero background 
By default the background colour of the Hero is primary colour, same colour as
the top navigation. There are few classes can be used for background
customisation. 

* The ``hero-body`` class is appeared in all the Hero.
* Each pages have ``hero-${title|lower,h,trim}`` class too, where title is the
  page title with all lower case, and number with no special characters
  (including space characters).
* All ``POSTS`` and ``PAGES`` can also have extra classes by adding value to
  ``hero-class`` metadata.

### Custom Hero title

By default, there is no text in the Hero. If the feature is turn on, by default
the text will show ``BLOG_TITLE`` and/or ``BLOG_DESCRIPTION`` depending if the
values are not empty. Here are few more customisation:

* All ``POSTS`` and ``PAGES`` have the same hero text, set
  ``carpet__show_hero_title`` to **True**. 
* To customise all ``POSTS`` and ``PAGES`` with different Hero text, set
  ``carpet__hero_post_title`` to **True**. Only those pages that accept
  metadata values.
  * By default, there is no Hero text.
  * Turn on hero text in each ``POSTS`` page, set ``show-hero`` metadata to
    **True**. It will show the default values, which are ``BLOG_TITLE`` and/or ``BLOG_DESCRIPTION`` depending if the values are not empty.
  * To customise each ``POSTS`` page, set ``show-hero`` to ``custom``. It will
    use ``hero-title`` and/or ``hero-description`` depending if the values are
    not empty.

### Custom Hero size

There are few sizes come with [Bulma](http://bulma.io/) Hero, ``is-medium``,
``is-large`` and ``is-fullheight``. Change these values to
``carpet__hero_size``. Refer to
[Bulma Hero](http://bulma.io/documentation/layout/hero/) for more info.

### Custom Hero footer

If you like to have Hero footer, add value to ``carpet__hero_footer``.

## Breadcrumb

Be default, breadcrumb doesn't have any icons. If you like to have icons on either breadcrumb home and/or separators, here are the example values:

```python
GLOBAL_CONTEXT = {
  "carpet__breadcrumb_home": "fa-home",
  "carpet__breadcrumb_separator": "fa-angle-right"
}
```

## Post type

If you are using post type features, you can have different icons for different post types. Below are examples values:

```python
GLOBAL_CONTEXT = {
  "carpet__post_type": {
      "text": "fa-file-text-o",
      "quote": "fa-quote-right",
      "book": "fa-book",
      "recipe": "fa-bookmark",
      "link": "fa-link",
      "video": "fa-film",
      "photo": "fa-image-o"
  }
}
```

## Custom colour theme

Currently, there is no easy way to change the theme colour. In order to do it,
you need to regenerate the CSS files. Here are the steps:

* At the root of the theme, enter this command in the console / terminal,
  ``make install``. It will install all the JavaScript packages that needed for
  regenerating the CSS files.
* All the custom styles that depending on
  [Bulma variables ](http://bulma.io/documentation/overview/variables/)
  need to be before import statement in ``src/scss/main.scss`` files. For
  example, in this theme, the primary color is changed to ``#445826``.
* After all customisation, enter this command in the console / terminal,
  ``make build``. It will regenerate all the CSS files and place them in ``assets/css/`` folder.

## Optimise CSS delivery 

Anyone who is interested in [Optimise CSS delivery](https://developers.google.com/speed/docs/insights/OptimizeCSSDelivery), this theme manage to improve it using
[Critical](https://github.com/addyosmani/critical/blob/master/README.md)
tool. Here are the steps:

* At the root of the theme, enter this command in the console / terminal,
  ``make install``. It will install all the JavaScript packages that needed for
  generating critical-path CSS.
* Firstly,
  * set ``carpet__late_load_css`` to **False**
  * For best result, set ``USE_BUNDLES`` to **True**, which is easier to convert
    one CSS file
  * enter ``nikola build`` to build all the ``output`` files
* As the tool only support one source file,
  * find the any pages of the site that use the most CSS style and update the
    ``src`` file value in ``gulpfile.js``
  * also make sure the ``base`` folder is correct, which is ``output`` folder
* Once the values in ``gulpfile.js`` are correct based on your need, enter this
  command in the console / terminal, ``gulp critical``.
* Once the ``dest`` file is generated,
  * copy the inline CSS code to ``EXTRA_HEAD_DATA``
  * set ``carpet__late_load_css`` to **True**
  * enter ``nikola build`` to rebuild all the ``output`` files again

## Cookie message

It is to display information about cookies to the users.

* ``carpet__cookie_message`` - cookie message notification
* ``carpet__cookie_path`` - (optional) for changing cookie path, by default it is across the entire domain
* ``carpet__cookie_expiry`` - (optional) for extending cookie lifetime, by default it is 30 days

## More contents

* ``carpet__head_prefix`` - extra custom content right after opening ``<head>``
* ``carpet__body_prefix`` - extra custom content right after opening ``<body>``
* ``carpet__content_prefix`` - extra custom content right before ``<main>`` content
* ``carpet__content_suffix`` - extra custom content right after ``<main>`` content

## Known Issues

* Not all features of Nikola are tested
* Value of ``THEME_COLOR`` is not used

## Todo list

* Optimise images with image compression 

## Dependencies

* [Nikola](https://getnikola.com/)
* [Mako](http://www.makotemplates.org/) 
* [Bulma](http://bulma.io/)
* [Font Awesome](http://fontawesome.io/)
* [Cookie message](https://github.com/studio24/cookie-message)

## License

Carpet - [MIT License](https://github.com/ivanteoh/nikola-carpet-mako/blob/master/LICENSE)

Nikola - [MIT License](https://getnikola.com/license.html)

Mako - [MIT License](http://www.opensource.org/licenses/mit-license.php)

Bulma [MIT License](https://github.com/jgthms/bulma/blob/master/LICENSE)

Font Awesome [Full details](http://fontawesome.io/license/)

Cookie message [MIT License](https://github.com/studio24/cookie-message/blob/master/LICENSE.md)
