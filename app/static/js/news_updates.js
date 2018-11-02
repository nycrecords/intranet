var increment = 2;
var posts_start = 0;
var posts_end = increment;

$(document).ready(function(){
    // initializes popovers
    $('.new-post-popover').popover({
        placement: 'right',
        html: true,
        container: "body",
        content: function () {
            return $(this).next('.popover-content').html();
        }
    });
});

function displayResults (data) {
    /*
    Util function to display posts rows for a specific posts type tab
    This is called as a result on hitting the /posts/search/ endpoint
     */
    var posts_selector = $('#posts-section');
    var posts_prev = $('#posts-prev');
    var posts_next = $('#posts-next');
    var posts_page_info = $('#posts-page-info');

    posts_selector.html(''); // Clear out existing html
    posts_selector.html(data['posts']); // Render new posts rows

    // Conditional block to determine what should be displayed on the page info part of the pagination div
    // and whether or not to show/hide the next/prev buttons
    if (data['posts_max'] === 0) {
        posts_prev.hide();
        posts_next.hide();
        posts_page_info.html(0 + ' - ' + 0 + ' of ' + 0);
    }
    else if (data['posts_max'] <= increment) {
        posts_prev.hide();
        posts_next.hide();
        posts_page_info.html(data['posts_start'] + ' - ' + data['posts_max'] + ' of ' + data['posts_max']);
    }
    else if (data['posts_start'] === 1) {
        posts_page_info.html(data['posts_start'] + ' - ' + data['posts_end'] + ' of ' + data['posts_max']);
        posts_prev.hide();
        posts_next.show();
    }
    else {
        posts_page_info.html(data['posts_start'] + ' - ' + data['posts_end'] + ' of ' + data['posts_max']);
        posts_prev.show();
    }
}

function displayPreviousResults(data) {
    /*
    Util function to display document rows for a specific document type tab when prev button is clicked
    This is called as a result on hitting the /documents/page/ endpoint
     */
    var posts_selector = $('#posts-section');
    var posts_prev = $('#posts-prev');
    var posts_next = $('#posts-next');
    var posts_page_info = $('#posts-page-info');

    // Clear our and render new document rows
    posts_selector.html(''); // Clear out existing html
    posts_selector.html(data['posts']); // Render new posts rows

    // Set page info and determine visibility of pagination buttons
    if (data['posts_start'] === 1) {
        posts_prev.hide();
    }
    posts_next.show();
    posts_page_info.html(data['posts_start'] + ' - ' + data['posts_end'] + ' of ' + data['posts_max']);
}

function displayNextResults(data) {
    /*
    Util function to display document rows for a specific document type tab when next button is clicked
    This is called as a result on hitting the /documents/page/ endpoint
     */
    var posts_selector = $('#posts-section');
    var posts_prev = $('#posts-prev');
    var posts_next = $('#posts-next');
    var posts_page_info = $('#posts-page-info');

    // Clear our and render new document rows
    posts_selector.html(''); // Clear out existing html
    posts_selector.html(data['posts']); // Render new posts rows

    // Set page info and determine visibility of pagination buttons
    if (data['posts_end'] >= data['posts_max']) {
        posts_page_info.html(data['posts_start'] + ' - ' + data['posts_max'] + ' of ' + data['posts_max']);
        posts_next.hide();
    }
    else {
        posts_page_info.html(data['posts_start'] + ' - ' + data['posts_end'] + ' of ' + data['posts_max']);
    }
    posts_prev.show();
}

$('#posts-prev').click(function () {
    // increment the page counters for that document type
    posts_start = posts_start - increment;
    posts_end = posts_end - increment;

    // AJAX call to get the next rows that should display on the frontend
    $.ajax({
        url: '/posts/search/',
        type: 'GET',
        dataType: 'json',
        data: {
            'sort_by': $('#sort-dropdown').find('option:selected').val(),
            'search_term': '',
            'post_type': ['news', 'event_posts', 'meeting_notes'],
            'posts_start': posts_start,
            'posts_end': posts_end
        },
        success: function (data) {
            displayPreviousResults(data); // Render the new rows
        }
    });
});

$('#posts-next').click(function () {
    // increment the page counters for that document type
    posts_start = posts_start + increment;
    posts_end = posts_end + increment;

    // AJAX call to get the next rows that should display on the frontend
    $.ajax({
        url: '/posts/search/',
        type: 'GET',
        dataType: 'json',
        data: {
            'sort_by': $('#sort-dropdown').find('option:selected').val(),
            'search_term': '',
            'post_type': ['news', 'event_posts', 'meeting_notes'],
            'posts_start': posts_start,
            'posts_end': posts_end
        },
        success: function (data) {
            displayNextResults(data); // Render the new rows
        }
    });
});


var test = ['news', 'event_posts', 'meeting_notes'];
$(function () {
    // AJAX call for initial page load
    $.ajax({
        url: '/posts/search/',
        type: 'GET',
        dataType: 'json',
        data: {
            'sort_by': $('#sort-dropdown').find('option:selected').val(),
            'search_term': $('#save-search-term').text(),
            'post_type': ['news', 'event_posts', 'meeting_notes'],
            'posts_start': posts_start,
            'posts_end': posts_end
        },
        success: function (data) {
            // Render the rows for each posts type
            displayResults(data);

            var search_term = $('#save-search-term').text();
            if (search_term !== '') {
                $('#display-search-term').show();
            }
            else {
                $('#display-search-term').hide();
            }
        }
    });

    // Handle sort by dropdown change event
    $('#sort-dropdown').change(function() {
        // Reset page counters
        posts_start = 0;
        posts_end = increment;

        $.ajax({
            url: '/posts/search/',
            type: 'GET',
            dataType: 'json',
            data: {
                'sort_by': $('#sort-dropdown').find('option:selected').val(),
                'search_term': $('#save-search-term').text(),
                'post_type': ['news', 'event_posts', 'meeting_notes'],
                'posts_start': posts_start,
                'posts_end': posts_end
            },
            success: function (data) {
                displayResults(data);
            }
        });
    });
});