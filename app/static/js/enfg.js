$(function () {
    // Do not reset on click
    $('#borough').find('option').mousedown(function (e) {
        e.preventDefault();
        $('#borough').focus();
        $(this).prop('selected', !$(this).prop('selected'));
        return false;
    });
});
