$(function() {

    var reset = function() {
        $('#processing-text, #importing-text, .alert, table, #confirm-button, #back-button, #undo-button').hide();
    };

    $('form').submit(function(event) {
        event.preventDefault();

        reset();
        $('select[id^=options]').empty();
        $('#processing-text').show();

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

                    $('#confirm-button, #back-button').show();

                    $('select[id^=options]').change(function() {
                        var myid = $(this).attr('id');
                        var selected = myid.split('options')[1];
                        var selectedCol = $(this).val();

                        $("#col2row" + selected).html(dataDict[selectedCol]);

                        var tab = $("#col3row" + selected).html();
                        var col = $("#col4row" + selected).html();
                        dataTable[tab + col] = selectedCol;
                    });
                } else if (data['completed'] === 'Fail') {
                    $('#alert-import-danger').show();
                }

                $('.container-fluid').off('click', 'button:contains("Confirm")').on('click', 'button:contains("Confirm")', function() {
                    $('#processing-text, .alert, #confirm-button, #undo-button, #back-button').hide();
                    $('#importing-text').show();

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
                                $('#alert-import-success, #back-button, #undo-button').show();
                            } else if (response['completed'] === 'Fail') {
                                $('#importing-text').hide();
                                $('#alert-import-danger, #back-button').show();
                            }

                            $('.container-fluid').off('click', 'button:contains("Undo")').on('click', 'button:contains("Undo")', function() {
                                $('.alert, #confirm-button, #back-button, #undo-button').hide();
                                $('#processing-text').show();

                                $.ajax({
                                        method: 'POST',
                                        url: '/advising_groups/undo/',
                                        beforeSend: function(xhr, settings) {
                                            xhr.setRequestHeader("X-CSRFToken", csrftoken);
                                        },
                                        data: {
                                            id: response['current_id']
                                        },
                                    })
                                    .done(function(resp) {
                                        reset();
                                        if (resp['completed'] === 'Success') {
                                            $('form, #alert-undo-success').show();
                                        } else if (resp['completed'] === 'Fail') {
                                            $('form, #alert-undo-danger').show();
                                        }
                                    });

                            });
                        });
                });

                $('.container-fluid').off('click', 'button:contains("Back")').on('click', 'button:contains("Back")', function() {
                    reset();
                    $('form').show();
                });
            });
    });

});
