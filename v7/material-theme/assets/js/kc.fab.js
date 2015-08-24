/*===================================================================
=            KC.FAB : Materialize Floating Action Button            =
===================================================================*/
/*
 * Copyright 2015 Mark Luk
 * Released under the MIT license
 * https://github.com/katrincwl/kc_fab/blob/master/LICENSE
 *
 * @author: Mark Luk
 * @version: 1.0
 * @date: 18/3/2015
 */

(function($){
    if(!$.kc){
        $.kc = new Object();
    };
    
    $.kc.fab = function(el, links, options){
        // To avoid scope issues, use 'base' instead of 'this'
        // to reference this class from internal events and functions.
        var base = this;
        
        // Access to jQuery and DOM versions of element
        base.$el = $(el);
        base.el = el;
        
        // Add a reverse reference to the DOM object
        base.$el.data("kc.fab", base);
        
        var main_fab_btn;
        var sub_fab_btns;

        base.init = function(){
            if( typeof( links ) === "undefined" || links === null ) {
                links = [
                    {
                        "url":null,
                        "bgcolor":"red",
                        "icon":"+"
                    },
                    {
                        "url":"http://www.example.com",
                        "bgcolor":"orange",
                        "icon":"+"
                    },
                    {
                        "url":"http://www.example.com",
                        "bgcolor":"yellow",
                        "icon":"+"
                    }
                ];
            }


            base.links = links;
            if (base.links.length > 0){
                main_btn = base.links[0];
                color_style = (main_btn.color)? "color:"+main_btn.color+";" : "";
                bg_color_style = (main_btn.bgcolor)? "background-color:"+main_btn.bgcolor+";" : "";
                main_btn_dom = "<button data-link-href='"+((main_btn.url)?main_btn.url:"")+"' data-link-target='"+((main_btn.target)?main_btn.target:"")+"' class='btn btn-fab btn-raised btn-material-red kc_fab_main_btn' style='"+bg_color_style+"'><span style='"+color_style+"'>"+main_btn.icon+"</span></button>";
                

                sub_fab_btns_dom = "";
                base.links.shift();
                /* Loop through the remaining links array */
                for (var i = 0; i < base.links.length; i++) {
                    color_style = (base.links[i].color)? "color:"+base.links[i].color+";" : "";
                    bg_color_style = (base.links[i].bgcolor)? "background-color:"+base.links[i].bgcolor+";" : "";

                    sub_fab_btns_dom += "<div><button data-link-href='"+(base.links[i].url?base.links[i].url:"")+"' data-link-target='"+((base.links[i].target)?base.links[i].target:"")+"' class='sub_fab_btn' style='"+bg_color_style+"'><span style='"+color_style+"'>"+base.links[i].icon+"</span></button></div>";
                    
                };
                sub_fab_btns_dom = "<div class='sub_fab_btns_wrapper'>"+sub_fab_btns_dom+"</div>";
                base.$el.append(sub_fab_btns_dom).append(main_btn_dom);

            }else{
                if (typeof console == "undefined") {
                    window.console = {
                        log: function (msg) {
                            alert(msg);
                        }
                    };
                }
                console.log("Invalid links array param");
            }
            
            base.options = $.extend({},$.kc.fab.defaultOptions, options);


            main_fab_btn = base.$el.find(".kc_fab_main_btn");
            sub_fab_btns = base.$el.find(".sub_fab_btns_wrapper");

            main_fab_btn.click(function(e){
                if ($(this).attr('data-link-href').length > 0){
                    if ($(this).attr('data-link-target')){
                        window.open($(this).attr('data-link-href'), $(this).attr('data-link-target'));
                    }else{
                        window.location.href = $(this).attr('data-link-href');
                    }
                }
            	sub_fab_btns.toggleClass('show');

            	if ($(".kc_fab_overlay").length > 0){
            		$(".kc_fab_overlay").remove();
                    main_fab_btn.blur();
            	}else{
            		$('body').append('<div class="kc_fab_overlay" ></div>');	
            	}
            	
            	

                if($(this).find(".ink").length === 0){
                    $(this).prepend("<span class='ink'></span>");
                }else{
                    $(this).find(".ink").remove();
                    $(this).prepend("<span class='ink'></span>");
                }
                     
                ink = $(this).find(".ink");
                 
                if(!ink.height() && !ink.width()){
                    d = Math.max($(this).outerWidth(), $(this).outerHeight());
                    ink.css({height: d, width: d});
                }
                 
                x = e.pageX - $(this).offset().left - ink.width()/2;
                y = e.pageY - $(this).offset().top - ink.height()/2;
                 
                ink.css({top: y+'px', left: x+'px'}).addClass("animate");

            });

            sub_fab_btns.find('.sub_fab_btn').on('mousedown', function(e){
                if ($(this).attr('data-link-href').length > 0){
                    if ($(this).attr('data-link-target')){
                        window.open($(this).attr('data-link-href'), $(this).attr('data-link-target'));
                    }else{
                        window.location.href = $(this).attr('data-link-href');
                    }
                }

            });

            main_fab_btn.focusout(function(){
                sub_fab_btns.removeClass('show');
                overlay = $(".kc_fab_overlay");
                overlay.remove();
                
            });
            
            // Put your initialization code here
        };
        
        // Sample Function, Uncomment to use
        // base.functionName = function(paramaters){
        // 
        // };


        
        // Run initializer
        base.init();
    };
    
    $.kc.fab.defaultOptions = {};
    
    $.fn.kc_fab = function(links, options){
        return this.each(function(){
            (new $.kc.fab(this, links, options));
        });
    };
    
})(jQuery);


