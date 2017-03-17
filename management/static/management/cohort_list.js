$(function() {


    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    function getQueryVariable(name, url) {
        name = name.replace(/[\[\]]/g, "\\$&");
        var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
            results = regex.exec(url);
        if (!results) return null;
        if (!results[2]) return '';
        return decodeURIComponent(results[2].replace(/\+/g, " "));
    }

    var cohortListUrl = $('#resultsTable').data('url');

    var ajaxFilter = function(data) {
        $.ajax({
            url: cohortListUrl,
            datatype: 'html',
            method: "POST",
            data: data,
            success: function(data) {
                $('#resultsTable').html($('#resultsTable', $(data)).html());
            },
            error: function(data) {
                console.log('Sorry! There was an error.');
            }
        });

    }

    $('#allCohorts').change(function() {
        var data = {};
        if ($(this).is(":checked")) {
            data['checked'] = 'all';
            ajaxFilter(data);
            return;
        }
        data['checked'] = 'active';
        ajaxFilter(data);
    });

    $('#resultsTable').on("click", 'button.submit', function(event) {
        event.preventDefault();
        var code = $(this).attr('id');
        var action = $(this).data("action");
        $.ajax({
            method: 'POST',
            url: cohortListUrl,
            data: {
                code: code,
                action: action
            },
            success: function(data) {
                location.reload();
            },
            error: function(XMLHttpRequest, textStatus, errorThrown) {
                alert("Sorry! There was an error.");

            }
        });

    });

    $('#resultsTable').on("click", 'a.page-link', function(event) {
        event.preventDefault();
        var query = $(this).attr('href');
        var page = getQueryVariable('page', query);
        var data = {
            'page': page
        };
        if ($('#allCohorts').is(":checked")) {
            data['checked'] = 'all';
        } else {
            data['checked'] = 'active';
        }
        $.ajax({
            url: cohortListUrl + '' + $(this).attr('href'),
            datatype: 'html',
            method: 'POST',
            data: data,
            success: function(data) {
                $('#resultsTable').html($('#resultsTable', $(data)).html());
            },
            error: function(data) {
                console.log('Sorry! There was an error.');
            }
        });
    });

});
