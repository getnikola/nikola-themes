# material-theme-nikola
A theme for nikola based on Bootstrap 3, which lets you use the new [Google Material Design](http://www.google.com/design/spec/material-design/).

Based on [bootstrap-material-design](https://github.com/FezVrasta/bootstrap-material-design).

## Customization

### Navbar color schema 

    GLOBAL_CONTEXT = {                                                               
         'header_color': 'default'                                                    
    }

Options available:

* `default` or `primary`
* `success`
* `info`
* `warning`
* `danger`

![headers examples](https://themes.getnikola.com/resources/material-theme-navbars.png)


### Social links in floating action button

    GLOBAL_CONTEXT = {
        "social_links": [
        {
            'bgcolor': "#F44336",
            'icon': "<i class='fa fa-share-square-o'></i>"
        },
        {
            "url": "https://twitter.com/",
            "bgcolor": "#55ACEE",
            "color": "#fffff",
            "icon": "<i class='fa fa-twitter'></i>",
            "target": "_blank"
        },
        {
            "url": "https://github.com/",
            "bgcolor": "#666666",
            "color": "#fffff",
            "icon": "<i class='fa fa-github-square'></i>",
            "target": "_blank"
        },
        {
            "url": "https://www.facebook.com",
            "bgcolor": "#3B5998",
            "color": "#fffff",
            "icon": "<i class='fa fa-facebook'></i>",
            "target": "_blank"
        },
        ]
    }
    
![actions-links-gif](https://themes.getnikola.com/resources/material-theme-actions-links.gif)


### Set author's avatar in header post

    GLOBAL_CONTEXT = {
        'author_avatar': '/images/avatar.jpg',
    }
    
![author's avatar](https://themes.getnikola.com/resources/material-theme-avatar-author.png)


### Show author's biography into the dialog of credits (or footer)

For convenience, first define a variable with the html biography.

    BIOGRAPHY = """
    <img class="img-circle" style="float:left;margin:10px 20px 10px 0px;max-height:200px;" src="/images/avatar.jpg">
    <p>Nikola Tesla (Serbian Cyrillic: Никола Тесла; 10 July 1856 – 7 January 1943) was a Serbian American inventor, electrical engineer, mechanical engineer, physicist, and futurist best known for his contributions to the design of the modern alternating current (AC) electricity supply system.
    </p>
    """
    
Then, add it to `biography` viariable into `GLOBAL_CONTEXT`

    GLOBAL_CONTEXT = {
        "biography": BIOGRAPHY,
    }

![biography](https://themes.getnikola.com/resources/material-theme-biography.png)

### Add Google Analytics script

Define a variable with javascript block:
 
    ANALYTICS = """
    < script>
        (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
        (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
        m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
        })(window,document,'script','//www.google-analytics.com/analytics.js','ga');
        ga('create', 'XX-XXXXXXXXX-X', 'auto');
        ga('send', 'pageview');
    < /script> 
    """

And add it to analytics variable into `GLOBAL_CONTEXT`:

    GLOBAL_CONTEXT = {
        "analytics": ANALYTICS,
    }


### Enable use of pace.js

For enable use of [PACE](http://github.hubspot.com/pace/docs/welcome/), add a variable into GLOBAL_CONTEXT:

    GLOBAL_CONTEXT = {
        'use_pace': True,
    }

