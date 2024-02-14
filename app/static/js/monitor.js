// Uses "data" to display information on the table
function WebsiteMonitorFunction () {
    // "this" cannot be used inside an ajax call.
    const websiteID = $(this).attr('id').split('-').pop();
    const tableRow = $(this);

    $.ajax({
        url: '/monitor',
        type: 'POST',
        data: {
            url: $('#website-' + websiteID + '-url').attr('href')
        },
        success: function (data) {
            // Color the bars on the table.
            if (data['status_code'] === '200') {
                tableRow.removeClass('danger');
                tableRow.removeClass('warning');
                tableRow.addClass('success');

                $('#website-' + websiteID + '-check').show();
                $('#website-' + websiteID + '-warning').hide();
                $('#website-' + websiteID + '-x').hide();
            } else {
                tableRow.removeClass('warning');
                tableRow.removeClass('success');
                tableRow.addClass('danger');

                // Hide and show the check and x symbol
                $('#website-' + websiteID + '-check').hide();
                $('#website-' + websiteID + '-warning').hide();
                $('#website-' + websiteID + '-x').show();
            }
            // Inject data
            $('#website-' + websiteID + '-time').html(data['current_timestamp']);
            $('#website-' + websiteID + '-time-2').html(data['most_recent_success']);
            $('#website-' + websiteID + '-status-code').html(data['status_code']);
            $('#modalBody-' + websiteID).html(data['reason']);
        },
        error: function (data) {
            tableRow.removeClass('danger');
            tableRow.removeClass('success');
            tableRow.addClass('warning');

            // Hide and show the check and x symbol
            $('#website-' + websiteID + '-check').hide();
            $('#website-' + websiteID + '-x').hide();
            $('#website-' + websiteID + '-warning').show();
        }
    });
}

$(document).ready(function () {
    // Calls the WebsiteMonitorFunction
    $('.website').each(WebsiteMonitorFunction);

    setInterval(function () {
        $('.website').each(WebsiteMonitorFunction);
    }, $("meta[name='site-refresh-rate']").attr('content'));


    // Create the individual modals.
    $('#monitor-table').find('tr[data-id]').on('click', function () {
        let modalDataID = $(this).data('id');
        $('#monitor-modal-' + modalDataID).modal('show');
    });
});

// Stops modal and link from being opened at the same time.
$('.website-url').click(function (event) {
    event.stopPropagation();
})