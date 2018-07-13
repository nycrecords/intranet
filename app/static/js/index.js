$('#first-name').attr('data-parsley-required', '');
$('#last-name').attr('data-parsley-required', '');

$('#email').attr('data-parsley-type', 'email');

// Prevent user from pressing keys other than digits when typing in phone number and zipcode
$('#phone').keypress(function (key) {
    if (key.charCode != 0) {
        if (key.charCode < 48 || key.charCode > 57) {
            key.preventDefault();
        }
    }
});

$('#zipcode').keypress(function (key) {
    if (key.charCode != 0) {
        if (key.charCode < 48 || key.charCode > 57) {
            key.preventDefault();
        }
    }
});

// jQuery mask plugin to format fields
$('#phone').mask("(999) 999-9999");

$('#phone').attr('data-parsley-length', '[14,14]');
$('#zipcode').attr('data-parsley-length', '[5,5]');


$('#phone').attr('data-parsley-length-message', 'The phone number must be 10 digits.');
$('#zipcode').attr('data-parsley-length-message', 'The zipcode must be 5 digits.');


// Disable default error messages for phone and zipcode so a custom one can be used instead.
$('#phone').attr('data-parsley-required-message', '');
$('#zipcode').attr('data-parsley-required-message', '');


$('#submit').click(function () {
    if (!$('#library').is(":checked") && !$('#archives').is(":checked") && !$('#genealogy').is(":checked")) {
        $('.library-archive-genealogy-error-message').show();
    }
    else {
        $('.library-archive-genealogy-error-message').hide();
    }
});

$("#sign-in-form").submit(function (event) {
    if (!$('#library').is(":checked") && !$('#archives').is(":checked") && !$('#genealogy').is(":checked")) {
        event.preventDefault();
    }
});