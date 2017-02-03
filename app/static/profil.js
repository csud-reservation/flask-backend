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
  
});