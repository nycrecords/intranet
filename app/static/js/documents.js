// Global variables
var increment = 10; // Change this to change how many results are shown on one page
var page_counters = {
    'instructions': {
        'start': 0,
        'end': increment
    },
    'policies_and_procedures': {
        'start': 0,
        'end': increment
    },
    'templates': {
        'start': 0,
        'end': increment
    },
    'training_materials': {
        'start': 0,
        'end': increment
    }
};

// Util functions start here
function openTab(evt, tabName) {
    /*
    Event handler to open a document type tab
     */
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName('tabcontent');
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = 'none';
    }
    tablinks = document.getElementsByClassName('tablinks');
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(' active', '');
    }
    document.getElementById(tabName).style.display = 'block';
    evt.currentTarget.className += ' active';
    $('.pagination-row').hide();
    $('#' + tabName + '-pagination').show();
}

function displayResults (data) {
    /*
    Util function to display document rows for a specific document type tab
    This is called as a result on hitting the /documents/search/ endpoint
     */
    var document_selector = $('#' + data['document_type']);
    var document_prev = $('#' + data['document_type'] + '-prev');
    var document_next = $('#' + data['document_type'] + '-next');
    var document_page_info = $('#' + data['document_type'] + '-page-info');

    document_selector.html(''); // Clear out existing html
    document_selector.html(data['documents']); // Render new document rows

    // Conditional block to determine what should be displayed on the page info part of the pagination div
    // and whether or not to show/hide the next/prev buttons
    if (data['documents_max'] === 0) {
        document_prev.hide();
        document_next.hide();
        document_page_info.html(0 + ' - ' + 0 + ' of ' + 0);
    }
    else if (data['documents_max'] <= increment) {
        document_prev.hide();
        document_next.hide();
        document_page_info.html(data['documents_start'] + ' - ' + data['documents_max'] + ' of ' + data['documents_max']);
    }
    else if (data['documents_start'] === 1) {
        document_page_info.html(data['documents_start'] + ' - ' + data['documents_end'] + ' of ' + data['documents_max']);
        document_prev.hide();
        document_next.show();
    }
    else {
        document_page_info.html(data['documents_start'] + ' - ' + data['documents_end'] + ' of ' + data['documents_max']);
        document_prev.show();
    }
}

function displayNextResults(data) {
    /*
    Util function to display document rows for a specific document type tab when next button is clicked
    This is called as a result on hitting the /documents/page/ endpoint
     */
    var document_selector = $('#' + data['document_type']);
    var document_prev = $('#' + data['document_type'] + '-prev');
    var document_next = $('#' + data['document_type'] + '-next');
    var document_page_info = $('#' + data['document_type'] + '-page-info');

    // Clear our and render new document rows
    document_selector.html('');
    document_selector.html(data['documents']);

    // Set page info and determine visibility of pagination buttons
    if (data['documents_end'] >= data['documents_max']) {
        document_page_info.html(data['documents_start'] + ' - ' + data['documents_max'] + ' of ' + data['documents_max']);
        document_next.hide();
    }
    else {
        document_page_info.html(data['documents_start'] + ' - ' + data['documents_end'] + ' of ' + data['documents_max']);
    }
    document_prev.show();
}

function displayPreviousResults(data) {
    /*
    Util function to display document rows for a specific document type tab when prev button is clicked
    This is called as a result on hitting the /documents/page/ endpoint
     */
    var document_selector = $('#' + data['document_type']);
    var document_prev = $('#' + data['document_type'] + '-prev');
    var document_next = $('#' + data['document_type'] + '-next');
    var document_page_info = $('#' + data['document_type'] + '-page-info');

    // Clear our and render new document rows
    document_selector.html('');
    document_selector.html(data['documents']);

    // Set page info and determine visibility of pagination buttons
    if (data['documents_start'] === 1) {
        document_prev.hide();
    }
    document_next.show();
    document_page_info.html(data['documents_start'] + ' - ' + data['documents_end'] + ' of ' + data['documents_max']);
}

