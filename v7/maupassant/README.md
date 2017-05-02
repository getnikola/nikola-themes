Nikola theme forked from <https://github.com/pagecho/maupassant>

Description from the original:

> A simple typecho template with great performance on different devices.

Suggested configuration is to add Home to nav links so you see the
"tabs" properly:

```python
NAVIGATION_LINKS = {
    DEFAULT_LANG: (
        ("/", "Home"),
        ("/archive.html", "Archive"),
        ("/categories/", "Tags"),
    ),
}
```



TODO:

* Could add support for fontawesome icons in nav bar like some forks of
  this theme have.
* Image gallery is somewhat broken
