$(function() {

    var currentClassCode;

    currentClassCode = $('#current-classsite-code').val();
    $('div[id^=student-menu-' + currentClassCode + ']').css('background-color', '#CCCCCC');

    $('div[id^=student-menu-], div[id^=student-list-]').on('click', function() {
        code = $(this).attr('id').split('-').pop();
        student = $('#student-username').val();
        location.href = '/students/' + student + '/class_sites/' + code + '/';

    });
});
