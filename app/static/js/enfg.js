$(function () {
    // Do not reset on click
    $('#borough').find('option').mousedown(function (e) {
        e.preventDefault();
        $('#borough').focus();
        $(this).prop('selected', !$(this).prop('selected'));
        return false;
    });

    // Handle text change when clicking all boroughs button
    $('#all-boroughs').click(function () {
        if ($('#all-boroughs').text() === 'All Boroughs') {
            $('#borough option').prop('selected', true);
            $('#all-boroughs').text('Remove All')
        }
        else {
            $('#borough option').prop('selected', false);
            $('#all-boroughs').text('All Boroughs')
        }
    });
});
