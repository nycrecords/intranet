// Handler for entering a search term in the header search bar
$('#header-search').click(function() {
    if ($('#global-search-bar').val() !== '') {
        window.location.replace('/news-and-updates?search_term=' + $('#global-search-bar').val());
    }
});