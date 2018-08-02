$('.popper').popover({
    placement: 'right',
    container: 'body',
    html: true,
    content: function () {
        return $(this).next('.popper-content').html();
    }
});