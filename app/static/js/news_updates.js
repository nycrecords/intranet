$(document).ready(function(){
    // // initializes popovers
    $('.new-post-popover').popover({
        placement: 'right',
        html: true,
        container: "body",
        content: function () {
            return $(this).next('.popover-content').html();
        }
    });
});