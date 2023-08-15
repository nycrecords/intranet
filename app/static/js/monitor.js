// Uses "data" to display information on the table
function WebsiteMonitorFunction () {
    // "this" cannot be used inside an ajax call.
    const el = $(this)

    $.ajax({
        url: '/Test',
        type: 'POST',
        success: function (data) {
            console.log(data);

            // Color the bars on the table.
            el.removeClass("danger")
            el.addClass("success")

            let checkId = el.find('.check').attr('id');
            $('#' + checkId).show();

            let xId = el.find('.x').attr('id');
            $('#' + xId).hide();

            let timeId = el.find('.time').attr('id');
            $('#' + timeId).html(data["time-stamp"]);
            $('#' + timeId).show(data["time-stamp"]);

            let timeId2 = el.find('.time-2').attr('id');
            $('#' + timeId2).html(data["time-stamp-2"]);
            $('#' + timeId2).show(data["time-stamp-2"]);

            let websiteStatusCode = el.find('.status').attr('id');
            $('#' + websiteStatusCode).html(data["status-code-success"]);
            // $('#' + websiteStatusCode).show(data["status-code-success"]);
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

    }, 10000);


// Create the individual modals.
    $("#monitor-table").find('tr[data-id]').on('click', function () {
        let modalDataID = $(this).data('id')
        $('#' + 'monitor-modal-' + modalDataID).modal('show');
    });
});




