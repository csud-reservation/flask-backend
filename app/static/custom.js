function login() {
  $(function(){
    if ($('#login_utilisateur').val() && $('#login_password').val()) {
      $.ajax({
          url: "login?" + $.param({
              "user": $('#login_utilisateur').val(),
              "password": $('#login_password').val(),
          }),
          type: "POST",
      })
      .done(function(data, textStatus, jqXHR) {
          alert(data);
      })
      .fail(function(jqXHR, textStatus, errorThrown) {
          return;
      })
    }
  });
}

function verifier_enter(event, form, callback) {
  // fonction tirée de  http://stackoverflow.com/questions/14251676/
  var code = (event.keyCode ? event.keyCode : event.which);
  if(code === 13) {
    callback();
  }
}