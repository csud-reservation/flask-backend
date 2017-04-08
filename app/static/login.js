$(function() {
  $('#submit').addClass('btn-primary pull-right');
  $('#remember_me').parent().parent().addClass('rm_checkbox')
  .wrap('<div class="row"></div>');
  $('#remember_me').parent().css('color', 'black')
  .wrap('<div class="col-sm-9"></div>').parent()
  .before('<div class="col-sm-3"></div>');
  
  $('.help-block').each(function(){
    $(this).hide();
  });
  
  $('.required').each(function() {
    $('label', this).addClass('col-sm-3 label_login'); 
    $('input', this).wrap('<div class="col-sm-9 input_login"></div>');
    $(this).wrap('<div class="row"></div>');
  });
  $('#hidden_block').show() 
});