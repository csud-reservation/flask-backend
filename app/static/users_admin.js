function hide_alerts() {
    $('#mod_profil_message, #new_user_message, #delete_user_message, #reset_password_message').addClass('hidden')
}

$('.new_user_button').click(function() {
    $('#new_user_modal').modal()
})

function restrip_table() {
    $('#users_table').removeClass('table-striped')
    
    $("tr:not(.hidden_row)").each(function (index) {
        $(this).toggleClass("stripe", !!(index & 1));
    });
}

function search_engine() {
    var search_input = $('#search_input').val()
    var regex = new RegExp(search_input, 'i');
    
    $('.user_row').each(function() {
        var first_name = $(this).find('.first_name').first().text()
        var last_name = $(this).find('.last_name').first().text()
        
        var search_matches = false
        if (regex.test(first_name+' '+last_name) || regex.test(last_name+' '+first_name)) {
            search_matches = true
        }
        if (search_matches) {
            $(this).removeClass('hidden_row')
        } else {
            $(this).addClass('hidden_row')
        }
    })
    restrip_table()
}

function assign_info_buttons() {
    $('.infos_button').click(function() {
        var user_id = $(this).parent().attr('id')
        $('#user_id').html(user_id)
        
        var to_mod = ['first_name', 'last_name', 'email', 'sigle']
        for (var i = 0; i < to_mod.length; i++) {
            $('#mod_'+to_mod[i]).val($('.'+user_id+'_'+to_mod[i]).text())
        }
        $('#mod_sigle').val($('#mod_sigle').val().replace(/\ /g, ''))
        $('#mod_email').val($('#mod_email').val().replace(/\ /g, ''))
        $('#mod_role').val($('.'+user_id+'_role').attr('class').slice(-1))
        $('#myModal').modal()
    })   
}
assign_info_buttons()

$('#mod_user_button').click(function() {
	var data_to_modify = ['first_name', 'last_name', 'email', 'sigle', 'role']

	for (var i = 0; i < data_to_modify.length; i++) {
	    if (data_to_modify[i] != 'role') {
	        if (!verify('mod_'+data_to_modify[i])) {
			    return
		    }
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
            for (var i = 0; i < data_to_modify.length; i++) {
                var modified_value = post_data[data_to_modify[i]]
                if (data_to_modify[i] == 'role') {
                    var modified_value = $("#mod_role option[value='"+modified_value+"']").text()
                } else if (data_to_modify[i] == 'sigle') {
                    modified_value = modified_value.toUpperCase()
                    modified_value = '<a href="user?sigle='+modified_value+'">'+modified_value+'</a>'
                } else if (data_to_modify[i] == 'email') {
                    modified_value = '<a href="mailto:'+modified_value+'">'+modified_value+'</a>'
                }
                $('.'+$('#user_id').html()+'_'+data_to_modify[i]).html(modified_value)
            }
            $('#mod_profil_message').html('Le profil de <strong>'+post_data['first_name'] + ' ' + post_data['last_name']+'</strong> a bien été modifié')
            hide_alerts()
            $('#mod_profil_message').removeClass('hidden')
            
            $('#myModal').modal('hide');
        }
        else {
            alert(data)
        }
    })
    .fail(function(jqXHR, textStatus, errorThrown) {
        alert('une erreur est survenue:' + JSON.stringify(jqXHR))
    })
})

$('#new_user_button').click(function() {
	var data_to_add = ['first_name', 'last_name', 'email', 'sigle', 'role']

	for (var i = 0; i < data_to_add.length; i++) {
	    if (data_to_add[i] != 'role') {
	        if (!verify('new_'+data_to_add[i])) {
			    return
		    }
	    } 
	}
	var post_data = {}
    for (var i = 0; i < data_to_add.length; i++) {
        post_data[data_to_add[i]] = $('#new_'+data_to_add[i]).val()
    }
    $.ajax({
        url: "user",
        type: "PUT",
        data: post_data,
    })
    .done(function(data, textStatus, jqXHR) {
        if (data !== 'operation interdite') {
            
            $.ajax({url: "last_user", type: "GET"}).done(function(data2, textStatus2, jqXHR2) {
                $('#first_row').after(data2)
                assign_info_buttons()
                search_engine()
                
                $('#new_user_message').html('Le nouvel utilisateur <strong>'
                +post_data['first_name']+' '+post_data['last_name']+'</strong> '
                +'a été créé avec le mot de passe suivant : <strong>'+data+'</strong>')
                
                hide_alerts()
                $('#new_user_message').removeClass('hidden')
                
                $('#new_user_modal').modal('hide')
                
                for (var i = 0; i < data_to_add.length-1; i++) {
                    $('#new_'+data_to_add[i]).val('')
                }
            })
        }
        else {
            alert(data)
        }
    })
    .fail(function(jqXHR, textStatus, errorThrown) {
        alert('une erreur est survenue:' + JSON.stringify(jqXHR))
    })
})

$('#delete_user_button').click(function() {
    var first_name = $('#mod_first_name').val()
    var last_name = $('#mod_last_name').val()
    var user_id = $('#user_id').html()
    
    $.ajax({
        url: "user",
        type: "DELETE",
        data: {user_id: user_id},
    })
    .done(function(data, textStatus, jqXHR) {
        if (data !== 'operation interdite') {
            $('#'+user_id).parent().remove()
            $('#delete_user_message').html('L\'utilisateur <strong>'+first_name+' '+last_name+'</strong> a bien été supprimé')
            
            hide_alerts()
            $('#delete_user_message').removeClass('hidden')
            
            $('#myModal').modal('hide');
        }
        else {
            alert(data)
        }
    })
    .fail(function(jqXHR, textStatus, errorThrown) {
        alert('une erreur est survenue:' + JSON.stringify(jqXHR))
    })
})

$('#reset_password_button').click(function() {
    var first_name = $('#mod_first_name').val()
    var last_name = $('#mod_last_name').val()
    var user_id = $('#user_id').html()
    
    $.ajax({
        url: "reset_password",
        type: "POST",
        data: {user_id: user_id},
    })
    .done(function(data, textStatus, jqXHR) {
        if (data !== 'operation interdite') {
            $('#reset_password_message').html('Le mot de passe de <strong>'+first_name+' '+last_name+'</strong> a été réinitialisé et est désormais le suivant : <strong>'+data+'</strong>')
            
            hide_alerts()
            $('#reset_password_message').removeClass('hidden')
            
            $('#myModal').modal('hide');
        }
        else {
            alert(data)
        }
    })
    .fail(function(jqXHR, textStatus, errorThrown) {
        alert('une erreur est survenue:' + JSON.stringify(jqXHR))
    })
})