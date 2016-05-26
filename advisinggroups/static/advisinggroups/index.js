$(function() {
    $('[data-toggle="tooltip"]').tooltip();
    $('#open-dialog').hide();
    $('#alert-success').hide();
    $('#alert-danger').hide();
    $('.text-primary').hide();
    $('table').hide();

    $('#upload-file').on('click', function() {
        event.preventDefault();
        $('#open-dialog').click();
    });

    $('#open-dialog').change(function() {
        $('#id_input_file').val($(this).val());
    });

    $('form').submit(function(event) {
        event.preventDefault();

        $('.text-primary').show();
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
                $('.text-primary').hide();
                $('table').hide();
                if (data['completed'] === 'Done') {
                    $('table').show();
                    if (data['heading_row'].length > 0) {
                        $('#col1row1').html("<p>" + data['heading_row'][0] + " (ex: " + data['data_row'][0] + ")</p>");
                        $('#col1row2').html("<p>" + data['heading_row'][1] + " (ex: " + data['data_row'][1] + ")</p>");
                        $('#col1row3').html("<p>" + data['heading_row'][2] + " (ex: " + data['data_row'][2] + ")</p>");
                        $('#col1row4').html("<p>" + data['heading_row'][3] + " (ex: " + data['data_row'][3] + ")</p>");
                    } else {
                        $('#col1row1').html(data['data_row'][0]);
                        $('#col1row2').html(data['data_row'][1]);
                        $('#col1row3').html(data['data_row'][2]);
                        $('#col1row4').html(data['data_row'][3]);
                    }
                    $('<button type="button" class="btn btn-info pull-right">Confirm</button>').insertAfter('.text-primary');

                } else if (data['completed'] === 'Error') {
                    $('#alert-danger').show();
                }
            }
        });

        $('body').on('click', 'button:contains("Confirm")', function() {
            $.ajax({
                method: 'GET',
                url: '/advising_groups/',
                data: formData,
                success: function(data) {
                    $('.text-primary').hide();
                    $('table').hide();
                    if (data['completed'] === 'Done') {
                        $('table').show();
                        if (data['heading_row'].length > 0) {
                            $('#col1row1').html("<p>" + data['heading_row'][0] + " (ex: " + data['data_row'][0] + ")</p>");
                            $('#col1row2').html("<p>" + data['heading_row'][1] + " (ex: " + data['data_row'][1] + ")</p>");
                            $('#col1row3').html("<p>" + data['heading_row'][2] + " (ex: " + data['data_row'][2] + ")</p>");
                            $('#col1row4').html("<p>" + data['heading_row'][3] + " (ex: " + data['data_row'][3] + ")</p>");
                        } else {
                            $('#col1row1').html(data['data_row'][0]);
                            $('#col1row2').html(data['data_row'][1]);
                            $('#col1row3').html(data['data_row'][2]);
                            $('#col1row4').html(data['data_row'][3]);
                        }
                        $('<button type="button" class="btn btn-info pull-right">Confirm</button>').insertAfter('.text-primary');

                    } else if (data['completed'] === 'Error') {
                        $('#alert-danger').show();
                    }
                }
            });
        });
    });

    $('#clear_text').on('click', function() {
        $('.text-primary').hide();
        $('table').hide();
        $('#alert-success').hide();
        $('#alert-danger').hide();
        $('#id_input_file').val('');
        $('#open-dialog').val('');
    });

    $(".up,.down").click(function() {
        var row = $(this).parents("tr:first");
        if ($(this).is(".up")) {
            var currentTr = row.children(':first');
            var previousTr = row.prev().children(':first');
            var temp = currentTr.contents();
            currentTr.append(previousTr.contents());
            previousTr.append(temp);
        } else {
            var currentTr = row.children(':first');
            var previousTr = row.next().children(':first');
            var temp = currentTr.contents();
            currentTr.append(previousTr.contents());
            previousTr.append(temp);
        }
    });

});
