// Handler for entering a search term in the header search bar
$('#header-search').click(function() {
    if ($('#search-bar').val() !== '') {
        window.location.href = '/news-updates?search_term=' + $('#search-bar').val();
    }
});