// Uses "data" to display information on the table
function WebsiteMonitorFunction () {
    // "this" cannot be used inside an ajax call.
    const websiteID = $(this).attr('id').split('-').pop()
    const tableRow = $(this)

    $.ajax({
        url: '/monitor',
        type: 'POST',
        data: {
            url: $('#website-' + websiteID + '-url').attr('href')
        },
        success: function (data) {
            // Color the bars on the table.
            if (data['status_code'] === '200') {
                tableRow.removeClass("danger")
                tableRow.addClass("success")

                $('#website-' + websiteID + '-check').show();
                $('#website-' + websiteID + '-x').hide();
            } else {
                tableRow.removeClass("success")
                tableRow.addClass("danger")

                // Hide and show the check and x symbol
                $('#website-' + websiteID + '-check').hide();
                $('#website-' + websiteID + '-x').show();
            }

            // Inject data
            $('#website-' + websiteID + '-time').html(data["current_timestamp"]);
            $('#website-' + websiteID + '-time-2').html(data["most_recent_success"]);
            $('#website-' + websiteID + '-status-code').html(data["status_code"]);
            $('#modalBody-' + websiteID).html(data['reason']);
        },

        error: function (data) {
            console.log(data);

            el.removeClass("success")
            el.addClass("danger")

            // Hide and show the check and x symbol
            let checkId = el.find('.check').attr('id');
            $('#' + checkId).hide();


            let xId = el.find('.x').attr('id');
            $('#' + xId).show();

            // Estimated time found in monitor.py and displayed.
            let timeId = el.find('.time').attr('id');
            $('#' + timeId).html(data["time-stamp"]);
            $('#' + timeId).show(data["time-stamp"]);

            let timeId2 = el.find('.time-2').attr('id');
            $('#' + timeId2).html(data["time-stamp-2"]);
            $('#' + timeId2).show(data["time-stamp-2"]);

            let websiteStatusCode = el.find('.status').attr('id');
            $('#' + websiteStatusCode).html(data["responseJSON"]["status-code-error"]);
            // $('#' + websiteStatusCode).show(data["responseJSON"]["status-code-error"]);

        }
    });
}

$(document).ready(function () {
    // calls the WebsiteMonitorFunction
    $(".website").each( WebsiteMonitorFunction );

    setInterval(function () {
        $(".website").each( WebsiteMonitorFunction );

    }, 60000);


// Create the individual modals.
    $("#monitor-table").find('tr[data-id]').on('click', function () {
        let modalDataID = $(this).data('id')
        $('#monitor-modal-' + modalDataID).modal('show');
    });
});

// Stops modal and link from being opened at the same time.
$(".website-url").click(function (event) {
    event.stopPropagation();
})