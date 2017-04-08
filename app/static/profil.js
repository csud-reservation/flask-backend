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

function show_error(id, recursion) {
  $(function() {
    var contenu = $('#'+id).val()
    if (contenu.length === 0){
      $('#'+id).parent().parent().removeClass('has-error').removeClass('has-error').removeClass('has-success')
      return
    }
    if (id == 'new_pw'){
      if (/.{8,128}/.test(contenu)) {
        $('#'+id).parent().parent().removeClass('has-error').addClass('has-success');
      } else {
        $('#'+id).parent().parent().addClass('has-error');
      }
      if (recursion) {
        show_error('new_pw2', false)
      }
    }
    if (id == 'new_pw2'){
      if (
        (contenu === $('#new_pw').val()) 
        && (contenu.length !== 0) 
        && (/.{8,128}/.test(contenu))
      ) {
        $('#'+id).parent().parent().removeClass('has-error').addClass('has-success');
      } else {
        $('#'+id).parent().parent().addClass('has-error');
      }
      if (recursion) {
        show_error('new_pw', false)
      }
    }
  })
}

$(function() {
  var old_password = document.getElementById('old_pw');
  var new_password = document.getElementById('new_pw');
  var password_confirmation = document.getElementById('new_pw2');
  old_password.setAttribute('onKeyUp', 'show_error("old_pw", true);');
  new_password.setAttribute('onKeyUp', 'show_error("new_pw", true);');
  password_confirmation.setAttribute('onKeyUp', 'show_error("new_pw2");');
  $('#hidden_block').show() 
});