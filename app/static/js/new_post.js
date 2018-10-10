$(function () {
    // initialize datepickers
    $('#meeting-date').datepicker({
        dateFormat: 'mm/dd/yy',
        maxDate: 0
    }).keydown(function (e) {
        // prevent keyboard input except for tab
        if (e.keyCode !== 9) {
            e.preventDefault();
        }
    });

    $('#next-meeting-date').datepicker({
        dateFormat: 'mm/dd/yy'
    }).keydown(function (e) {
        // prevent keyboard input except for tab
        if (e.keyCode !== 9) {
            e.preventDefault();
        }
    });

    try {
        // initialize timepicker plugins
        $('.timepicker').timepicker({
            timeFormat: 'h:mm p',
            interval: 5,
            minTime: '12:00am',
            maxTime: '11:59pm',
            startTime: '9:00am',
            dynamic: false,
            dropdown: true,
            scrollbar: true
        }).keydown(function (e) {
            // prevent keyboard input except for allowed keys
            if (e.keyCode !== 8 && // backspace
                e.keyCode !== 9 && // tab
                e.keyCode !== 37 && // left-arrow
                e.keyCode !== 39 && // right-arrow
                e.keyCode !== 48 && // 0
                e.keyCode !== 49 && // 1
                e.keyCode !== 50 && // 2
                e.keyCode !== 51 && // 3
                e.keyCode !== 52 && // 4
                e.keyCode !== 53 && // 5
                e.keyCode !== 54 && // 6
                e.keyCode !== 55 && // 7
                e.keyCode !== 56 && // 8
                e.keyCode !== 57 && // 9
                e.keyCode !== 16 && // Shift
                e.keyCode !== 65 && // a
                e.keyCode !== 77 && // m
                e.keyCode !== 80 && // p
                e.keyCode !== 186) {// semi-colon
                e.preventDefault();
            }
        });

    }
    catch (err) {
        // if one of the forms doesn't have a time field it will throw an error when you try to render it
        // TODO: find a better way to handle this error
    }

    // initialize tinymce editor
    tinymce.init({
        selector: 'textarea',
        plugins: 'lists'
    });

    // set parsley for required fields
    var requiredFields = ['title',
                          'meeting-type',
                          'division',
                          'meeting-date',
                          'meeting-location',
                          'meeting-leader',
                          'meeting-note-taker',
                          'start-time',
                          'end-time',
                          'attendees',
                          'tags',
                          'next-meeting-date',
                          'next-meeting-leader',
                          'next-meeting-note-taker'];
    for (var i = 0; i < requiredFields.length; i++) {
        $('#' + requiredFields[i]).attr('data-parsley-required', '');
    }

    // set user choices for autocomplete using ajax
    $.ajax({
        url: '/get_user_list/',
        type: 'GET',
        success: function (data) {
            $('#meeting-leader').autocomplete({
                source: data
            });
            $('#meeting-note-taker').autocomplete({
                source: data
            });
            $('#next-meeting-leader').autocomplete({
                source: data
            });
            $('#next-meeting-note-taker').autocomplete({
                source: data
            });
        }
    });

    // initialize multiselect plugin for tags
    $('#tags').multiselect({
        maxHeight: 400,
        buttonText: function (options, select) {
            if (options.length === 0) {
                return 'None Selected';
            }
            else if (options.length > 4) {
                return options.length + ' tags selected';
            }
            else {
                var labels = [];
                options.each(function () {
                    if ($(this).attr('label') !== undefined) {
                        labels.push($(this).attr('label'));
                    }
                    else {
                        labels.push($(this).html());
                    }
                });
                return labels.join(', ') + '';
            }
        },
        enableCaseInsensitiveFiltering: true,
        includeResetOption: true,
        includeResetDivider: true,
        resetText: 'Clear all',
        buttonWidth: '50%'
    });

    // initialize multiselect plugin for attendees
    $('#attendees').multiselect({
        maxHeight: 400,
        buttonText: function (options, select) {
            if (options.length === 0) {
                return 'None Selected';
            }
            else if (options.length > 4) {
                return options.length + ' people selected';
            }
            else {
                var labels = [];
                options.each(function () {
                    if ($(this).attr('label') !== undefined) {
                        labels.push($(this).attr('label'));
                    }
                    else {
                        labels.push($(this).html());
                    }
                });
                return labels.join(', ') + '';
            }
        },
        enableCaseInsensitiveFiltering: true,
        includeResetOption: true,
        includeResetDivider: true,
        resetText: 'Clear all',
        buttonWidth: '50%'
    });

    $("#new-meeting-notes-form").submit(function (e) {
        // Validate that content has been filled out
        if (tinyMCE.activeEditor.getContent() === '') {
            $('#content-error').show();
            e.preventDefault()
        }
    });
});