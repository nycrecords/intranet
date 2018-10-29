function openTab(evt, tabName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName('tabcontent');
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = 'none';
    }
    tablinks = document.getElementsByClassName('tablinks');
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(' active', '');
    }
    document.getElementById(tabName).style.display = 'block';
    evt.currentTarget.className += ' active';
}
document.getElementById('default-open').click();

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