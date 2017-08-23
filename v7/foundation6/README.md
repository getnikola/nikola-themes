# foundation6

This is a theme for the static site generator [Nikola](https://getnikola.com) using the [Foundation](http://foundation.zurb.com) framework.

It aims to be simple, elegant and not bloat the overall size of your site too much.

## Installation

You can install it directly with Nikola:

    nikola install_theme foundation6

## Usage

In your conf.py set `THEME` to `foundation6`.

Rebuild your site.

## Included in custom Foundation 6

This theme uses a custom Foundation 6 with fewer components to slim the size of the site even more.

Components used are:

* Grid, 12 Columns
* General
  * Typography
  * Visibility Classes
* Navigation
  * Menu
  * Accordion Menu
  * Top Bar
  * Pagination
* Containers
  * Callout
  * Table
* Media
  * Label

If you want to replace this with your own custom Foundation 6 - i.e. with different colors - just replace the foundation.min.css in the assets.

## Licenses

The Foundation framework is licensed under MIT.

This theme is licensed under APGLv3.

