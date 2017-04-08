$(function() {
    $('th:not(.modal-body th)').css('background-color', 'rgb(249,249,249)');
});

$('.infos_button').click(function() {
    var reservation_id = $(this).parent().attr("id")
    var detailed_infos_block = $('#'+reservation_id).find('.detailed_infos')
    $(detailed_infos_block.children()).each(function() {
        var element_class = $(this).attr('class')
        if (element_class === 'start_date' || element_class === 'end_date') {
            var text_to_export = convert_Date_to_dateString(convert_sql_dateString_to_Date($(this).text()))
        } else {
            var text_to_export = $(this).text()
        }
        if (text_to_export === '') {
            text_to_export = '-'
        }
        $('#'+element_class).html(text_to_export)
        $('#reservation_id').parent().hide()
    })
    reset_mv()
    $('#myModal').modal()
});

$('#modify_button').click(function() {
    $('#modal_view_content').find('table').hide()
    $('.modify_form').removeClass('hidden')
    $(this).before('<button type="button" class="btn btn-primary" id="cancel_mod_button" onclick="reset_mv()">Annuler les modifications</button>')
    $(this).before('<button type="button" class="btn btn-success" id="update_mod_button" onclick="update_mod()">Enregistrer les modifications</button>')
    $(this).hide()
    $('#delete_button').hide()
    $('#reason_short_input').val($('#reason_short').text())
    $('#student_group_input').val($('#student_group').text())
    $('#reason_details_input').val($('#reason_details').text())
    $('#modal_view_content').find('.modify_form').find('.form-control').each(function() {
        if ($(this).val() === '-') {
            $(this).val('')
        }
    })

});

function reset_mv() {
    $('#modal_view_content').find('table').show()
    $('.modify_form').addClass('hidden')
    $('#cancel_mod_button').remove()
    $('#update_mod_button').remove()
    $('#modify_button').show()
    $('#delete_button').show()
    $('#reason_short_input').val()
    $('#student_group_input').val()
    $('#reason_details_input').val()
}

$('#delete_button').click(function() {
    var reservation_id = $('#reservation_id').html()
    $.ajax({
        url: "my_reservations",
        type: "DELETE",
        data: {
            "id": reservation_id,
        },
    })
    .done(function(data, textStatus, jqXHR) {
        $('#'+reservation_id).parent().remove()
        $('#res_deleted_message').removeClass('hidden')
        $('#res_updated_message').addClass('hidden')
        $('#just_reserved').addClass('hidden')
    })
    .fail(function(jqXHR, textStatus, errorThrown) {
        alert('une erreur est survenue');
    })
});

function update_in_page(to_update) {
    var content_updated = $('#'+to_update+'_input').val()
    var reservation_id = $('#reservation_id').html()
    $('#'+reservation_id).find('.'+to_update).html(content_updated)
    $('#'+reservation_id).parent().find('.'+to_update+'_info').html(content_updated)
}

function update_mod() {
    var reservation_id = $('#reservation_id').html()
    $.ajax({
        url: "my_reservations",
        type: "PATCH",
        data: {
            "id": reservation_id,
            "reason_short": $('#reason_short_input').val(),
            "reason_details": $('#reason_details_input').val(),
            "student_group": $('#student_group_input').val(),
        },
    })
    .done(function(data, textStatus, jqXHR) {
        update_in_page('reason_short')
        update_in_page('reason_details')
        update_in_page('student_group')

        $('#myModal').modal('hide')
        $('#res_updated_message').removeClass('hidden')
        $('#res_deleted_message').addClass('hidden')
        $('#just_reserved').addClass('hidden')
    })
    .fail(function(jqXHR, textStatus, errorThrown) {
        alert('une erreur est survenue');
    })

}