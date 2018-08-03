$(function () {
    // $("#datepicker").datepicker();
    // $(".datepicker").datepicker();
    $("#meeting-date-datepicker").datepicker();
    $("#next-meeting-date-datepicker").datepicker();

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


    $('#textarea')
        .textext({
            plugins: 'tags autocomplete'
        })
        .bind('getSuggestions', function (e, data) {
            var list = [
                    'Basic',
                    'Closure',
                    'Cobol',
                    'Delphi',
                    'Erlang',
                    'Fortran',
                    'Go',
                    'Groovy',
                    'Haskel',
                    'Java',
                    'JavaScript',
                    'OCAML',
                    'PHP',
                    'Perl',
                    'Python',
                    'Ruby',
                    'Scala'
                ],
                textext = $(e.target).textext()[0],
                query = (data ? data.query : '') || ''
            ;

            $(this).trigger(
                'setSuggestions',
                {result: textext.itemManager().filter(list, query)}
            );
        });

    tinymce.init({selector: 'textarea'});

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
});

