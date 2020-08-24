$(document).ready(function(){
    $("#coming_soon_section").on('click', function(e){
        e.preventDefault();
        $("#carouselIndicators").hide();
        $("#comingSoonIndicators").show();
        $("#coming_soon_section a").removeClass("text-muted");
        $("#now_showing_section a").addClass("text-muted");
    });

    $("#now_showing_section").on('click', function(e){
        e.preventDefault();
        $("#carouselIndicators").show();
        $("#comingSoonIndicators").hide();
        $("#coming_soon_section a").addClass("text-muted");
        $("#now_showing_section a").removeClass("text-muted");
    });
});