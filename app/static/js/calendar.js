$(function () {
    // Get the current month and year to be passed back in AJAX call
    var today = new Date();
    var month = today.getMonth() + 1;
    var year = today.getFullYear();

    $.ajax({
        type: 'GET',
        url: '/get_events/',
        data: {'month': month,'year': year},
        dataType: 'json',
        success: function (data) {
            // Set event dates to highlight on calendar
            var eventDates = {};
            for (var i = 0; i < data['dates'].length; i++) {
                eventDates[new Date(data['dates'][i])] = new Date(data['dates'][i]);
            }
            // initialize datepicker plugin to act as the calendar
            $('#datepicker').datepicker({
                // Before showing each day check if it is in the list of eventDates. If it is then give it the 'event'
                // class which will use CSS to highlight it on the calendar
                beforeShowDay: function (date) {
                    var highlight = eventDates[date];
                    if (highlight) {
                        return [true, 'event'];
                    } else {
                        return [true, ''];
                    }
                },
                // Each time you change the month, pass the month and year to the backend to query for that
                // month's events
                onChangeMonthYear: function (year, month, inst) {
                    $.ajax({
                        type: 'GET',
                        url: '/get_events/',
                        data: {'month': month,'year': year},
                        dataType: 'json',
                        success: function (data) {
                            // update eventDates to highlight new dates
                            eventDates = {};
                            for (var i = 0; i < data['dates'].length; i++) {
                                eventDates[new Date(data['dates'][i])] = new Date(data['dates'][i]);
                            }
                            // refresh the calendar so beforeShowDate runs again
                            $("#datepicker").datepicker("refresh");
                            // render the template to the events row section
                            $('#event-rows').html(data['template']);
                        }
                    });
                }
            });
            // render the template to the event rows section
            $('#event-rows').html(data['template']);
        }
    });
});