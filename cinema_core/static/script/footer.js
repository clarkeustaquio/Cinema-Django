$(document).ready(function(){

    let screen_width = $(this).width();
    if (screen_width < 576){
        $("#footer_cinema").hide();
    }else if(screen_width > 576){
        $("#footer_cinema").show();
    }


    $(window).on('resize', function(){
        let width = $(this).width();
        if (width < 576){
            $("#footer_cinema").hide();
        }else if(width > 576){
            $("#footer_cinema").show();
        }
    });
});