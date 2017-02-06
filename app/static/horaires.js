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
    var date_formatted = convert_dateString_to_Date(original_date);
    switch(date_formatted.getDay()) {
        case 0: var lundi = add_days_to_date(date_formatted, 1); break;
        case 1: var lundi = add_days_to_date(date_formatted, 0); break;
        case 2: var lundi = remove_days_to_date(date_formatted, 1); break;
        case 3: var lundi = remove_days_to_date(date_formatted, 2); break;
        case 4: var lundi = remove_days_to_date(date_formatted, 3); break;
        case 5: var lundi = remove_days_to_date(date_formatted, 4); break;
        case 6: var lundi = add_days_to_date(date_formatted, 2); break;
    }
    var vendredi = add_days_to_date(lundi, 4);
    var str_lundi = convert_Date_to_dateString(lundi);
    var str_vendredi = convert_Date_to_dateString(vendredi);
    
    return str_lundi + ' - ' + str_vendredi;
}

function set_week_date() {
    var original_date = $('#weekly_datepicker').val()
    $('#weekly_datepicker').val(format_week_dates(original_date));
}

function get_two_dates(two_dates_str) {
    var matches = /^([0-9]{2}\.[0-9]{2}\.[0-9]{4})\ -\ ([0-9]{2}\.[0-9]{2}\.[0-9]{4})$/.exec(two_dates_str);
    return [matches[1], matches[2]];
}

function submit_invisible_form_timetable() {
    $('#titre').html('Salle ' + $('#rooms_numbers').val());
    $('#result').html('chargement des résultats');
    var dates = $('#weekly_datepicker').val();
    var room_number = $('#rooms_numbers').val();
    var start_date = get_two_dates(dates)[0];
    var end_date = get_two_dates(dates)[1];
    
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

function change_week(is_previous_week) {
    var monday_str = get_two_dates($('#weekly_datepicker').val())[0];
    var monday_Date = convert_dateString_to_Date(monday_str);
    if (is_previous_week) {
        var new_monday_Date = remove_days_to_date(monday_Date, 7);
    } else {
        var new_monday_Date = add_days_to_date(monday_Date, 7);
    }
    var new_monday_str = convert_Date_to_dateString(new_monday_Date);
    
    $('#weekly_datepicker').before('<input type="text" class="form-control today weekly_datepicker_replace">');
    $('#weekly_datepicker').remove();
    $('.weekly_datepicker_replace').attr('id', 'weekly_datepicker');
    $('#weekly_datepicker').val(new_monday_str);
    
    initialize_weekly_datepicker();
    submit_invisible_form_timetable();
}

function initialize_weekly_datepicker() {
    $('input').prop("readonly", true);
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
    set_week_date();
}

$(function() {
    $('#rooms_numbers').change(submit_invisible_form_timetable);
    
    $('#rooms_type').change(function() {
        var value = $(this).val();
        reset_select_rooms();
        if (value !== 'ALL') {
            filter_select_rooms(value);   
        }
        submit_invisible_form_timetable();
    });
    
    initialize_weekly_datepicker();
    
    $('#weekly_datepicker').change(function() {
        set_week_date();
        select_days_in_week();
        submit_invisible_form_timetable();
    });
    
    submit_invisible_form_timetable();
});