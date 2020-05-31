$(function() {
    $('.tabs').tabs();
    $('#btn-hide-log-data').on('click', function() {
        $('.div-container-header').slideToggle("slow")
    })
    $('#tab-assign-task').on('click', function() {
        $('.div-container-header').hide()
    });

    $('.modal').modal();

    $('.btn-delete-ack-parent').on('click', function() {
        var a = '/alertmgmt/ack_alert_delete/'
        var b = $(this).html()
        b = b.substring(b.indexOf("hidden"))
        b = b.substring(b.indexOf(">")+1, b.indexOf("<"))
        console.log(a)
        console.log(b)
        $('#btn-delete-ack').attr("action", a + b)
    });
    $('.btn-reassign-ack-parent').on('click', function() {
        var a = '/alertmgmt/alert_reassign/'
        var b = $(this).html()
        console.log(a)
        console.log(b)
        b = b.substring(b.indexOf("hidden"))
        b = b.substring(b.indexOf(">")+1, b.indexOf("<"))
        $('#btn-reassign').attr("action", a + b)
    });

    $(".radio-user-list").on("click", function() {
        $("#id_assignto").val($(this).val())
    });
    $("#btn-reass").on("click", function() {
        var a = window.location.href;
        assignment_name = decodeURIComponent(a.substring(a.lastIndexOf("/") + 1));
//        $('#form-id-reassign').attr('action', "alert_reassign/" + assignment_name)
        $("#id_assignment_name").val(assignment_name)
    });

    var uri = window.location.toString();

    var clean_uri = uri.substring(0, uri.indexOf("?"));
    window.history.replaceState({}, document.title, clean_uri);

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