$(document).ready(function(){
    $("#like_manager a").on('click', function(e){
        e.preventDefault();
        let href = $(this).attr("href");
        let id = $(this).data("manager");
        let attribute = $(this).attr("id");

        $.ajax({
            type: "GET",
            url: href,
            success: function(response){
                if (attribute == "like"){

                    if (($("[data-like="+ id +"]").hasClass("text-dark")) && ($("[data-dislike="+ id +"]").hasClass("text-dark"))){
                        $("[data-like="+ id +"]").removeClass("text-dark");
                        $("[data-like="+ id +"]").addClass("text-primary");
                    }else if(($("[data-like="+ id +"]").hasClass("text-primary")) && ($("[data-dislike="+ id +"]").hasClass("text-dark"))){
                        $("[data-like="+ id +"]").removeClass("text-primary");
                        $("[data-like="+ id +"]").addClass("text-dark");
                    }else if(($("[data-dislike="+ id +"]").hasClass("text-primary")) && ($("[data-like="+ id +"]").hasClass("text-dark"))){
                        $("[data-like="+ id +"]").removeClass("text-dark");
                        $("[data-like="+ id +"]").addClass("text-primary");

                        $("[data-dislike="+ id +"]").removeClass("text-primary");
                        $("[data-dislike="+ id +"]").addClass("text-dark");
                    }

                    

                }else if(attribute == "dislike"){
                    if (($("[data-like="+ id +"]").hasClass("text-dark")) && ($("[data-dislike="+ id +"]").hasClass("text-dark"))){
                        $("[data-dislike="+ id +"]").removeClass("text-dark");
                        $("[data-dislike="+ id +"]").addClass("text-primary");
                    }else if(($("[data-like="+ id +"]").hasClass("text-dark")) && ($("[data-dislike="+ id +"]").hasClass("text-primary"))){
                        $("[data-dislike="+ id +"]").removeClass("text-primary");
                        $("[data-dislike="+ id +"]").addClass("text-dark");
                    }else if(($("[data-dislike="+ id +"]").hasClass("text-dark")) && ($("[data-like="+ id +"]").hasClass("text-primary"))){
                        $("[data-like="+ id +"]").removeClass("text-primary");
                        $("[data-like="+ id +"]").addClass("text-dark");

                        $("[data-dislike="+ id +"]").removeClass("text-dark");
                        $("[data-dislike="+ id +"]").addClass("text-primary");
                    }
                }
            }
        });
    });
});