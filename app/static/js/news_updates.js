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
    Util function to display post rows when next button is clicked
    This is called as a result on hitting the /posts/search/ endpoint
     */
    var posts_selector = $('#posts-section');
    var posts_prev = $('#posts-prev');
    var posts_next = $('#posts-next');
    var posts_page_info = $('#posts-page-info');

    // Clear our and render new posts rows
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
    var tags = [];
    $('.tag-checkbox').each(function () {
        if ($(this).is(':checked')) {
            tags.push($(this).val());
        }
    });
    return tags;
}

function getSelectedPostTypes() {
    var post_types = [];
    if ($('.breadcrumb-header').text() === 'Meeting Notes'){
        post_types = ['meeting_notes'];
        return post_types;
    }
    else if ($('.breadcrumb-header').text() === 'News'){
        post_types = ['news'];
        return post_types;
    }
    else {
        $('.post-type-checkbox').each(function () {
            if ($(this).is(':checked')) {
                post_types.push($(this).val());
            }
        });
        if (post_types.length === 0) {
            post_types = ['news', 'event_posts', 'meeting_notes'];
        }
        return post_types;
    }
}

function getSelectedMeetingTypes() {
    if ($('.breadcrumb-header').text() === 'Meeting Notes') {
        var meeting_types = [];
        $('.meeting-type-checkbox').each(function () {
            if ($(this).is(':checked')) {
                meeting_types.push($(this).val());
            }
        });
        if (meeting_types.length === 0) {
            meeting_types = ['Division', 'Strategic Planning', 'Senior Staff', 'Project', 'Agency'];
        }
        console.log(meeting_types);
        return meeting_types;
    }
    return [];
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
            'post_type': getSelectedPostTypes(),
            'posts_start': posts_start,
            'posts_end': posts_end,
            'tags': getSelectedTags()
        },
        success: function (data) {
            displayPreviousResults(data); // Render the new rows
            $(window).scrollTop(0);
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
            'post_type': getSelectedPostTypes(),
            'posts_start': posts_start,
            'posts_end': posts_end,
            'tags': getSelectedTags()
        },
        success: function (data) {
            displayNextResults(data); // Render the new rows
            $(window).scrollTop(0);
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