A modern, highly accessible theme for Nikola, built on `bootstrap4`. It takes standard accessibility principles and **actually** implements them, not just claims them, which unfortunately seems to be the norm out there. On top of that, you also get cleaner HTML structure and a few conveniences most themes leave out.

Built by someone with a bit of firsthand experience on both sides of accessibility: living with the challenges, and building the tech that solves them. Said guy also likes clean code and optimization, and while he's fond of learning new things, he's not a fan of learning a pile of unrelated subtasks just to reach the one task he actually wanted to do.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Aarush%20Bhat-0A66C2?logo=linkedin&logoColor=white)](https://linkedin.com/in/aarushdev)
[![License: MIT](https://img.shields.io/github/license/Aarushb/lazykola-a11y)](https://github.com/Aarushb/lazykola-a11y/blob/main/LICENSE)

Full documentation, the design presets writeup, and the serverless comment system live in the [main repo](https://github.com/Aarushb/lazykola-a11y). Here's the TL;DR essentials to get you started.

## Accessibility

- **Proper current-page indicators**: `aria-current="page"` on nav links, instead of Bootstrap's hardcoded "active" class.
    > But but hardcoding the "current" for the page you're on works!: Sure, but there is a much more global, consistent, reliable and industry-standard way to do this; so no. Optimization, remember?
- **Corrected heading hierarchy**: the site name in the navbar is the real `<h1>`, post titles render as `<h2>`, and a small script auto-normalizes each post's own headings so the shallowest one always starts at `<h3>`, no matter whether you started writing at `#` or `###`.
    > **Yo wait wait, but why though?:** blind users, at the very least, regularly rely on structural navigation, like nested headings, to find their way around a page, and I'd imagine it helps low-vision users relying on things like high contrast too. But true inclusivity only works if it's for everyone, not just one group at the expense of another: making a site usable only for the sighted is inaccessible, and making it usable only for the blind is just as segregating in the other direction; accessible sure, but inclusive? Not so much. Keeping track of heading levels in your head, knowing where to start and handling every edge case, is cognitive overhead. So instead of asking you to think about that, this script does it for you.

- **Smart logo alt text**: before, a screen reader read `"My Website!"` no matter what. Now, once you set `LOGO_ALT_TEXT`, it reads whatever you actually wrote, and the redundant site-title text stops rendering separately so it isn't read twice.

```python
THEME_CONFIG = {
    DEFAULT_LANG: {
        "LOGO_URL": "/assets/images/logo.png",
        "LOGO_ALT_TEXT": "Me bent over a terminal with a lukewarm coffee that's been sitting there for six hours",
    }
}
```


- **WCAG AA contrast everywhere**: every color pairing in the theme, including the comment widget, has been run through an automated scanner and fixed to meet 4.5:1. Links inside body text are underlined by default, never distinguished by color alone.


## Design Presets

> **Huh?:** not everyone has the ability to visually perceive the website they're building. These presets exist to lower that barrier.

A `PRESET` key in `THEME_CONFIG` swaps the accent color, corner rounding, spacing, heading typeface, and card style as one coordinated set. Five presets ship with the theme (`portfolio`, `business`, `blog`, `docs`, `community`), each pre-checked for WCAG AA contrast in both light and dark mode, and each described in plain language in the main repo using words to help you pick one by picturing the kind of site you're building in your mind's eye.

```python
THEME_CONFIG = {
    DEFAULT_LANG: {
        "PRESET": "blog",  # or "portfolio", "business", "docs", "community"
    }
}
```


## Navbar

Not an accessibility fix (whaaaat?!), just a visual knob: switch to a light navbar, or drop in your own Bootstrap background class.

```python
THEME_CONFIG = {
    DEFAULT_LANG: {
        "navbar_light": False,  # light navbar with dark text, defaults to dark
        "navbar_custom_bg": "bg-dark",  # any Bootstrap bg-* class
    }
}
```

## Dark Mode

The whole theme, comment widget included, follows the visitor's OS/browser dark-mode preference automatically. No toggle, nothing to configure. Code blocks intentionally keep their light syntax-highlighting theme so copied code always looks the same regardless of the reader's setting; if you'd rather match dark mode, set a dark-friendly [Pygments style](https://pygments.org/styles/):

```python
PYGMENTS_STYLE = "monokai"
```

## Automatic, No Config Needed

A few more things this theme does on its own:

- **No redundant heading self-links**: post and page titles don't link back to themselves when you're already on that page, since a screen reader saying "link, same page" serves no one.
- **Local timezone stamps**: appends the visitor's own local time next to each post's build date.
- **Cleaner blog section titles**: the browser tab for the `/blog` section reads "Blog | Site Title" instead of the generic site title.
- **Copy-to-clipboard code blocks**: a keyboard-focusable button on every code block, whose label changes to "Copied!" to confirm the action for sighted and screen-reader users alike.

## Comments (Optional, Not Bundled)

> **This a static website generator bruh, get that crap outta here.:** this is honestly the biggest thing that sparked the motivation to build a whole new theme, and then, as these things usually go, it ballooned from there. Accessibility technologies typically cooperate better with text than with fancy UIs you have to learn the layout of and adapt to all the quirks of, so I didn't want to deal with the cognitive overhead of something like WordPress or Wix just to get this. But I still wanted people to be able to tell me how much my website sucks, without having to host my own server just for a static site to make that happen.

The theme ships with an out-of-the-box serverless comment system built on Cloudflare Workers and D1, deployable in a few minutes with zero server to maintain. It isn't included in this repo since it's a separate project with its own dependencies and deploy tooling, not theme code. Full setup instructions are in the [main repo](https://github.com/Aarushb/lazykola-a11y#serverless-comments-setup). Once deployed, point the theme at it:

```python
THEME_CONFIG = {
    DEFAULT_LANG: {
        "comment_turnstile_site_key": "your-turnstile-site-key",  # optional spam check
    }
}

COMMENT_SYSTEM = "lazykola"
COMMENT_SYSTEM_ID = "https://your-comments-worker.yourname.workers.dev"
```

## Using This Theme? Show It Off

If you've built a site with this theme, I'd genuinely like to see it. Part of what motivates me to get up in the morning is being able to make the lives of other people just a little bit better, so if this has helped you, please share, it would make my day to hear. Plus, potential users will hear it from people other than myself if the theme is any good!

Open a PR adding a link to your site (and, if you want, what preset you used) to the list below, in the main repo's README. Should this humble repo with single-digit stars be able to get you a little bit of traction, then I'm happy to serve that purpose as well.

### Sites Using This Theme

- [aarushb.github.io](https://aarushb.github.io): portfolio preset

## Conclusion

That "sucks" remark from earlier applies to everything, by the way. If you find something horribly broken with this theme, think a feature is bad, or have other suggestions for new features, feel free to open an issue on [the main repo](https://github.com/Aarushb/lazykola-a11y/issues).

[![GitHub issues](https://img.shields.io/github/issues/Aarushb/lazykola-a11y)](https://github.com/Aarushb/lazykola-a11y/issues)

---

Enjoy, and I hope you find this as helpful as I did; preferably more.

Stay safe, stay inclusive. ❤️