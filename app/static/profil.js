function verify_form_errors(id, class_to_verify) {
  return $('#'+id).parent().parent().hasClass(class_to_verify)
}

function is_empty(id) {
  return ($('#'+id).val() === '')
}

$(function() {
  $('#modify').addClass('btn-primary pull-right');

  $('.help-block').each(function(){
    //$(this).hide();
    return;
  });
  
  $('.required').each(function() {
    $('label', this).addClass('col-sm-3 label_login'); 
    $('input', this).wrap('<div class="col-sm-9 input_login"></div>');
    $(this).wrap('<div class="row"></div>');
  });
  
  $("#modify").click(function(e) {
    if (verify_form_errors('old_pw', 'has-error') || 
    verify_form_errors('new_pw', 'has-error') || 
    verify_form_errors('new_pw2', 'has-error')) {
      e.preventDefault();
    }
    if (is_empty('old_pw') || is_empty('new_pw') || is_empty('new_pw2')) {
      e.preventDefault();
    }
  });
  
});

function afficher_erreur(id) {
  $(function() {
    if (id == 'old_pw'){
      var contenu = $('#'+id).val();
      if (/.{8,128}/.test(contenu)) {
        $('#'+id).parent().parent().removeClass('has-error').addClass('has-success');
      } else {
        $('#'+id).parent().parent().addClass('has-error');
      }
    }
    if (id == 'new_pw'){
      var contenu = $('#'+id).val();
      if (/.{8,128}/.test(contenu)) {
        $('#'+id).parent().parent().removeClass('has-error').addClass('has-success');
      } else {
        $('#'+id).parent().parent().addClass('has-error');
      }
    }
    if (id == 'new_pw2'){
      if ($('#new_pw2').val() === $('#new_pw').val()) {
        $('#'+id).parent().parent().removeClass('has-error').addClass('has-success');
      } else {
        $('#'+id).parent().parent().addClass('has-error');
      }
    }
  })
}

$(function() {
  var old_password = document.getElementById('old_pw');
  var new_password = document.getElementById('new_pw');
  var password_confirmation = document.getElementById('new_pw2');
  old_password.setAttribute('onKeyUp', 'afficher_erreur("old_pw");');
  new_password.setAttribute('onKeyUp', 'afficher_erreur("new_pw");');
  password_confirmation.setAttribute('onKeyUp', 'afficher_erreur("new_pw2");');
});