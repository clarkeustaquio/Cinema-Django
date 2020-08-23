$(document).ready(function(){

    let screen_width = $(this).width();
    if (screen_width < 576){
        $("#primary").addClass("btn-block");
        $("#resend").addClass("btn-block");
        $("#remove").addClass("btn-block");
    }

    $(window).on('resize', function(){
        let width = $(this).width();
        if (width < 576){
            $("#primary").addClass("btn-block");
            $("#resend").addClass("btn-block");
            $("#remove").addClass("btn-block");
        }else if(width > 576){
            $("#primary").removeClass("btn-block");
            $("#resend").removeClass("btn-block");
            $("#remove").removeClass("btn-block");
        }
    });
});