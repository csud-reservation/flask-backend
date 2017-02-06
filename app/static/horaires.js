function reset_select_rooms() {
    var original_html = $('#rooms_numbers_hidden').html();
    $('#rooms_numbers').html(original_html
        .replace(/rooms_choice_hidden/g, 'rooms_choice'));
}

function filter_select_rooms(value) {
    $('.rooms_choice').each(function() {
        var regex = new RegExp(value, 'i');
        if (!regex.test($(this).val())) {
            $(this).remove();
        } 
    });
}

function select_days_in_week() {
    var days_in_week = document.getElementsByClassName('day active')[0]
    .parentNode.getElementsByClassName('day');
    for (var i = 1; i < days_in_week.length-1; i++) {
        days_in_week[i].className = 'active day';
    }
    $('.active').filter('.disabled').filter('.disabled-date').filter('.day').removeClass('active');
}

function format_week_dates(original_date) {
    // NB : ce code est un peu chaotique, mais j'étais fatigué au moment de l'écrire
    var matches = /([0-9]{2})\.([0-9]{2})\.([0-9]{4})/.exec(original_date);
    var date_formatted = new Date(parseInt(matches[3].replace(/^0(.+)/, '$1')),
        parseInt(matches[2].replace(/^0(.+)/, '$1'))-1,
        parseInt(matches[1].replace(/^0(.+)/, '$1')));
    var vendredi = new Date();
    switch(date_formatted.getDay()) {
        case 6: var lundi = new Date(date_formatted.getFullYear(), (date_formatted.getMonth()), (date_formatted.getDate()+2), 0, 0, 0, 0); break;
        case 0: var lundi = new Date(date_formatted.getFullYear(), (date_formatted.getMonth()), (date_formatted.getDate()+1), 0, 0, 0, 0); break;
        case 1: var lundi = new Date(date_formatted.getFullYear(), (date_formatted.getMonth()), (date_formatted.getDate()+0), 0, 0, 0, 0); break;
        case 2: var lundi = new Date(date_formatted.getFullYear(), (date_formatted.getMonth()), (date_formatted.getDate()-1), 0, 0, 0, 0); break;
        case 3: var lundi = new Date(date_formatted.getFullYear(), (date_formatted.getMonth()), (date_formatted.getDate()-2), 0, 0, 0, 0); break;
        case 4: var lundi = new Date(date_formatted.getFullYear(), (date_formatted.getMonth()), (date_formatted.getDate()-3), 0, 0, 0, 0); break;
        case 5: var lundi = new Date(date_formatted.getFullYear(), (date_formatted.getMonth()), (date_formatted.getDate()-4), 0, 0, 0, 0); break;
    }
    var vendredi = new Date(lundi.getFullYear(), lundi.getMonth(), (lundi.getDate()+4), 0, 0, 0, 0);
    var str_lundi = (String(lundi.getDate()).replace(/^([0-9])$/, '0' + '$1') + '.' + 
    (String(lundi.getMonth() + 1)).replace(/^([0-9])$/, '0' + '$1') + "." + lundi.getFullYear())
    var str_vendredi = (String(vendredi.getDate()).replace(/^([0-9])$/, '0' + '$1') + '.' + 
    (String(vendredi.getMonth() + 1)).replace(/^([0-9])$/, '0' + '$1') + "." + vendredi.getFullYear())
    
    return str_lundi + ' - ' + str_vendredi;
}

function set_week_date() {
    var original_date = $('#weekly_datepicker').val()
    $('#weekly_datepicker').val(format_week_dates(original_date));
}

function submit_invisible_form_timetable() {
    $('#result').html('chargement des résultats');
    var dates = $('#weekly_datepicker').val();
    var room_number = $('#rooms_numbers').val();
    var matches = /^([0-9]{2}\.[0-9]{2}\.[0-9]{4})\ -\ ([0-9]{2}\.[0-9]{2}\.[0-9]{4})$/.exec(dates);
    var start_date = matches[1];
    var end_date = matches[2];
   
    // add_to_form('room_number', room_number)
    // add_to_form('start_date', start_date)
    // add_to_form('end_date', end_date)
    
    // var full_form = $('#invisible_form').html();
    // $('<form action="timetable" method="post">' + full_form + '</form>').submit();
    
    $.ajax({
    url: "timetable?" + $.param({
        "room_number": room_number,
        "start_date": start_date,
        "end_date": end_date,
    }),
        type: "POST",
    })
    .done(function(data, textStatus, jqXHR) {
        $('#result').html(data);
    })
    .fail(function(jqXHR, textStatus, errorThrown) {
        alert('une erreur est survenue');
    })
}

$(function() {
    $('#rooms_type').change(function() {
        var value = $(this).val();
        reset_select_rooms();
        if (value !== 'ALL') {
            filter_select_rooms(value);   
        }
    });
    
    set_week_date();
    
    $('#weekly_datepicker').datepicker({language: "fr", daysOfWeekDisabled: '0,6'})
    .on('show', function(e) {
        select_days_in_week();
        $('.day').filter('.active').parent().parent().find('tr').each(function() {
            if ($(this).find('.day').length != 0) {
                $(this).hover(function() {
                    $(this).addClass('date_hover'); 
                }, function() {
                    $(this).removeClass('date_hover');
                });
            }
        });
    }).on('hide', function(e) {
        set_week_date();
    });
    $('#weekly_datepicker').change(function() {
        set_week_date();
        select_days_in_week();
    });
});