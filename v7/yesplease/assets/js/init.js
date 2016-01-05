$(function(){
    $('a.image-reference').fluidbox();

    $('pre.code').each(function(i, block) {
      hljs.highlightBlock(block);
    });

    // Required because the pre.code is automatically generated from ReST post.
    // Making a custom code ReST directive would allow generating this desired container around the pre.code element.
    $('pre.code').wrap('<div class="yp-code-container yp-well"></div>');
});