This theme (particularly the side-menu) is based on an 
[example layout](http://purecss.io/layouts/side-menu/) from PureCSS. 
It features a sidemenu that collapses into a hamburger on small screens
and a single column for posts. 

Posts may include a header image on which the title is overlaid. The
image will be darkened and blurred to provide contrast to the title. The 
photo is set by including a header-image directive to the top of the post.
For example:

```
.. title: Welcome to Nikola
.. slug: welcome-to-nikola
.. date: 2015-03-30 23:00:00 UTC-03:00
.. tags: nikola, blog
.. category: personal
.. header-image: https://farm1.staticflickr.com/138/352972944_4f9d568680.jpg
```

You may set a default header image for posts by setting 
``default_header_image`` in the GLOBAL_CONTEXT. An image to use on the main 
blog page (pages that use the blog title) can be set by setting
``blog_header_image`` key. For example:

```
GLOBAL_CONTEXT = {
    'default_header_image': 'https://farm1.staticflickr.com/138/352972944_4f9d568680.jpg',
    'blog_header_image': 'https://farm1.staticflickr.com/138/352972944_4f9d568680.jpg'
}
```

You may exclude post content from indexes by setting 'exclude_index_content'
in the GLOBAL_CONTEXT variable. Such as:

```
GLOBAL_CONTEXT = {
    'exclude_index_content': True
}
```

Figures, code blocks, and slides within a post are allowed to expand to the 
full width of the content area while the text of the post expands to a 
maximum 800px. The margin on the sides of the text adjusts based on screen
size.

Post dates are displayed in plain language relative to the current time. This
uses moment.js, but the DATE_FANCINESS variable is not used and the 
behaviour cannot be disabled.

External libraries used in this theme include:

* Figures within posts have a simple lightbox affect implemented by 
  [Fluidbox](http://terrymun.github.io/Fluidbox/).
* [Font Awesome](https://fortawesome.github.io/Font-Awesome/) is included for
  their great icons.
* [highlight.js](https://highlightjs.org/) provides syntax highlighting for 
  code blocks.
* [jQuery](https://jquery.com/) is used for whatever and as a dependency for 
  Fluidbox.
* [moment.js](http://momentjs.com/) displays dates as plain language relative 
  to the current time. 
* [PureCSS](http://purecss.io) for a responsive grid system.

This theme does not use any functionaly from the base Nikola theme. The templates 
are commented extensively to allow this theme to be used as an example for other 
custom themes. The recommended way to do this is to copy the theme under a new 
name and edit to suit. 