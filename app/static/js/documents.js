$(function () {
    // handle close button text on use policy
    $('.intranet-use-policy-close-button').click(function () {
        if ($('#intranet-use-policy').hasClass('in')) {
            $('.intranet-use-policy-close-button').text('Open');
        }
        else {
            $('.intranet-use-policy-close-button').text('Close');
        }
    });

    // set parsley for required fields
    var requiredFields = ['title',
                          'document-type',
                          'division',
                          'file-object'];
    for (var i = 0; i < requiredFields.length; i++) {
        $('#' + requiredFields[i]).attr('data-parsley-required', '');
    }
});