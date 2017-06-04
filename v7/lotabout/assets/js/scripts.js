jQuery(function($) {
    /* ============================================================ */
    /* Header Nav */
    /* ============================================================ */
    function headerNav() {
        var header = $('.header'),
            curPos = $(document).scrollTop(),
            prevPos = curPos;

        function refreshNav() {
            curPos = $(document).scrollTop();
            if (curPos > 10) {
                if (header.hasClass('transparent')) {
                    header.removeClass('transparent');
                }
            }
            if (curPos < 10) {
                header.addClass('transparent');
                if (header.hasClass('dynamic')) {
                    header.removeClass('dynamic');
                }
                prevPos = curPos;
            }
            else if (curPos - prevPos > 50) {
                if (!header.hasClass('dynamic')) {
                    header.addClass('dynamic');
                }
                prevPos = curPos;
            } else if (curPos - prevPos < -50) {
                if (header.hasClass('dynamic')) {
                    header.removeClass('dynamic');
                }
                prevPos = curPos;
            }
        }

        refreshNav();

        $(window).scroll(refreshNav);
    }


    /* Load theme */
    function loadTheme(html) {
      var tag, theme, href,
          $css_theme = $('#css_theme');
      if (html) {
         tag = $('#tag-theme', html);
      } else {
         tag = $('#tag-theme');
      }


      if (tag.length == 1) {
        theme  = tag.attr('data-theme');
        href = '/assets/css/theme.'+theme+'.css';
      } else {
        href = '/assets/css/theme.gray.css';
      }
      if ($css_theme.attr('href') !== href ) {
          $css_theme.attr('href', href);
      }
    }

    $(document).ready(function() {
        //$(".body").fitVids();
        headerNav();
        loadTheme();
        // $('#history-back').on('click',function(e){
        //     e.preventDefault();
        //     window.History.back();
        //     return false;
        // });
        $('.scroll.top').on('click', function(e) {
            e.preventDefault();
            $('html, body').animate({
                scrollTop: 0,
            }, {
                duration: 500
            });
            return false;
        });

    });

});
