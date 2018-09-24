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

    $('.popper').popover({
        placement: 'right',
        html: true,
        container: "body",
        content: function () {
            return $(this).next('.popper-content').html();
        }
    });

    $(document).on("click", ".popover-content .close", function () {
        $(this).parents(".popover").popover('hide');
    });

    $('[data-toggle="popover"]').on('click', function () {
        $('[data-toggle=popover]').not(this).popover('hide');
    });
});