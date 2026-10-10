This is a theme based on Bulma 1.0, a modern CSS framework based on Flexbox.

Bulma is a CSS-only framework (no JavaScript), which means this theme is lighter than Bootstrap-based themes.

## Features

- Clean, modern design
- Responsive navbar with mobile burger menu, usable from the keyboard
- No JavaScript on ordinary pages: the burger menu is CSS-only, and the
  lightbox and gallery scripts load only on pages that use them
- No inline scripts or styles, so it works under a Content-Security-Policy
  without `'unsafe-inline'` (except with `DATE_FANCINESS`, whose setup is
  still an inline script)
- reStructuredText and Jupyter CSS load only on pages that need them
- Bulma 1.0.4 via CDN

## Configuration

You can customize the navbar appearance in your `conf.py`:

```python
THEME_CONFIG = {
    DEFAULT_LANG: {
        'navbar_light': False,  # Set to True for light navbar
        'navbar_custom_bg': '',  # Custom background class, e.g., 'has-background-info'
    }
}
```

## Note

This theme uses Bulma's native classes:
- `.is-active` for active states
- `.is-sr-only` for screen-reader-only content
- `.navbar-burger` for mobile menu toggle (as the label of a hidden checkbox)
- Bulma's `.section`, `.container`, `.columns`, `.column` for layout
