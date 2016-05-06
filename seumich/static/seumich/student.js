$(function() {
    $('div[id^=student-menu-]').on('click', function() {
        code = $(this).attr('id').split('-').pop();
        student = $('#student-username').val();
        location.href = '/students/' + student + '/class_sites/' + code + '/';

    });
});
