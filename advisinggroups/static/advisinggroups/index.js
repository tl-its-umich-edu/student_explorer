$(function() {
    $('[data-toggle="tooltip"]').tooltip();

    $('#upload-file').on('click', function() {
        event.preventDefault();
        $('#open-dialog').click();
    });

    $('#open-dialog').change(function() {
        $('#id_input_file').val($(this).val());
    });
});
