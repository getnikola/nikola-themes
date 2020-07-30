# The GruberWine Theme

## Description

This theme is based on Zen-jinja, at least visually. But it takes most of its cues from two well-known blogs: John Gruber's [Daring Fireball](https://daringfireball.net), and Dave Winer's [Scripting News](http://scripting.com). Hence the name.

## What That Means

There are two key specialisms that come from those sites. First, Daring Fireball-style link posts are supported. If your post includes a URL in the `link` metadata, then your post's title will link to that URL, instead of being the permalink for the post. The post's timestamp will be its permalink.

Second, Winer's titleless microblog posts are supported. If any of the following conditions are true, the title will not be displayed:

- the `type` metadata is set to `micro`
- the `title` metadata is blank
- the `title` metadata is set to "NO TITLE" (as is the case for posts imported from WordPress without titles).

What happens if both of those interact? To be quite honest, I haven't tried that! I expect it to behave as a microblog post; in other words, Wine(r) will win over Gruber.

## Extra Functionality

There is also a new template,

If you want to see it in action, visit my own site, <https://devilgate.org/>
