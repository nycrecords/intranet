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

    // handle sort by dropdown change event
    $('#sort-dropdown').change(function() {
        $.ajax({
            url: '/documents/sort/',
            type: 'GET',
            dataType: 'json',
            data: {
                'sort_by': $('option:selected', this).val(),
                'current_tab': $('.tablinks.active').val(),
                'search_term': $('#save-search-term').text()
            },
            success: function (data) {
                // if (response.redirect) {
                //     window.location.href = response.redirect;
                // }
                $('#instructions').html('');
                $('#policies-and-procedures').html('');
                $('#templates').html('');
                $('#training-materials').html('');
                $('#instructions').html(data['instructions']);
                $('#policies-and-procedures').html(data['policies_and_procedures']);
                $('#templates').html(data['templates']);
                $('#training-materials').html(data['training_materials']);
            }
        });
    });


    $('.documents-search-button').click(function() {
        var search_term = $('#document-search-term').val();
        $('#document-search-term').val('');
        $.ajax({
            url: '/documents/sort/',
            type: 'GET',
            dataType: 'json',
            data: {
                'sort_by': $('option:selected', this).val(),
                'current_tab': $('.tablinks.active').val(),
                'search_term': search_term
            },
            success: function (data) {
                // if (response.redirect) {
                //     window.location.href = response.redirect;
                // }
                $('#instructions').html('');
                $('#policies-and-procedures').html('');
                $('#templates').html('');
                $('#training-materials').html('');
                $('#instructions').html(data['instructions']);
                $('#policies-and-procedures').html(data['policies_and_procedures']);
                $('#templates').html(data['templates']);
                $('#training-materials').html(data['training_materials']);
                if (search_term !== '') {
                    $('#save-search-term').html(search_term);
                    $('#display-search-term').show()
                }
                else {
                    $('#save-search-term').html('');
                    $('#display-search-term').hide()
                }
            }
        });
    });
});