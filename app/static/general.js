function input_format(name, value) {
    return '<input type="hidden" name="' + name + '" value="' + value + '" />';
}

function add_to_form(name, value) {
    $('#input_invisible_base').before(input_format(name, value));
    $('#input_invisible_base').parent().hide();
}

