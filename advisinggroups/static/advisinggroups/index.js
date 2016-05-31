$(function() {

    $('#upload-file').on('click', function() {
        event.preventDefault();
        $('#open-dialog').click();
    });

    $('#open-dialog').change(function() {
        $('#id_input_file').val($(this).val());
    });

    $('form').submit(function(event) {
        event.preventDefault();

        $('#processing-text').show();
        $('.alert').hide();
        $('table').hide();
        $('#confirm-button').remove();
        $('#back-button').remove();
        $('select[id^=options]').empty();

        var formData = new FormData($(this)[0]);
        var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();

        $.ajax({
                method: 'POST',
                url: '/advising_groups/',
                beforeSend: function(xhr, settings) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                },
                data: formData,
                processData: false,
                contentType: false,
            })
            .done(function(data) {

                $('#processing-text').hide();

                if (data['completed'] === 'Success') {

                    $('form').hide();
                    $('table').show();

                    var dataDict = data['excel_data'];
                    var colOrder = data['cols_order']
                    var select_list = $('select[id^=options]');
                    var dataTable = {}

                    $.each(select_list, function(index, options) {
                        var myid = $(this).attr('id');
                        var selected = myid.split('options')[1];
                        var selectedCol = colOrder[selected - 1]

                        $("#col2row" + selected).html(dataDict[selectedCol]);

                        var tab = $("#col3row" + selected).html();
                        var col = $("#col4row" + selected).html();
                        dataTable[tab + col] = selectedCol;

                        $.each(Object.keys(dataDict), function(index, value) {
                            if (value == selectedCol) {
                                $(options).append("<option selected>" + value + "</option>");
                            } else {
                                $(options).append("<option>" + value + "</option>");
                            }
                        });
                    });

                    $('<button type="button" class="btn btn-warning pull-left" id="back-button">Back</button>').insertBefore('table');
                    $('<button type="button" class="btn btn-info pull-right" id="confirm-button">Confirm</button>').insertBefore('table');
                } else if (data['completed'] === 'Fail') {
                    $('#alert-danger').show();
                }

                $('select[id^=options]').change(function() {
                    var myid = $(this).attr('id');
                    var selected = myid.split('options')[1];
                    var selectedCol = $(this).val();

                    $("#col2row" + selected).html(dataDict[selectedCol]);

                    var tab = $("#col3row" + selected).html();
                    var col = $("#col4row" + selected).html();
                    dataTable[tab + col] = selectedCol;
                });

                $('body').on('click', 'button:contains("Confirm")', function() {

                    $('#processing-text').hide();
                    $('#importing-text').show();
                    $('.alert').hide();
                    $('#confirm-button').remove();
                    $('#back-button').hide();

                    $.ajax({
                            method: 'POST',
                            url: '/advising_groups/confirm/',
                            beforeSend: function(xhr, settings) {
                                xhr.setRequestHeader("X-CSRFToken", csrftoken);
                            },
                            data: {
                                tabledata: JSON.stringify(dataTable)
                            },
                        })
                        .done(function(response) {
                            if (response['completed'] === 'Success') {
                                $('#importing-text').hide();
                                $('#alert-success').show();
                                $('#back-button').show();
                            } else if (response['completed'] === 'Fail') {
                                $('#importing-text').hide();
                                $('#alert-danger').show();
                                $('#back-button').show();
                            }
                        });
                });

                $('body').on('click', 'button:contains("Back")', function() {
                    $('form').show();
                    $('table').hide();
                    $('#confirm-button').remove();
                    $('#back-button').remove();
                });
            });
    });

    $('#clear_text').on('click', function() {
        $('#processing-text').hide();
        $('#importing-text').hide();
        $('table').hide();
        $('.alert').hide();
        $('#id_input_file').val('');
        $('#open-dialog').val('');
        $('#confirm-button').remove();
        $('#back-button').remove();
    });

});
