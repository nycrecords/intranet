// Global variables used to pagination
var increment = 10;
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
    Util function to display post rows when prev button is clicked
    This is called as a result on hitting the /posts/search/ endpoint
     */
    var posts_selector = $('#posts-section');
    var posts_prev = $('#posts-prev');
    var posts_next = $('#posts-next');
    var posts_page_info = $('#posts-page-info');

    // Clear out and render new post rows
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
    Util function to display post rows when next button is clicked
    This is called as a result on hitting the /posts/search/ endpoint
     */
    var posts_selector = $('#posts-section');
    var posts_prev = $('#posts-prev');
    var posts_next = $('#posts-next');
    var posts_page_info = $('#posts-page-info');

    // Clear out and render new posts rows
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

function getSelectedTags() {
    /*
    Util function to determine which tags are currently selected
     */
    var tags = [];
    $('.tag-checkbox').each(function () {
        if ($(this).is(':checked')) {
            tags.push($(this).val());
        }
    });
    return tags;
}

function getSelectedPostTypes() {
    /*
    Util function to determine what post types are currently selected
     */
    var post_types = [];
    // If on meeting notes page, strictly filter on meeting notes
    if ($('.breadcrumb-header').text() === 'Meeting Notes'){
        post_types = ['meeting_notes'];
        return post_types;
    }
    // If on news page, strictly filter on news
    else if ($('.breadcrumb-header').text() === 'News'){
        post_types = ['news'];
        return post_types;
    }
    // Otherwise determine which types are selected
    else {
        $('.post-type-checkbox').each(function () {
            if ($(this).is(':checked')) {
                post_types.push($(this).val());
            }
        });
        // If none are selected, filter on all types
        if (post_types.length === 0) {
            post_types = ['news', 'event_posts', 'meeting_notes'];
        }
        return post_types;
    }
}

function getSelectedMeetingTypes() {
    /*
    Util function to determine what meeting types are currently selected
     */
    // If on meeting notes page, determine which types are selected
    if ($('.breadcrumb-header').text() === 'Meeting Notes') {
        var meeting_types = [];
        $('.meeting-type-checkbox').each(function () {
            if ($(this).is(':checked')) {
                meeting_types.push($(this).val());
            }
        });
        // If none are selected, filter on all meeting types
        if (meeting_types.length === 0) {
            meeting_types = ['Division', 'Strategic Planning', 'Senior Staff', 'Project', 'Agency'];
        }
        return meeting_types;
    }
    // Otherwise return an empty list
    return [];
}

$('#posts-prev').click(function () {
    // Update pagination counters
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
            'post_type': getSelectedPostTypes(),
            'posts_start': posts_start,
            'posts_end': posts_end,
            'tags': getSelectedTags()
        },
        success: function (data) {
            displayPreviousResults(data); // Render the new rows
            $(window).scrollTop(0); // Scroll to top of page
        }
    });
});

$('#posts-next').click(function () {
    // Update pagination counters
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
            'post_type': getSelectedPostTypes(),
            'posts_start': posts_start,
            'posts_end': posts_end,
            'tags': getSelectedTags()
        },
        success: function (data) {
            displayNextResults(data); // Render the new rows
            $(window).scrollTop(0); // Scroll to top of page
        }
    });
});


$(function () {
    // AJAX call for initial page load
    $.ajax({
        url: '/posts/search/',
        type: 'GET',
        dataType: 'json',
        data: {
            'sort_by': $('#sort-dropdown').find('option:selected').val(),
            'search_term': $('#save-search-term').text(),
            'post_type': getSelectedPostTypes(),
            'posts_start': posts_start,
            'posts_end': posts_end,
            'meeting_type': getSelectedMeetingTypes()
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
                'post_type': getSelectedPostTypes(),
                'posts_start': posts_start,
                'posts_end': posts_end,
                'tags': getSelectedTags(),
                'meeting_type': getSelectedMeetingTypes()
            },
            success: function (data) {
                displayResults(data);
            }
        });
    });

    // Handler for each time a new tag is selected
    $('.tag-checkbox').click(function() {
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
                'post_type': getSelectedPostTypes(),
                'posts_start': posts_start,
                'posts_end': posts_end,
                'tags': getSelectedTags(),
                'meeting_type': getSelectedMeetingTypes()
            },
            success: function (data) {
                displayResults(data);
            }
        });
    });

    // Handler for each time a post type is selected
    $('.post-type-checkbox').click(function() {
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
                'post_type': getSelectedPostTypes(),
                'posts_start': posts_start,
                'posts_end': posts_end,
                'tags': getSelectedTags(),
                'meeting_type': getSelectedMeetingTypes()
            },
            success: function (data) {
                displayResults(data);
            }
        });
    });

    // Handler for each time a meeting type is selected
    $('.meeting-type-checkbox').click(function() {
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
                'post_type': getSelectedPostTypes(),
                'posts_start': posts_start,
                'posts_end': posts_end,
                'tags': getSelectedTags(),
                'meeting_type': getSelectedMeetingTypes()
            },
            success: function (data) {
                displayResults(data);
            }
        });
    });
});