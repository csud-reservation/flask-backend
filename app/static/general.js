function input_format(name, value) {
    return '<input type="hidden" name="' + name + '" value="' + value + '" />';
}

function add_to_form(name, value) {
    $('#input_invisible_base').before(input_format(name, value));
    $('#input_invisible_base').parent().hide();
}

function convert_sql_dateString_to_Date(sql_date_str) {
    var matches = /([0-9]{4})-([0-9]{2})-([0-9]{2})/.exec(sql_date_str);
    return new Date(parseInt(matches[1]),
        parseInt(matches[2])-1,
        parseInt(matches[3]));
}

function convert_dateString_to_Date(date_str) {
    var matches = /([0-9]{2})\.([0-9]{2})\.([0-9]{4})/.exec(date_str);
    return new Date(parseInt(matches[3]),
        parseInt(matches[2])-1,
        parseInt(matches[1]));
}

function convert_Date_to_dateString(date) {
    return String(date.getDate()).replace(/^([0-9])$/, '0' + '$1') + '.' + 
    (String(date.getMonth() + 1)).replace(/^([0-9])$/, '0' + '$1') + "." + date.getFullYear()
}

function add_days_to_date(date, days_to_add) {
    return new Date(date.getFullYear(), (date.getMonth()), 
    (date.getDate()+parseInt(days_to_add)), 0, 0, 0, 0);
}

function remove_days_to_date(date, days_to_remove) {
    return new Date(date.getFullYear(), (date.getMonth()), 
    (date.getDate()-parseInt(days_to_remove)), 0, 0, 0, 0);
}

$(function() {
    $('.date_format').each(function() {
        var original_date = $(this).html();
        var date_formated = convert_sql_dateString_to_Date(original_date);
        var date_string = convert_Date_to_dateString(date_formated);
        $(this).html(date_string);
    });    
});
