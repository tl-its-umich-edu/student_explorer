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

});
