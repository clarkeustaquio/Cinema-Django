$(document).ready(function(){

    let screen_width = $(this).width();
    if (screen_width < 992){
        $("#mobileView").show();
        $("#desktopView").hide();

    }else if (screen_width > 992){
        $("#mobileView").hide();
        $("#desktopView").show();
    }

    $(window).on('resize', function(){
        let width = $(this).width();
        if (width < 992){
            $("#mobileView").show();
            $("#desktopView").hide();
        }else if (width > 992){
            $("#mobileView").hide();
            $("#desktopView").show();
        }
    });
});