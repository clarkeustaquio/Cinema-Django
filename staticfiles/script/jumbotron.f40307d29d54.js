$(document).ready(function(){
    let width = $(this).width();
    if (width < 992){
        $("#jumbotron_col_1").hide();
        $("#jumbotron_col_2").attr("class", "col");
        $("#now_showing_section").removeClass("h4");
        $("#coming_soon_section").removeClass("h4");
    }

    $(window).on('resize', function(){
        let screen_width = $(this).width();
    
        if (screen_width < 992){
            $("#jumbotron_col_1").hide();
            $("#jumbotron_col_2").attr("class", "col");
            $("#now_showing_section").removeClass("h4");
            $("#coming_soon_section").removeClass("h4");
        }else if(screen_width > 992){
            $("#jumbotron_col_1").show();
            $("#jumbotron_col_2").attr("class", "col-6");
            $("#now_showing_section").addClass("h4");
            $("#coming_soon_section").addClass("h4");
        }
    });
});