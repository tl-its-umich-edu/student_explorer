$(function() {
    $('[data-toggle="tooltip"]').tooltip();
    $('#open-dialog').hide();
    $('#alert-success').hide();
    $('#alert-danger').hide();
    $('img').hide();

    $('#upload-file').on('click', function() {
        event.preventDefault();
        $('#open-dialog').click();
    });

    $('#open-dialog').change(function() {
        $('#id_input_file').val($(this).val());
    });

    $('form').submit(function(event) {
        event.preventDefault();

        $('img').show();
        $('#alert-danger').hide();
        $('#alert-success').hide();

        var formData = new FormData($(this)[0]);
        var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();

        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        });

        $.ajax({
            method: 'POST',
            url: '/advising_groups/',
            data: formData,
            processData: false,
            contentType: false,
            success: function(data) {
                $('img').hide();
                if (data['completed'] === 'Done') {
                    $('#alert-success').show();
                } else if (data['completed'] === 'Error') {
                    $('#alert-danger').show();
                }
            }
        });
    });

    $('#clear_text').on('click', function() {
        $('img').hide();
        $('#alert-success').hide();
        $('#alert-danger').hide();
        $('#id_input_file').val('');
        $('#open-dialog').val('');
    });
});
