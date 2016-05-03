$(function () {

  var csrfSafeMethod;

  csrfSafeMethod = function (method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  };

  var csrfToken, urlPath;
  csrfToken = $('#csrfmiddlewaretoken').val();
  advisor = $('#selected-advisor').val();
  urlPath = '/students/';

  $.ajax({
    method: 'GET',
    url: urlPath,
    data: {'advisor': advisor},
    beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrfToken);
          }
        },
    success: function (data) {
      $('#load-advisor-detail').html(data);

    }
  });
});
