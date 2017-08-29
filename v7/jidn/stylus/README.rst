STDIO Compilation Example
=======================================

``stylus`` reads from stdin and outputs to stdout, so for example::

  $ stylus --compress < some.styl > some.css

Try Stylus some in the terminal! Type below and press CTRL-D for __EOF__::

  $ stylus
  body
    color red
    font 14px Arial, sans-serif

Compiling Files Example
=======================================

``stylus`` also accepts files and directories. For example, a directory named css will compile and output .css files in the same directory.::

  $ stylus css

The following will output to ./public/stylesheets::

  $ stylus css --out public/stylesheets

Or a few files::

  $ stylus one.styl two.styl

For development purposes, you can use the linenos option to emit comments indicating the Stylus filename and line number in the generated CSS::

  $ stylus --line-numbers <path>

Converting CSS
=======================================

If you wish to convert CSS to the terse Stylus syntax, use the ``--css`` flag.

Via stdio::

  $ stylus --css < test.css > test.styl

Output a .styl file of the same basename::

  $ stylus --css test.css

Output to a specific destination::

  $ stylus --css test.css /tmp/out.styl

CSS Property Help
=======================================

On OS X, stylus help <prop> will open your default browser and display help documentation for the given <prop>.::

    $ stylus help box-shadow

Interactive Shell
=======================================

The Stylus REPL (Read-Eval-Print-Loop) or “interactive shell” allows you to play around with Stylus expressions directly from your terminal.

Note that this works only for expressions—not selectors, etc. To use simple add the -i, or --interactive flag::

    $ stylus -i
    > color = white
    => #fff
    > color - rgb(200,50,0)
    => #37cdff
    > color
    => #fff
    > color -= rgb(200,50,0)
    => #37cdff
    > color
    => #37cdff
    > rgba(color, 0.5)
    => rgba(55,205,255,0.5)

