$(function () {
    $(window).bind("load", function () {
        var tweets = $('#tweetsRow li').toArray();
        var twitter = $('#tweetsRow ul');
        var newHeight;
        var containerHeight = $('#twitter .container').outerHeight();
        var containerWidth = ($(window).width() - $('#twitter .container').outerWidth())/2;
        $.each(tweets, function () {
            newHeight = twitter.outerHeight() - $(this).find(".user").outerHeight() -
                                                $(this).find(".tweet").outerHeight() -
                                                $(this).find(".interact").outerHeight(true) -
                                                $(this).find(".timePosted").outerHeight(true) - 40;
            if($(this).find(".media img").height() > $(this).find(".media img").width()) {
                $(this).find(".media img").css({
                    "height": newHeight*1.5 + "px"
                });
            } else {
                $(this).find(".media img").css({
                    "height": newHeight + "px"
                });
            }
            $(this).find(".media").css({
                "height": newHeight + "px"
            });
        });

        $('#leftArrow').css({
            'height': containerHeight,
            'width': containerWidth
        });

        $('#rightArrow').css({
            'height':containerHeight,
            'width': containerWidth
        });

    });

    $('#rightArrow').click(function() {
        $('#tweetsRow ul').animate({
            scrollLeft:"+="+380+"px"
        }, 700, function() {

            $('html, body').animate({
                scrollLeft: 0
            }, 700);

        });
    });

    $('#leftArrow').click(function() {
        $('#tweetsRow ul').animate({
            scrollLeft:"-="+380+"px"
        }, 700, function() {

            $('html, body').animate({
                scrollLeft: 0
            }, 700);

        });
    });

});
