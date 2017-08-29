This repo contains the publicly available themes for Nikola (<https://getnikola.com/>)

To contribute a theme:

* Make sure it works well for you
* Start a branch that puts your theme "foo" in vX/foo (we prefer committing full code as opposed to using submodules — it’s easier to maintain)
* Run ``scripts/test_themes.py foo`` and see if it complains of anything
* Make sure you have a ``README.md`` (written in Markdown), a ``.theme`` meta
  file, and ``parent``/``engine`` files in your theme
* Double check licenses for everyhing in your theme
* Make a Pull Request

After a brief discussion it will be merged and available for everyone :-)

See also: [Creating a Theme](https://getnikola.com/creating-a-theme.html),
[Theming reference](https://getnikola.com/theming.html), [Template
variables](https://getnikola.com/template-variables.html).
