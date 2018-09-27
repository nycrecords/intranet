$(function () {
    // On first page load get autocomplete options for default filters
    $(document).ready(function () {
        $.ajax({
            url: '/get_filter_options_list/' + $('#filter-data').val(),
            type: "GET",
            success: function (data) {
                $("#staff-directory-search-data").autocomplete({
                    source: data
                });
            }
        });
    });

    // handles autocomplete options on filter change
    $(document).on("focus", "#filter-data", function () {
        $("#filter-data").off().change(function () {
            $.ajax({
                url: '/get_filter_options_list/' + $('#filter-data').val(),
                type: "GET",
                success: function (data) {
                    $("#staff-directory-search-data").autocomplete({
                        source: data
                    });
                }
            });
        });
    });

    // initializes popovers
    $('.popper').popover({
        placement: 'right',
        html: true,
        container: "body",
        content: function () {
            return $(this).next('.popover-content').html();
        }
    });

    // handles dismissing popovers with close button
    $(document).on("click", ".popover-content .close", function () {
        $(this).parents(".popover").popover('hide');
    });

    // handles dismiss of current popover when you click another popover
    $('[data-toggle="popover"]').on('click', function () {
        $('[data-toggle=popover]').not(this).popover('hide');
    });

    $('[data-toggle="popover"]').popover();

    // handles dismiss of popover when you click outside
    $('body').on('click', function (e) {
        $('[data-toggle="popover"]').each(function () {
            // the 'is' for buttons that trigger popups
            // the 'has' for icons within a button that triggers a popup
            if (!$(this).is(e.target) && $(this).has(e.target).length === 0 && $('.popover').has(e.target).length === 0) {
                $(this).popover('hide');
            }
        });
    });
});