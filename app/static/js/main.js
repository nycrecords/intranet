$(document).ready(function () {
    ////////////////////////////////////////
    // Mutation observer - watch for RTL
    ////////////////////////////////////////

    var target = document.querySelector('html');

    var observer = new MutationObserver(function (mutations) {
        mutations.forEach(function () {
            var classes = target.getAttribute('class');
            var single_class = 'translated-rtl';
            if (classes.includes(single_class)) {
                target.setAttribute('dir', 'rtl');
            } else {
                target.setAttribute('dir', 'ltr');
            }
        });
    });

    var config = {
        attributes: true,
        attributeFilter: ['class']
    }

    observer.observe(target, config);

    ////////////////////////////////////////
    // Language, Search, and Menu Toggle
    ////////////////////////////////////////

    // Prevent collapse from closing when clicking inside
    $('#global-search, #global-language').on('click', function (e) {
        e.stopPropagation();
    });

    // Keep the dropdowns open when clicking inside them
    $('.collapse').on('click', function (e) {
        e.stopPropagation();
    });

    $('#global-language').on('show.bs.collapse', function (e) {
        e.stopPropagation();
        $('#global-search').collapse('hide');
        $('#nav-primary').collapse('hide');
    });

    $('#global-search').on('show.bs.collapse', function (e) {
        e.stopPropagation();
        $('#global-language').collapse('hide');
        $('#nav-primary').collapse('hide');
    });

    $('#nav-primary').on('show.bs.collapse', function (e) {
        e.stopPropagation();
        $('#global-search').collapse('hide');
        $('#global-language').collapse('hide');
    });

    $(document).ready(function() {
        // Explicitly initialize dropdowns
        $('.dropdown-toggle').dropdown();
    
        // Prevent dropdown from closing when clicking inside
        $('.dropdown-menu').on('click', function(e) {
            e.stopPropagation();
        });
    });

    ////////////////////////////////////////
    // Language and Search Toggle Focus
    ////////////////////////////////////////

    $('#global-language').on('shown.bs.collapse', function () {
        $('.goog-te-combo').focus();
    }).on('show.bs.collapse', function () {
        $('.goog-te-combo').blur();
    });

    $('#global-search').on('shown.bs.collapse', function () {
        document.getElementById('global-search-bar').focus();
    }).on('show.bs.collapse', function () {
        document.getElementById('global-search-bar').blur();
    });

    // Close dropdowns when clicking outside
    $(document).on('click', function (e) {
        if (!$(e.target).closest('.collapse').length &&
            !$(e.target).closest('.no-btn-style').length) {
            $('.collapse').collapse('hide');
        }
    });

    ////////////////////////////////////////
    // Back to top
    ////////////////////////////////////////

    var scroll_speed = 800;

    if ($('#back-to-top').length) {
        $('#back-to-top > a').click(function () {
            $('body, html').animate({
                scrollTop: 0
            }, scroll_speed);
        });

        $(window).scroll(function () {
            var window_scroll = $(document).scrollTop();
            var primary_content = $('#primary-content').offset().top;

            if (window_scroll > primary_content) {
                $('#back-to-top').addClass('show');
            } else {
                $('#back-to-top').removeClass('show');
            }
        }).scroll();
    }
});

////////////////////////////////////////
// Google Translate Links
////////////////////////////////////////

$(document).ready(function() {
    $('.lang-select').click(function (e) {
        e.preventDefault();
        var lang = $(this).attr('data-lang')
        setLanguage(lang);
    });
});

function setLanguage(theLang) {
    var theSelect = $('.goog-te-combo');
    var db = theSelect.get(0);
    theSelect.val(theLang);
    fireEvent(db, 'change');
}

function fireEvent(element, event) {
    if (document.createEventObject) {
        var evt = document.createEventObject();
        return element.fireEvent('on' + event, evt)
    } else {
        var evt = document.createEvent("HTMLEvents");
        evt.initEvent(event, false, true);
        return !element.dispatchEvent(evt);
    }
}