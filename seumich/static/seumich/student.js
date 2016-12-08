$(function() {

    var currentClassCode;

    currentClassCode = $('#current-classsite-code').val();
    $('div[id^=student-menu-' + currentClassCode + ']').css('background-color', '#CCCCCC');

});
