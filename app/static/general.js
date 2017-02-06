function input_format(name, value) {
    return '<input type="hidden" name="' + name + '" value="' + value + '" />';
}

function add_to_form(name, value) {
    $('#input_invisible_base').before(input_format(name, value));
    $('#input_invisible_base').parent().hide();
}



$(function() {
    $('.date_format').each(function(i, obj) {
        
    var date = new Date($(this).text())
    var day = date.getDate()
    if (day < 10){
        day = "0"+day
    }
    
    var month = date.getMonth()
    if (month < 10){
        month = "0"+month
    }
    $(this).text(day+"."+month+"."+date.getFullYear())
    });
});
    
