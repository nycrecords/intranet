$(function () {
    // $("#datepicker").datepicker();
    // $(".datepicker").datepicker();
    // $("#meeting-date-datepicker").datepicker();
    // $("#next-meeting-date-datepicker").datepicker();
    $("#meeting-date-datepicker").datepicker({
        dateFormat: "mm/dd/yy",
        maxDate: 0
    }).keydown(function (e) {
        // prevent keyboard input except for tab
        if (e.keyCode !== 9) {
            e.preventDefault();
        }
    });

    $("#next-meeting-date-datepicker").datepicker({
        dateFormat: "mm/dd/yy",
    }).keydown(function (e) {
        // prevent keyboard input except for tab
        if (e.keyCode !== 9) {
            e.preventDefault();
        }
    });
    try {
        // render timepicker plugins
        $(".timepicker").timepicker({
            timeFormat: "h:mm p",
            interval: 5,
            minTime: "12:00am",
            maxTime: "11:59pm",
            startTime: "9:00am",
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

    var options = {
        data: ["blue", "green", "pink", "red", "yellow"]
    };

    $("#basics").easyAutocomplete(options);


    //Getting content from the tinymce text-editor and saving it's characters to the datebase
    window.onload = function () {
        tinymce.init({
            selector: 'textarea',
            // plugins: 'paste',
            // paste_auto_cleanup_on_paste: true,
            // paste_remove_styles: true,
            // paste_remove_styles_if_webkit: true,
            // paste_strip_class_attributes: true,
            // remove_trailing_brs: false,
            // paste_as_text: true,
            // forced_root_block: "",
            setup: function (ed) {
                ed.on('keyup', function (e) {
                    ed.save();
                    var element = document.getElementById('content');
                    var text = element.innerText || element.textContent;
                    element.innerHTML = text;
                });
            }
        });
    }

    //autocomplete using ajax for meeting leader and next meeting leader
    var users = [];
    $.ajax({
        url: "/get_user_list/",
        type: "GET",
        dataType: "json",
        success: function (data) {
            for (key in data) {
                var userJSON = {};
                userJSON["value"] = key;
                userJSON["label"] = data[key];
                users.push(userJSON);
            }

            $("#meeting-leader").autocomplete({
                source: users,
                focus: function (event, ui) {
                    $("#meeting-leader").val(ui.item.label);
                    return false;
                },
                select: function (event, ui) {
                    $("#meeting-leader").val(ui.item.label);
                    $("#meeting-leader-id").val(ui.item.value);
                    return false;
                }
            });

            $("#meeting-note-taker").autocomplete({
                source: users,
                focus: function (event, ui) {
                    $("#meeting-note-taker").val(ui.item.label);
                    return false;
                },
                select: function (event, ui) {
                    $("#meeting-note-taker").val(ui.item.label);
                    $("#meeting-note-taker-id").val(ui.item.value);
                    return false;
                }
            });

            $("#next-meeting-leader").autocomplete({
                source: users,
                focus: function (event, ui) {
                    $("#next-meeting-leader").val(ui.item.label);
                    return false;
                },
                select: function (event, ui) {
                    $("#next-meeting-leader").val(ui.item.label);
                    $("#next-meeting-leader-id").val(ui.item.value);
                    return false;
                }
            });

            $("#next-meeting-note-taker").autocomplete({
                source: users,
                focus: function (event, ui) {
                    $("#next-meeting-note-taker").val(ui.item.label);
                    return false;
                },
                select: function (event, ui) {
                    $("#next-meeting-note-taker").val(ui.item.label);
                    $("#next-meeting-note-taker-id").val(ui.item.value);
                    return false;
                }
            });

        }
    });

    //required validation for the StringFields
    var requiredFields = ["title", "meeting-type", "division", "meeting-date-datepicker", "meeting-location",
        "start-time", "end-time", "attendees", "tags", "content", "next-meeting-date-datepicker"]

    for (var i = 0; i < requiredFields.length; i++) {
        $("#" + requiredFields[i]).attr("data-parsley-required", "");
    }

    //max and min length validation
    $("#title").attr("data-parsley-maxlength", 100);
    $("#title").attr("data-parsley-minlength", 10);
    $("#meeting-location").attr("data-parsley-maxlength", 100);


});

