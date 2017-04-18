function verify_form_errors(id, class_to_verify) {
	return $('#'+id).parent().parent().hasClass(class_to_verify)
}

function is_empty(id) {
	return ($('#'+id).val() === '')
}

function show_error(id, recursion) {
	var contenu = $('#'+id).val()
	if (contenu.length === 0){
		$('#'+id).parent().parent().removeClass('has-error').removeClass('has-success')
		$('#'+id).parent().find('.wrong_password').each(function() { $(this).remove() })
		return
	} 
	function to_do(bool, message, id) {
		if (bool) {
			$('#'+id).parent().parent().removeClass('has-error').addClass('has-success');
			$('#'+id).parent().find('.wrong_password').each(function() { 
				$(this).remove() 
			})
		} else {
			$('#'+id).parent().parent().addClass('has-error');
			if (!$('#'+id).next().hasClass('wrong_password')) {
				$('#'+id).after(format_help_block(message))
			}
		}
	}
	if (id == 'new_pw'){
		to_do((/.{8,128}/.test(contenu)), 'Le mot de passe doit contenir au moins 8 caractères', id)
		if (recursion) {
			show_error('new_pw2', false)
		}
	} 
	if (id == 'new_pw2'){
		to_do((contenu === $('#new_pw').val()), 'Les mots de passes saisis ne sont pas identiques', id)
		if (recursion) {
			show_error('new_pw', false)
		}
	}
}

function get_regex(data) {
  	switch(data) {
	    case 'mod_first_name': case 'mod_last_name':
	    	return /(^$)|(^([^\!#\$%&\(\)\*,\./:;\?@\[\\\]_\{\|\}¨ˇ“”€\+<=>§°\d\s¤®™©]| )+$)/
	    case 'mod_email':
	    	return /^[a-z0-9\.-_]+\@[a-z0-9\.-_]+\.[a-z]{2,10}$/i
	    case 'mod_sigle':
	    	return /^[a-zA-Z]{4}$/
	}
}

function verify(id) {
	var input_form = $('#'+id).parent().parent()

	if ($('#'+id).val().length === 0) {
		input_form.removeClass('has-success').removeClass('has-error')
		return false
	}
	if (get_regex(id).test($('#'+id).val())) {
		input_form.removeClass('has-error').addClass('has-success')
		return true
	} // else
	input_form.removeClass('has-success').addClass('has-error')
	return false
}

$('#mod_profil_button').click(function() {
	var data_to_modify = ['first_name', 'last_name', 'email', 'sigle']

	for (var i = 0; i < data_to_modify.length; i++) {
		if (!verify('mod_'+data_to_modify[i])) {
			return
		}
	}
	var post_data = { 
		id: $('#user_id').html()
	}
    for (var i = 0; i < data_to_modify.length; i++) {
        post_data[data_to_modify[i]] = $('#mod_'+data_to_modify[i]).val()
    }
    $.ajax({
        url: "user",
        type: "PATCH",
        data: post_data,
    })
    .done(function(data, textStatus, jqXHR) {
        if (data === 'success') {
            $('#myModal').modal('hide');
            for (var i = 0; i < data_to_modify.length; i++) {
            	$('#'+data_to_modify[i]).html($('#mod_'+data_to_modify[i]).val())
            }
            $('#mod_password_message').addClass('hidden')
            $('#mod_profil_message').removeClass('hidden')
        }
    })
    .fail(function(jqXHR, textStatus, errorThrown) {
        alert('une erreur est survenue:' + JSON.stringify(jqXHR))
    })
})

$(function() {
	if (!/\?/.test(window.location.href)) {
		$('.required').each(function() {
			$('label', this).addClass('col-sm-3 label_login'); 
			$('input', this).wrap('<div class="col-sm-9 input_login"></div>');
			$(this).wrap('<div class="row"></div>');
		});
		
		$('#modify').addClass('btn-primary pull-right');
		$("#modify").click(function(e) {
			if (verify_form_errors('new_pw', 'has-error') || 
			verify_form_errors('new_pw2', 'has-error')) {
				e.preventDefault();
			}
			if (is_empty('old_pw') || is_empty('new_pw') || is_empty('new_pw2')) {
				e.preventDefault();
			}
		}); 

		document.getElementById('old_pw').setAttribute('onkeyup', 'show_error("old_pw", true);');
		document.getElementById('new_pw').setAttribute('onkeyup', 'show_error("new_pw", true);');
		document.getElementById('new_pw2').setAttribute('onkeyup', 'show_error("new_pw2", true);');

		$('#modify_password_block').removeClass('hidden')

		if ($('#mod_password_message').length) {
			$('#profil_alerts').append($('#mod_password_message').parent().html())
		}
		if ($('#wrong_actual_password').length) {
			$('#old_pw').parent().parent().addClass('has-error');
			$('#old_pw').after(format_help_block('Le mot de passe est incorrect'))
		}
		$('#profil_alerts .mod_password_alert').removeClass('hidden')

		if ($('#last_new_password').length) {
			$('#new_pw').val($('#last_new_password').html())
			$('#new_pw2').val($('#last_new_password').html())
			show_error('new_pw', true)
		}
	}
});