function generatePaginationButtonHandlers (document_type_underscore, document_type_dash, document_type_plain_text) {
    /*
    Util function to event handlers for prev/next buttons of a specific document type
     */
    $('#' + document_type_dash + '-prev').click(function () {
        // decrement the page counters for that document type
        page_counters[document_type_underscore]['start'] = page_counters[document_type_underscore]['start'] - increment;
        page_counters[document_type_underscore]['end'] = page_counters[document_type_underscore]['end'] - increment;

        // AJAX call to get the previous rows that should display on the frontend
        $.ajax({
            url: '/documents/page/',
            type: 'GET',
            dataType: 'json',
            data: {
                'sort_by': $('#sort-dropdown').find('option:selected').val(),
                'search_term': $('#save-search-term').text(),
                'page_counters': JSON.stringify(page_counters),
                'document_type_plain_text': document_type_plain_text,
                'document_type_underscore': document_type_underscore,
                'document_type_dash': document_type_dash
            },
            success: function (data) {
                displayPreviousResults(data); // Render the new rows
            }
        });
    });

    $('#' + document_type_dash + '-next').click(function () {
        // increment the page counters for that document type
        page_counters[document_type_underscore]['start'] = page_counters[document_type_underscore]['start'] + increment;
        page_counters[document_type_underscore]['end'] = page_counters[document_type_underscore]['end'] + increment;

        // AJAX call to get the next rows that should display on the frontend
        $.ajax({
            url: '/documents/page/',
            type: 'GET',
            dataType: 'json',
            data: {
                'sort_by': $('#sort-dropdown').find('option:selected').val(),
                'search_term': $('#save-search-term').text(),
                'page_counters': JSON.stringify(page_counters),
                'document_type_plain_text': document_type_plain_text,
                'document_type_underscore': document_type_underscore,
                'document_type_dash': document_type_dash
            },
            success: function (data) {
                displayNextResults(data); // Render the new rows
            }
        });
    });
}
// Util functions end here

$(function () {
    // On initial page load open the selected default tab
    document.getElementById('default-open').click();

    // Generate event handlers for prev/next buttons for all document types
    generatePaginationButtonHandlers('instructions', 'instructions', 'Instructions');
    generatePaginationButtonHandlers('policies_and_procedures', 'policies-and-procedures', 'Policies and Procedures');
    generatePaginationButtonHandlers('templates', 'templates', 'Templates');
    generatePaginationButtonHandlers('training_materials', 'training-materials', 'Training Materials');

    // AJAX call for initial page load
    $.ajax({
        url: '/documents/search/',
        type: 'GET',
        dataType: 'json',
        data: {
            'sort_by': $('#sort-dropdown').find('option:selected').val(),
            'search_term': $('#save-search-term').text(),
            'page_counters': JSON.stringify(page_counters)
        },
        success: function (data) {
            // Render the rows for each document type
            displayResults(data['instructions_data']);
            displayResults(data['policies_and_procedures_data']);
            displayResults(data['templates_data']);
            displayResults(data['training_materials_data']);
        }
    });

    // Handle sort by dropdown change event
    $('#sort-dropdown').change(function() {
        // Reset page counters
        page_counters = {
            'instructions': {
                'start': 0,
                'end': increment
            },
            'policies_and_procedures': {
                'start': 0,
                'end': increment
            },
            'templates': {
                'start': 0,
                'end': increment
            },
            'training_materials': {
                'start': 0,
                'end': increment
            }
        };

        $.ajax({
            url: '/documents/search/',
            type: 'GET',
            dataType: 'json',
            data: {
                'sort_by': $('#sort-dropdown').find('option:selected').val(),
                'current_tab': $('.tablinks.active').val(),
                'search_term': $('#save-search-term').text(),
                'page_counters': JSON.stringify(page_counters),
            },
            success: function (data) {
                displayResults(data['instructions_data']);
                displayResults(data['policies_and_procedures_data']);
                displayResults(data['templates_data']);
                displayResults(data['training_materials_data']);
            }
        });
    });

    // Handler for clicking the search button which filters based on the search term
    $('.documents-search-button').click(function() {
        var search_term = $('#document-search-term').val(); // Get the current search term
        $('#document-search-term').val(''); // Reset Search By field
        // Reset page counters
        page_counters = {
            'instructions': {
                'start': 0,
                'end': increment
            },
            'policies_and_procedures': {
                'start': 0,
                'end': increment
            },
            'templates': {
                'start': 0,
                'end': increment
            },
            'training_materials': {
                'start': 0,
                'end': increment
            }
        };

        $.ajax({
            url: '/documents/search/',
            type: 'GET',
            dataType: 'json',
            data: {
                'sort_by': $('#sort-dropdown').find('option:selected').val(),
                'search_term': search_term,
                'page_counters': JSON.stringify(page_counters),
            },
            success: function (data) {
                displayResults(data['instructions_data']);
                displayResults(data['policies_and_procedures_data']);
                displayResults(data['templates_data']);
                displayResults(data['training_materials_data']);

                // Display search term
                if (search_term !== '') {
                    $('#save-search-term').html(search_term);
                    $('#display-search-term').show();
                }
                else {
                    $('#save-search-term').html('');
                    $('#display-search-term').hide();
                }

            }
        });
    });
});