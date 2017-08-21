$(function() {
	$('#submit').addClass('btn-primary pull-right login_submit_button');
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
	if ($('#csrf_token').parent().parent().hasClass('has-error')) {
		$('#account').after(format_help_block("Le nom d'utilisateur ou le mot de passe est incorrect"))
		$('#account').next().addClass('login_error_message')
	}
	$('#hidden_block').show() 
});