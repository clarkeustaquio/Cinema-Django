$(document).ready(function(){
    let href = window.location.href;

    if (href.indexOf('now_showing_section') > -1){
        $("#now_showing_section").trigger("click");
    }else if (href.indexOf('coming_soon_section') > -1) {
        $("#coming_soon_section").trigger("click");
    }
});