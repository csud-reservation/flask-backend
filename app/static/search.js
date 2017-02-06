var nowDate = new Date();

if (nowDate.getDay() == 6) {
    var today2 = new Date(nowDate.getFullYear(), nowDate.getMonth(), (nowDate.getDate() + 2), 0, 0, 0, 0);
} else if (nowDate.getDay() == 0) {
    var today2 = new Date(nowDate.getFullYear(), nowDate.getMonth(), (nowDate.getDate() + 1), 0, 0, 0, 0);
} else {
    var today2 = new Date(nowDate.getFullYear(), nowDate.getMonth(), nowDate.getDate(), 0, 0, 0, 0);
}

function submit_invisible_form() {
    if ($('.selected').length) {
        if (!is_checked('switch')) { // pas de récurrence
            if ($('#date_non_ponctuelle').val() === '') {
                alert('vous devez choisir une date');
                return;
            }
            var start_date = $('#date_non_ponctuelle').val();
            var end_date = $('#date_non_ponctuelle').val();
        } else { // si c'est récurrent
            if ($('#date_de').val() === '' || $('#date_a').val() === '') {
                alert('vous devez choisir une date');
                return;
            }
            var start_date = $('#date_de').val();
            var end_date = $('#date_a').val();
        }
        var type_salle = '%('+$('#type_salle').val()+')';
        if (/ALL/.test(type_salle)) { type_salle = '%'; }
        var selected = document.getElementsByClassName('selected');
        var firstID = selected[0].id.replace('periode_', '');
        var lastID = selected[selected.length-1].id.replace('periode_', '');
        add_to_form('start_date', start_date);
        add_to_form('end_date', end_date);
        add_to_form('room_type', type_salle);
        add_to_form('firstID', firstID);
        add_to_form('lastID', lastID);
        
        var full_form = $('#invisible_form').html();
        $('<form action="search" method="post">' + full_form + '</form>').submit();
    } else {
        alert('vous n\'avez sélectionné aucune période');
    }
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
    $(function() {
        $('.selected').removeClass('selected');
        $('.pivot').removeClass('pivot');
    });
}

$(function() {
    var curr_date_full = (String(today2.getDate()).replace(/^([0-9])$/, '0' + '$1') + '.' + 
    (String(today2.getMonth() + 1)).replace(/^([0-9])$/, '0' + '$1') + "." + today2.getFullYear())
    $('.today').val(curr_date_full);
    
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
        $('#date_a').datepicker({language: "fr", daysOfWeekDisabled: listBanned, autoclose: true});
        $('#date_a').val(dateSelected);
    });

    $('#date_de').each(function () {
        $(this).datepicker({language: "fr", daysOfWeekDisabled: '0,6', autoclose: true});
    });
    $('#date_a').each(function () {
        $(this).datepicker({language: "fr", daysOfWeekDisabled: '0,6', autoclose: true});
    });
     
    $('.date').datepicker({language: "fr", daysOfWeekDisabled: '0,6', autoclose: true});
    
    $("#switch").change(function() {
        if(this.checked) {
            //$(".end_dp").hide()
            $('#recurrence_off').hide()
            $('#recurrence_on').show()
            $(".date_input_form").first().removeClass('col-sm-3').addClass('col-sm-5')
        }
        else{
            //$(".end_dp").show()
            $('#recurrence_on').hide()             //new   
            $('#recurrence_off').show()             //new 
            $(".date_input_form").first().removeClass('col-sm-5').addClass('col-sm-3')
        }
    });
});