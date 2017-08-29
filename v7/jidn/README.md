# JIDN: a Nikola Theme

When I ran across Hynek Schlawack's [blog](https://hynek.me/articles), I liked the simplistic beauty.
When I took a look at the source, I fell in love.
Here is my homage to beauty, to which I can only inspire.

You can view the demo, where you can change between the different colors, at http://jidn.com/blog/jidn-a-nikola-theme/ and the code at [GitHub](https://github.com/jidn/nikola-jidn).

## Theme Highlights

* Color Themes
* Post Sharing
    + Twitter
    + Facebook
    + Google+
* Author Information
    + image
    + email
    + short biography
    + location information
* Author social accounts
    + Twitter
    + Facebook
    + Github
    + StackOverflow
    + Instagram
    + Pinterest
    + and more
* Easy CSS Override

## Preview

This theme is based on the [lanyon theme](https://themes.getnikola.com/v7/lanyon/).
All the interesting things in this theme happen at the post bottom.  Here is a quick look at the end of a post.  You can see post sharing with Twitter, Facebook, and Google+. The author section contains a name, photo, and other configurable items.
![nikola-jidn](https://user-images.githubusercontent.com/3378145/29786394-9f1c2d3e-8bf0-11e7-8cc1-e3ec20f64df8.png)

## Post Sharing

What you write is worth reading.
But getting the word out about your post can be hard.
This theme tries to make it easier for your readers to share your posts on Twitter, Facebook, and Google+.
Sharing icons are seen at the end of a post.

## Author Information

Author information is shown at the end of a post as long as the author name associated with the post has a corresponding entry in the configuration.
While Nikola is commonly used with a single author, I figured we should allow for multiple.

First, create a dictionary in the `GLOBAL_CONTEXT` of your `conf.py` with "JIDN" as the key.
Inside this dictionary, add additional dictionaries, one for each author.
Each of these dictionaries is added to "JIDN" with the author's name as the key.
For additional authors, be sure to use the name as it appears in the post author [metadata](https://getnikola.com/handbook.html#extra).
So if the author section doesn't appear in your blog post, closely check that the author's name in `conf.py` to that in the post.

Each dictionary for an author can have the following fields.
All of which are optional except for `image`:

image
:   **[Required field]**
    A URL to a 120x120 image of yourself or avatar.
    If you want a different size, you can change to dimensions in the CSS (
    look for `.author-image`).

email
:   This could be BLOG_EMAIL or an alternate authors email address

bio
:   A short biography of your self.

map
:   A string providing your general or specific location.

social
:   A sequence of your public social accounts you want others to see.
    From the URL I try to match to something in [FontAwsome](http://fontawesome.io/icons/#brand)


Example:

```python
GLOBAL_CONTEXT = {
    "JIDN": {BLOG_AUTHOR: {   # Or "Given Surname" for alternate authors
            "image": "http://example.com/my-image.jpg",

            ## The following are all individually optional
            "email": BLOG_EMAIL,  # or something else for alternate authors
            "bio": """I am the very model of a modern, major general.""",
            "map": "Kahlotus, WA  USA",
            "social": (
                "https://twitter.com/username",
                "https://facebook.com/username",
                "https://github.com/username",
                # You get the idea
                )
            }
            # Add any needed alternate authors
            }
    ...
}
```

## Color Themes

The lanyon theme was one of my inspirations.
Thus, the JIDN theme supports all the same colored themes.
However, instead of using a hex code to reference them, I use the color name to identify the theme.
Available colors include red, orange, yellow, green, cyan, blue, magenta, and brown.

To the `GLOBAL_CONTEXT` in "conf.py", add the key `"JIDN-theme"` and the value of `"theme-base-*color*"`, replacing *color* with one of the available colors.

Example:

```python
GLOBAL_CONTEXT = {
    "JIDN-theme": "theme-base-blue",
    ...
    "JIDN": ...
}
```

So you don't like any of these color choices and you just have to have electric lime, `#ccff00`, as your color?
Set `"JIDN-theme"` to `"theme-custom"`

```python
    GLOBAL_CONTEXT = {
        "JIDN-theme": "theme-custom",
        ...
        "JIDN": ...
    }
```

Copy the following CSS to `assets/css/custom.css` and you are ready to hurt your eyes.

```css
.theme-custom .sidebar,
.theme-custom .sidebar-toggle:active,
.theme-custom #sidebar-checkbox:focus ~ .sidebar-toggle,
.theme-custom #sidebar-checkbox:checked ~ .sidebar-toggle {
    background-color: #ccff00;
}
.theme-custom .container a,
.theme-custom .sidebar-toggle,
.theme-custom .related-posts li a:hover {
    color: #ccff00;
}
.theme-custom .sidebar-toggle:before {
    background-image: -webkit-linear-gradient(to bottom, #ccff00, #ccff00 20%, #fff 20%, #fff 40%, #ccff00 40%, #ccff00 60%, #fff 60%, #fff 80%, #ccff00 80%, #ccff00 100%);
    background-image:    -moz-linear-gradient(to bottom, #ccff00, #ccff00 20%, #fff 20%, #fff 40%, #ccff00 40%, #ccff00 60%, #fff 60%, #fff 80%, #ccff00 80%, #ccff00 100%);
    background-image:     -ms-linear-gradient(to bottom, #ccff00, #ccff00 20%, #fff 20%, #fff 40%, #ccff00 40%, #ccff00 60%, #fff 60%, #fff 80%, #ccff00 80%, #ccff00 100%);
    background-image:         linear-gradient(to bottom, #ccff00, #ccff00 20%, #fff 20%, #fff 40%, #ccff00 40%, #ccff00 60%, #fff 60%, #fff 80%, #ccff00 80%, #ccff00 100%);
}
.theme-custom .sidebar-toggle:active:before,
.theme-custom #sidebar-checkbox:focus ~ .sidebar-toggle:before,
.theme-custom #sidebar-checkbox:checked ~ .sidebar-toggle:before {
    background-image: -webkit-linear-gradient(to bottom, #fff, #fff 20%, #ccff00 20%, #ccff00 40%, #fff 40%, #fff 60%, #ccff00 60%, #ccff00 80%, #fff 80%, #fff 100%);
    background-image:    -moz-linear-gradient(to bottom, #fff, #fff 20%, #ccff00 20%, #ccff00 40%, #fff 40%, #fff 60%, #ccff00 60%, #ccff00 80%, #fff 80%, #fff 100%);
    background-image:     -ms-linear-gradient(to bottom, #fff, #fff 20%, #ccff00 20%, #ccff00 40%, #fff 40%, #fff 60%, #ccff00 60%, #ccff00 80%, #fff 80%, #fff 100%);
    background-image:         linear-gradient(to bottom, #fff, #fff 20%, #ccff00 20%, #ccff00 40%, #fff 40%, #fff 60%, #ccff00 60%, #ccff00 80%, #fff 80%, #fff 100%);
}
```

Just replace `#ccffoo` with the color of your choice.

## Easy CSS Override

Place all of your CSS changes into `custom.css` and the theme will load it as your last word on styling.
