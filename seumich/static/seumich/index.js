$(document).ready(function() {
    $('[data-toggle="tooltip"]').tooltip();

    $('.pagination .disabled a, .pagination .active a').on('click', function(e) {
        e.preventDefault();
    });
});
