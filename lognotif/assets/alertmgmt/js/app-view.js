$(function() {
    $('.datepicker').datepicker();
    $('.timepicker').timepicker();
    $("#div-container-filter").hide()
    $("#filter-container").click(function(){
        $("#div-container-filter").slideToggle();
    });
    $(".severity-option").on("click", function() {
        var s = ($(this).val())
        $("#severity-option-output").val(s)
    });

    $(".time-option").on("click", function() {
        var s = ($(this).val())
        $("#timestamp-option-output").val(s)
    });

    $("#decrease_page_counter").on("click", function() {
        var c = parseInt($("#page-no-output").val())
        if(c > 1) {
            $("#page-no-output").val(c-1)
            $('#btn_submit_filter_form').trigger( "click" );
        }
    });

    $("#increase_page_counter").on("click", function() {
        var c = parseInt($("#page-no-output").val())
            $("#page-no-output").val(c+1)
            $('#btn_submit_filter_form').trigger( "click" );
    });

    $(".radio-log-source").on("click", function() {
        $("#input-logsource").val($(this).val());
    });

    $('.modal').modal();

    $('.id-userlist-group').on("click", function() {
        $('#id_assignto').val($(this).val())
    });

    var logs = []

//    $('.select-all-logs').on('click', function() {
//        var logs = document.getElementsByClassName("select-logs")
//        var opt = document.getElementsByClassName('select-all-logs')
//        var i;
//        var txt = "";

//        $('input[type="checkbox"]').click(function(){
//            if($(this).prop("checked") == true){
//                console.log("Checkbox is checked.");
//                for(i=0;i<logs.length;i ++) {
//                    $(logs[i]).attr("checked", true)
//                }
//            }
//            else if($(this).prop("checked") == false){
//                console.log("Checkbox is unchecked.");
//                for(i=0;i<logs.length;i ++) {
//                    $(logs[i]).attr("checked", false)
//                }
//            }
//        });
//    })

    $('#id-btn-assign').on('click', function() {
        var logs = document.getElementsByClassName("select-logs")
        var i;
        var txt = "";
        for(i=0;i<logs.length;i ++) {
            if (logs[i].checked) {
                txt = txt + logs[i].value + " _;_ ";
            }
        }
        $("#id_loglist").text(txt)
        if(txt == '') {
            $("#error_new_assignment").text('Please select atleast 1 log to save this assignment.')
        } else {
            $("#error_new_assignment").text('')
        }
    });
});

function copyToClipboard(element) {
    M.toast({html: 'Copied to Clipboard!', classes: 'rounded', displayLength: '2000'})
    var $temp = $("<textarea>");
    var brRegex = /<br\s*[\/]?>/gi;
    $("body").append($temp);
    $temp.val($(element).html().replace(brRegex, "\n")).select();
    document.execCommand("copy");
    $temp.remove();
}