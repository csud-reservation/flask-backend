$(function() {
    $('.input-daterange input').each(function() {
        $(this).datepicker({language: "fr", daysOfWeekDisabled: "0,6"});
     });
    $('.date').datepicker({language: "fr", daysOfWeekDisabled: "0,6"});
    $("#switch").change(function() {
        if(this.checked) {
            //$(".end_dp").hide()
            $('#recurrence_off').hide()             //new
            $('#recurrence_on').show()             //new 
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

function redirect(url, method) {
    $('<form>', {
        method: method,
        action: url
    }).submit();
};

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

function reset_modal_view() {
    $(function() {
        $('.selected').removeClass('selected');
        $('.pivot').removeClass('pivot');
    });
}

function search() {
    redirect('search', 'post');
}
