$(document).ready(function() {
    $('[data-toggle="tooltip"]').tooltip();

    var winWidth = 0; /* Window width */
    setContainerDims();

    function setContainerDims() {
        winWidth = parseInt($(window).width());

        $(".student-detail-main-menu").css({
            "width": winWidth,
        });
    }

    $(window).resize(function() {
        setContainerDims();
    })
});
