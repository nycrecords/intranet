$(function () {
    $("#datepicker").datepicker();

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

    $("#filter-menu").on("focus", ".request-type", function () {
        var target = document.activeElement.id;
        target = target.replace("request-type-", "");
        var targetId = "#" + document.activeElement.id;
        $("#filter-menu").off().change(function () {
            if (target == "First Name") {

                $.ajax({
                    url: "/get_user_first_names/",
                    type: "GET",
                    success: function (data) {
                        $("#test").autocomplete({
                            source: data
                        });
                    }
                });
            }

            else if (target == "Last Name") {

                $.ajax({
                    url: "/get_user_last_names/",
                    type: "GET",
                    success: function (data) {
                        $("#test").autocomplete({
                            source: data
                        });
                    }
                });
            }

            else if (target == "Division") {

                $.ajax({
                    url: "/get_user_division/",
                    type: "GET",
                    success: function (data) {
                        $("#test").autocomplete({
                            source: data
                        });
                    }
                });
            }

            else if (target == "Title") {

                $.ajax({
                    url: "/get_user_title/",
                    type: "GET",
                    success: function (data) {
                        $("#test").autocomplete({
                            source: data
                        });
                    }
                });
            }

            else {
                $.ajax({
                    url: "/get_user_first_names/",
                    type: "GET",
                    success: function (data) {
                        $("#test").autocomplete({
                            source: data
                        });
                    }
                });
            }
        });
    });


    // $('#filter').on(function(){
    //    var value = $('#filter-data').val();
    //     $.ajax({
    //         url: "/get_user_data'/",
    //         type: "GET",
    //         success: function (data) {
    //             $("#test").autocomplete({
    //                 source: data
    //             });
    //         }
    //     });
    // });

    tinymce.init({selector: 'textarea'});

    $('[data-toggle="popover"]').popover({
        placement: 'right',
        html: true,
        content: function () {
            return $(this).next('.popper-content').html();
        }
    });
    $(document).on("click", ".popover-content .close", function () {
        $(this).parents(".popover").popover('hide');
    });
    $('[data-toggle=popover]').on('click', function () {
        $('[data-toggle=popover]').not(this).popover('hide');
    });

});

