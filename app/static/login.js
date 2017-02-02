$(function() {
  $('#submit').addClass('btn-primary pull-right');
  $('#remember_me').parent().css('color', 'black');
  if ($('.help-block').first().text() === 'This field is required.') {
      $('.help-block').each(function(){
          $(this).text('Ce champs est requis.');
      });
  }
});