$(function() {

    $('img[id^=plus-button-]').show();
    $('img[id^=minus-button-]').hide();
    $('p[id^=assignment-grader-comment-]').hide();


    $('img[id^=plus-button-]').on('click', function() {
        var imgId;

        imgId = $(this).attr('id').split('-').pop();
        // hide plus button
        $(this).hide();
        // show grader comment
        $('#assignment-grader-comment-' + imgId).show();
        // change text of comment title
        $('#comment-title-' + imgId).text('Hide Comment');
        // show minus button
        $('#minus-button-' + imgId).show();
    })

    $('img[id^=minus-button-]').on('click', function() {
        var imgId;

        imgId = $(this).attr('id').split('-').pop();
        // hide minus button
        $(this).hide();
        // hide grader comment
        $('#assignment-grader-comment-' + imgId).hide();
        // change text of comment title
        $('#comment-title-' + imgId).text('View Comment');
        // show plus button
        $('#plus-button-' + imgId).show();
    })


});
