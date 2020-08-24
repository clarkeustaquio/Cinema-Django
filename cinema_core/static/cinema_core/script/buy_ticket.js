$(document).ready(function(){
    let screen_width = $(this).width();
    if (screen_width < 992){
        $("#image_banner").hide();
        $("#container_form").removeClass();
        $("#container_form").addClass("container");
    }

    $(window).on('resize', function(){
        let width = $(this).width();

        if (width < 992){
            $("#image_banner").hide();
            $("#container_form").removeClass();
            $("#container_form").addClass("container");
        }else if (width > 992){
            $("#image_banner").show();
            $("#container_form").addClass("mt-3");
            $("#container_form").addClass("ml-3");
            $("#container_form").addClass("mb-5");
        }
    });
});