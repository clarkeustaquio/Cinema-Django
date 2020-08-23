$(document).ready(function(){
    let width = $(this).width();
    if (width < 576){
        $("#edit_email").removeClass("float-right");
        $("#edit_pass").removeClass("float-right");
    }

    $(window).on('resize', function(){
        let screen_width = $(this).width();
        if (screen_width < 576){
            $("#edit_email").removeClass("float-right");
            $("#edit_pass").removeClass("float-right");
        }else if (screen_width > 576){
            $("#edit_email").addClass("float-right");
            $("#edit_pass").addClass("float-right");
        }
    });
});