var nowDate = new Date();
switch(nowDate.getDay()) {
    case 6: var today2 = add_days_to_date(nowDate, 2); break;
    case 0: var today2 = add_days_to_date(nowDate, 1); break;
    default: var today2 = add_days_to_date(nowDate, 0); break;
}

function get_available_rooms() {
    if ($('.selected').length) {
        if (!is_checked('switch')) { // pas de récurrence
            var start_date = $('#date_non_ponctuelle').val();
            var end_date = $('#date_non_ponctuelle').val();
        } else { // si c'est récurrent
            var start_date = $('#date_de').val();
            var end_date = $('#date_a').val();
        }
        
        var selected = document.getElementsByClassName('selected');
        var firstID = selected[0].id.replace('periode_', '');
        var lastID = selected[selected.length-1].id.replace('periode_', '');
        
        var adminRights = is_checked('admin_rights')
        if (is_checked('room_object_selector')) {
            var reservation_type = 'item'
            var type_salle = $('#type_objet').val()
        } else {
            var reservation_type = 'room'
            
            var type_salle = '%('+$('#type_salle').val()+')';
            if (/ALL/.test(type_salle)) { 
                type_salle = '%'; 
            }
        }
        
        $.ajax({
            url: "search",
            type: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            contentType: "application/x-www-form-urlencoded",
            data: {
                "start_date": start_date,
                "end_date": end_date,
                // room_type est aussi item_type quand on veut réserver un objet
                "room_type": type_salle,
                "firstID": firstID,
                "lastID": lastID,
                "adminRights": adminRights,
                "reservation_type": reservation_type,
            },
        })
        .done(function(data, textStatus, jqXHR) {
            if (data === 'no room available') {
                $('#no_available_room').removeClass('hidden')
                return;
            }
            $('#full_second_form').html(data)
            $('#full_first_form').hide()
            format_dates()
        })
        .fail(function(jqXHR, textStatus, errorThrown) {
            alert('une erreur est survenue')
        });

    } else {
        $('#no_hour_selected').removeClass('hidden')
    }
}

function cancel_reservation() {
    $('#full_second_form').html('')
    $('#full_first_form').show()
}

function new_reservation() {
    remove_form()
    create_form()
    var data = ['room_select','student_group','reason','res_name','first_period','last_period','start_date','end_date']

    for (var i = 0; i < data.length; i++) {
        if ($('#'+data[i]).is('span')) {
            add_to_form(data[i], $('#'+data[i]).html())    
        } else { 
            add_to_form(data[i], $('#'+data[i]).val())
        }
    }
    
    $('#invisible_form').wrap('<form id="full_invisible_form" action="new_reservation" method="post"></form>');
    $('#full_invisible_form').submit();
}
 
function select(element, index) {
    $(function() {
        if ($('.pivot').length) {
            $('.selected').removeClass('selected');
            var firstID = parseInt($('.pivot').get(0).id.replace('periode_', ''));
            var lastID = index
            if (firstID < lastID) {
                while (firstID <= lastID) {
                    $('#periode_'+firstID).addClass('selected');
                    firstID = firstID + 1;
                }
            } else {
                while (firstID >= lastID) {
                    $('#periode_'+firstID).addClass('selected');
                    firstID = firstID - 1;
                }
            }
            $('.pivot').removeClass('pivot');
            $('#periode_'+lastID).addClass('pivot');
        } else {
            $(element).addClass('pivot selected');
        }
    });
    if ($('.selected').length) {
        $('#no_hour_selected').addClass('hidden')
    }
}

function is_checked(id) {
    // http://stackoverflow.com/questions/2204250/check-if-checkbox-is-checked-with-jquery
    var checked = $("input[id=" + id + "]:checked").length;
    if (checked == 0) {
      return false;
    } else {
      return true;
    }
}

function reset_modal_view() {
    $('.selected').removeClass('selected');
    $('.pivot').removeClass('pivot');
}

function initialize_datepicker(element, listBanned='0,6') {
    $('input:not(.modal-body input)').prop("readonly", true);
    $(element).datepicker({language: "fr", daysOfWeekDisabled: listBanned, autoclose: true})
        .on('hide', function(e) {
            return;
        });
}

$("#room_select").change(function() {
  $("#room").text($("#room_select").val())
});

$(function() {

    $("#room").text($("#room_select").val());
    $('.today').val(convert_Date_to_dateString(today2));
    
    $('#date_de').change(function() {
        var dateSelected = $(this).val();
        var matches = /([0-9]{2})\.([0-9]{2})\.([0-9]{4})/.exec(dateSelected);
        var date_formatted = new Date(parseInt(matches[3].replace(/^0(.+)/, '$1')),
            parseInt(matches[2].replace(/^0(.+)/, '$1'))-1,
            parseInt(matches[1].replace(/^0(.+)/, '$1')), 0, 0, 0, 0);
        var day = date_formatted.getDay();
        var listBanned = '0,1,2,3,4,5,6'.replace(','+day, '');
        $('#date_a').before('<input type="text" class="form-control date_a_replace">');
        $('#date_a').remove();
        $('.date_a_replace').attr('id', 'date_a');
        $('#date_a').val(dateSelected);
        initialize_datepicker($('#date_a'), listBanned);
    });

    initialize_datepicker($('#date_de'));
    initialize_datepicker($('#date_a'));
    initialize_datepicker($('.date'));
    
    $("#switch").change(function() {
        if (this.checked) {
            $('#recurrence_off').hide()
            $('#recurrence_on').show()
            $(".date_input_form").first().removeClass('col-sm-3').addClass('col-sm-5')
        }
        else{
            $('#recurrence_on').hide() 
            $('#recurrence_off').show()
            $(".date_input_form").first().removeClass('col-sm-5').addClass('col-sm-3')
        }
    });
    
    $('#room_object_selector').change(function() {
        if (this.checked) {
            // réservation d'objet
            $('.label_type_objet').first().removeClass('hidden');
            $('.label_type_salle').first().addClass('hidden');
            $('#type_objet').removeClass('hidden');
            $('#type_salle').addClass('hidden');
        } else {
            // réservation de salle
            $('.label_type_objet').first().addClass('hidden');
            $('.label_type_salle').first().removeClass('hidden');
            $('#type_objet').addClass('hidden');
            $('#type_salle').removeClass('hidden');
        }
    });

    $('#myModal').on('hidden.bs.modal', function(e) { 
        if (!$('.selected').length) {
            $('#no_hour_selected').removeClass('hidden')
        }
    });
    
    $('.toggle-on, .toggle-off').each(function() {
        if ($(this).parent().parent().parent().hasClass('room_object_selector')) {
            if ($(this).hasClass('toggle-on')) {
                $(this).html('Objet')
            } else if ($(this).hasClass('toggle-off')) {
                $(this).html('Salle')
            }
        }
    })
});