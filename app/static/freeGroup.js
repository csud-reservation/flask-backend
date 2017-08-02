function generateConfirmMessage(){
    
     if ($('.selected').length) {
         console.log("hi")
     if (!is_checked('switch')) { // pas de récurrence
            var start_date = $('#date_non_ponctuelle').val();
            var end_date = $('#date_non_ponctuelle').val();
        } else { // si c'est récurrent
            var start_date = $('#date_de').val();
            var end_date = $('#date_a').val();
        }
    
    
    if (!is_checked('group')) {
        
        group = $("#general").val()
        determinant ="les classes "
    }
    
    else{
        group = $("#particular").val()
        determinant = "la classe "
        
    }

        var selected = document.getElementsByClassName('selected');
        var firstID = selected[0].id.replace('periode_', '');
        var lastID = selected[selected.length-1].id.replace('periode_', '');

    if (!is_checked('switch')) { 
        $("#confirmMessage").text("Voulez-vous vraiment libérer les classes "+group+" de la période "+firstID+" à "+lastID + " le "+start_date+ " ?")
    }
    else{
        $("#confirmMessage").text("Voulez-vous vraiment libérer les classes "+group+" de la période "+firstID+" à "+lastID + " du "+start_date+" au "+end_date +" ?")
    }
    
    $('#confirm').modal('toggle');
    
    } else {
        $('#no_hour_selected').removeClass('hidden')

    }
}

function free_group() {
    
    if (!is_checked('switch')) { // pas de récurrence
            var start_date = $('#date_non_ponctuelle').val();
            var end_date = $('#date_non_ponctuelle').val();
        } else { // si c'est récurrent
            var start_date = $('#date_de').val();
            var end_date = $('#date_a').val();
        }
        
        if ($('#select_general').hasClass('active')) {
            var group = $('#general').val()
            var type = 'student_group'
        }
        else if ($('#select_particular').hasClass('active')) {
            var group = $('#particular').val()
            var type = 'student_group'
        }
        else {
            var group = $('#room').val()
            var type = 'room'
        }

        var selected = document.getElementsByClassName('selected');
        var firstID = selected[0].id.replace('periode_', '');
        var lastID = selected[selected.length-1].id.replace('periode_', '');
    
        $.ajax({
            url: "freegroup",
            type: "PATCH",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            contentType: "application/x-www-form-urlencoded",
            data: {
                "start_date": start_date,
                "end_date": end_date,
                "group": group,
                "type": type,
                "firstID": firstID,
                "lastID": lastID,
            },
        })
        .fail(function(jqXHR, textStatus, errorThrown) {
            alert('une erreur est survenue')
        })
        
        .done(function(data, textStatus, jqXHR) {
            $('#free_group').text(data)
            $('#free_success').removeClass('hidden')
        })

}


$('#select_general, #select_particular, #select_room').click(function() {
    var select_id = $(this).attr('id')
    $('#select_general, #select_particular, #select_room').removeClass('active').addClass('notActive')
    $('#'+select_id).removeClass('notActive').addClass('active')
    $('#general, #particular, #room').hide()
    $('#'+select_id.replace('select_','')).show()
    if (select_id === 'select_room') {
        $('#label_group_room').text('Salle')
    } else if (select_id === 'select_general' || select_id === 'select_particular') {
        $('#label_group_room').text('Groupe')
    }
})

$(function() {
    $('#general, #particular, #room').hide()
    $('#general').show()
})