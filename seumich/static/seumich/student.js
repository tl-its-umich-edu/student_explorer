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
});
