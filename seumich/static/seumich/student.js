$(function() {

    var currentClassCode;

    currentClassCode = $('#current-classsite-code').val();
    $('div[id^=student-menu-' + currentClassCode + ']').css('background-color', '#CCCCCC');

    $('div[id^=student-menu-]').on('click', function() {
        code = $(this).attr('id');
        code = code.split('student-menu-')[1];
        student = $('#student-username').val();
        location.href = '/students/' + student + '/class_sites/' + code + '/';

    });

    var winWidth = 0; /* Window width */
    setContainerDims();

    function setContainerDims() {
        winWidth = parseInt($(window).width());

        if (winWidth <= 768) {
            $(".student-detail-left-menu").css({
                "width": winWidth,
            });
        } else {
            $(".student-detail-left-menu").css({
                "width": "25%",
            });
        }
    }

    $(window).resize(function() {
        setContainerDims();
    })
});
