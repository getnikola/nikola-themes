#####################
nikola-skeleton-theme
#####################

``skeleton`` is a responsive, minimal theme for the `Nikola`_ static site
generator based on the `Skeleton`_ web framework.

The theme is incredibly lightweight, coming in at ~220KB, including fonts.

Most (all?) Nikola features are supported.

A navbar, with dropdown submenus is included out of the box. On small devices,
the navmenu will be replaced by a dropbox containing the same options.

.. _Nikola: https://getnikola.com/

.. _Skeleton: http://getskeleton.com/

**********************
Issues / Contributions
**********************

nikola-skeleton-theme lives in two places:

-   `gwax/nikola-skeleton-theme <https://github.com/gwax/nikola-skeleton-theme>`_
    (authoritative) official maintained home of the theme
-   `getnikola/nikola-themes <https://github.com/getnikola/nikola-themes>`_
    (mirror) copy managed via ``git subtree`` to ease use by others.

PRs, Issues, questions, and comments should be directed to
`gwax/nikola-skeleton-theme`_ and changes should then be subtree merged into
`getnikola/nikola-themes`_

Pulling changes
===============

.. code:: bash

    git remote add skeleton git@github.com:gwax/nikola-skeleton-theme.git
    git subtree pull --prefix=v8/skeleton skeleton master
