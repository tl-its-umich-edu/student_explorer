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

                if (data['completed'] === 'Success') {
                    $('table').show();

                    var dataDict = data['excel_data'];
                    var colOrder = data['cols_order']

                    var select_list = []

                    select_list.push("#options1");
                    select_list.push("#options2");
                    select_list.push("#options3");
                    select_list.push("#options4");

                    $.each(select_list, function(index, options) {
                        var selected = options.split('#options')[1];
                        $("#col2row" + selected).html(dataDict[colOrder[selected - 1]]);

                        $.each(Object.keys(dataDict), function(index, value) {
                            if (value == colOrder[selected - 1]) {
                                $(options).append("<option selected>" + value + "</option>");
                            } else {
                                $(options).append("<option>" + value + "</option>");
                            }

                        });

                    });

                    $('select').change(function() {
                        var myid = $(this).attr('id');
                        var selected = myid.split('options')[1];
                        $("#col2row" + selected).html(dataDict[$(this).val()]);
                    });

                    $('<button type="button" class="btn btn-info pull-right">Confirm</button>').insertAfter('.text-primary');

                } else if (data['completed'] === 'Error') {
                    $('#alert-danger').show();
                }
            }
        });

        $('body').on('click', 'button:contains("Confirm")', function() {
            var myTableArray = [];

            $("table tr").each(function() {
                var arrayOfThisRow = [];
                var tableData = $(this).find('td');
                tableData[0] = $(this).find('select');
                if (tableData.length > 0) {
                    tableData.each(function() {
                        arrayOfThisRow.push($(this).text());
                    });
                    arrayOfThisRow[0] = tableData[0].val();
                    myTableArray.push(arrayOfThisRow);
                }
            });

            $.ajax({
                method: 'GET',
                url: '/advising_groups/',
                data: {
                    tabledata: JSON.stringify(myTableArray)
                },
                success: function(d) {}
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

});
