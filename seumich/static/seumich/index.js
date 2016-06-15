$(document).ready(function() {
    // Handle old URLs based on hash fragment routing
    var hash = window.location.hash;
    if (hash.length > 0) {
      var url = hash.substring(1);
      console.log("Hash fragmnet found, redirecting to: " + url);
      window.location = url;

    }

    $('[data-toggle="tooltip"]').tooltip();

    $('.pagination .disabled a, .pagination .active a').on('click', function(e) {
        e.preventDefault();
    });

    var changeFeedback = function() {
        $('.feedback').css('position', 'absolute');
        $('.feedback').css('margin', '0 auto');
        // check if a scroll bar is present
        if ($(document).height() > $(window).height()) {
            // if scroll, feedback link should be placed absolutely
            // relative to the body
            $('body').css('position', 'relative');
            // if scroll and window width less than 736, reset feedback
            // position to default
            if ($(window).width() <= 736) {
                $('.feedback').css('position', 'static');
                $('.feedback').css('margin-top', '20px');
                $('.feedback').css('margin-bottom', '-25px');
            }
        } else {
            // if no scroll, feedback link should be placed absolutely
            // relative to page  (as height: auto for body)
            $('body').css('position', 'static');
            // if no scroll and window width less than 736, set navbar
            // to fixed as i want it to be at bottom of screen
            if ($(window).width() <= 736) {
                $('.navbar-fixed-bottom').css('position', 'fixed');
            }
        }
    };

    changeFeedback();

    $(window).resize(function() {
        changeFeedback();
    });

});
