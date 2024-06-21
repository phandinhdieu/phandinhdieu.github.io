jQuery(function() {

	var $ = jQuery;

  $('body').addClass('postload');

  $(document).ready(function() {

  	// Add fullwidth class to gallery thumbs if less than 6

  	$('.imageGallery').each(function(){
  	  if ($(this).children('div').length <= 6) {
  	    $(this).children('div').addClass('fullwidth-mobile');
  	  }
  	});

  	// Add swipe to fancybox mobile

    var swipeGallery = function(){
      setTimeout(function(){
      var touchGallery = document.getElementsByClassName("fancybox-wrap")[0];
      var mc = new Hammer(touchGallery);
      mc.on("panleft panright", function(ev) {
        if (ev.type == "panleft") {
          $("a.fancybox-next").trigger("click");
        }
        else if (ev.type == "panright") {
          $("a.fancybox-prev").trigger("click");
        }
        swipeGallery();
      });
      }, 500);
    }

    if ('ontouchstart' in window) {
      $("body").on( "click", "a.w-fancybox", function() {
        swipeGallery();
      });
  	}

    // Watch for changes on nav
    var interval = function(interval, duration){
      var counter = 0;
      var looper = setInterval(function(){
        if (counter >= duration) {
          clearInterval(looper);
        } else {
          navmove();
          cartstyle();
          counter += interval;
        }
      }, interval);
    }

    // Watch for post-load nav elements
    var navmove = function(){
      $(".w-navlist a").each(function(){
        var navlinkid = $(this).attr("id");
        if (navlinkid) {
          var navLinkParent = $(this).parent().clone(true);
          if (!$("#navcontainer #"+navlinkid).length) {
            $("#navcontainer .wsite-menu-default").append(navLinkParent);
            var newheight = $("#navcontainer .wsite-menu-default").height();
            $(".wsite-mobile-menu").height(newheight);
          }
        }
      });
      if (!$("#header-wrap #wsite-menus").length) {
        var submenus = $("#wsite-menus").detach();
        $("#header-wrap").append(submenus);
      }
    }
    // Check for search

    if ($("#header-wrap .wsite-search").length) {
      var search = $("#header-wrap .wsite-search").clone(true);
      $("#search").append(search);
    }

    // Style mini cart
    var cartstyle = function() {
      if ( !$("#site-wrap > #wsite-mini-cart").length && $("#wsite-mini-cart").length) {
        var minicart = $('#wsite-mini-cart').detach();
        $("#site-wrap").append(minicart);
        $('#wsite-mini-cart').addClass('overlay');
        $('.wsite-nav-cart').append('<div class="cart-notice">Cart Updated</div>');
        $('#wsite-mini-cart').on('DOMSubtreeModified propertychange', function() {
        	$('#wsite-nav-cart-a').unbind('mouseenter mouseleave');
        });
      	$('#wsite-nav-cart-a').unbind('mouseenter mouseleave');
      }
      if (!$("#wsite-mini-cart").length) {
        $(".spacer.hidden-sm").removeClass("spacer");
      }
    }

    // Category + Search sidebar dropdown on mobile
    $(".wsite-com-sidebar, #wsite-search-sidebar").click(function(){
      $(this).toggleClass("open");
    });

    // Overlay open functions

    var overlayopen = function(target) {
      $(target).on('click', function(e) {
    		e.preventDefault();
    		var target = $(this).attr("data-target")  ? $(this).attr("data-target") : "#search";
      	$('.overlay').not(target).removeClass('open');
    	  $(target).toggleClass('open');
    	  if ($('.overlay').hasClass("open")) {
    	    $('#close-overlay').addClass("visible");
    	  }
    	  else {
          $('#close-overlay').removeClass("visible");
    	  }
    	  return false;
    	});
    }

    // Move mobile nav

    if ($(".wsite-nav-cart").length) {
      if ($(window).width() > 767) {
        $("#nav-open").after('<div class="spacer"></div>');
        $('#wsite-nav-cart-a').unbind('mouseenter mouseleave');
        $('#wsite-nav-cart-a').attr("data-target","#wsite-mini-cart");
        overlayopen('#wsite-nav-cart-a');
      }
      else {
        var cartLink = $(".wsite-nav-cart").detach();
        $("#header-wrap").append(cartLink);
        $("#content-wrap").addClass("cartpad");
        $("#nav-open").after('<div class="spacer"></div>');
        $('#wsite-nav-cart-a').unbind('mouseenter mouseleave');
        $('#wsite-nav-cart-a').attr("data-target","#wsite-mini-cart");
        overlayopen('#wsite-nav-cart-a');
      }
    }

    // Cart change notification

    $('.wsite-product-button, #wsite-com-product-add-to-cart, .wsite-product-item .wsite-remove-button').on('click', function(){
      $('.cart-notice').fadeIn(300).delay(1600).fadeOut(300);
    });


    // Move submenu so it stays fixed



    // Initialize

    interval(800, 4000);

    overlayopen('#nav-open');
    overlayopen('#header-wrap .wsite-search-button');

    $('#close-overlay').on('click', function(e) {
  		e.preventDefault();
    	$('.overlay').removeClass('open');
      $('#close-overlay').removeClass("visible");
  	});

  	window.onkeydown = function(e) {
      if (e.keyCode == 27) {
        $('#close-overlay').trigger('click');
      }
    }

  });
});
