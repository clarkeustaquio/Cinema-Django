$(document).ready(function(){
    $("#seatContainer a").click(function(e){
        e.preventDefault();
        var href = $(this).attr("href");
        var id = $(this).data("seat");
        
        $.ajax({
            type: "GET",
            url: href,
            success: function(response){
                var img_ref = $("img[id="+id+"]");
                var length = response.ticket_orders.length - 1;
                var data = response.ticket_orders[length];

                if(response.cart != 0){
                    $("#emptyCart").remove();
                    $("#checkout").removeClass("disabled");
                }else{
                    $("#checkout").addClass("disabled");
                    $("#totalCart").remove();
                }

                $("#cart").html(response.cart);
                if(img_ref.attr("src") == image_available){
                    img_ref.attr("src", image_selected);
                    
                    var cartBox = $('<li data-order="' + id + '" id="cartInfo" class="list-group-item d-flex justify-content-between lh-condensed"><div><h6>'+ data.movie_title + '</h6>' +
                        '<h6><small class="text-muted">'+ data.date + '</small></h6><small class="text-muted">Seat No: ' + data.seat +'</small></div>' +
                        '<div><span class="text-muted">₱'+ data.movie_price +'</span><h6><small class="text-muted"><a data-remove="' + id+ '" href="' + href + '">Remove</a></small></h6></div></li>'
                    );
                    
                    var modalBody = $('<div id="card_layout" class="card mb-1" data-modal="'+ id + '"><div class="card-header"><div class="container"><div class="row"><div class="col">' + 
                        '<h5><b>' + data.movie_title + '</b></h5></div><div class="col"><h5>Price</h5></div><div class="col"><h5>Date</h5></div><div class="col">' +
                        '<h5>Seat No.</h5></div></div></div></div><div class="card-body"><div class="container"><div class="row"><div class="col">' +
                        '<img src="' + data.movie_banner + '" class="card-img w-50"></div><div class="col"><h5>Php ' + data.movie_price + '</h5></div><div class="col">' +
                        '<h5><b>' + data.theater_name + '</b></h5><h5>' + data.date + '</h5><h5>' + data.time + '</h5></div><div class="col"><h5>' + data.seat + '</h5>' +
                        '</div></div></div></div></div><div class="d-flex flex-row flex-wrap" data-modal="' + id + '"><div id="card_block" class="card mb-2 ml-auto mr-auto" style="width: 34.5rem"><div class="row no-gutters">' +
                        '<div class="col-md-8"><div class="card-body mb-3"><h3 class="card-title">' + data.movie_title + '</h3><p class="card-text"><b>' + data.theater_name + ' - Php ' + data.movie_price + '</b></p>' +
                        '<div style="height: 5.5rem;"><p class="text-justify">' + data.date + '</p><p class="test-justify">' + data.time + '</p><p>Seat: <b>' + data.seat + '</b></p></div></div></div></div></div></div>'
                    );
                    
                    var totalBox = $('<li id="totalCart" class="list-group-item d-flex justify-content-between lh-condensed"><div class="col"><div class="row">' +
                        '<div class="col ml-n3"><h6 class="float-left"><span>Total (Php)</span></h6><div class="modal fade" id="view_ticket_info" tabindex="-1" role="dialog" aria-labelledby="viewTicketInfoLabel" aria-hidden="true">' +
                        '<div class="modal-dialog modal-xl"><div class="modal-content"><div class="modal-header"><h5 class="modal-title" id="viewTicketInfoLabel">Your Ticket Info</h5><button type="button" class="close" data-dismiss="modal" aria-label="Close">' +
                        '<span aria-hidden="true">&times;</span></button></div><div class="modal-body" id="modalBody"></div><button type="button" class="btn btn-dark rounded-0 float-right" data-dismiss="modal">Close</button></div></div></div></div><div class="col"><strong id="totalAmount" class="float-right mr-n2">₱'+ response.total_amount +'</strong>' +
                        '</div></div><div class="row float-right"><button type="button" data-toggle="modal" data-target="#view_ticket_info" class="btn btn-light">View Ticket Info</button></div></div></li>'
                    );

                    if($("#ticketOrder #totalCart").length){
                        $(cartBox).insertBefore("#totalCart");
                    }else{
                        $("#ticketOrder").append(cartBox);
                        $("#ticketOrder").append(totalBox);
                    }
                    $("#modalBody").append(modalBody);          
                }else{
                    img_ref.attr("src", image_available);
                    
                    $("[data-order="+ id +"]").remove();
                    $("[data-modal="+ id +"]").remove();

                    if($("#ticketOrder li").length == 0){
                        $("#ticketOrder").append('<li id="emptyCart" class="list-group-item d-flex justify-content-between lh-condensed"><h6 class="mt-1">Please add a ticket</h6></li>');
                    }
                }   
                $("#totalAmount").html("₱" + response.total_amount);

                $("#ticketOrder a").click(function(e){
                    e.preventDefault();
                    e.stopImmediatePropagation();

                    var info_href = $(this).attr("href");
                    var info_id = $(this).data('remove');

                    $.ajax({
                        type: "GET",
                        url: info_href,
                        success: function(response){
                            var img_info = $("img[id="+info_id+"]");

                            if(response.cart != 0){
                                $("#emptyCart").remove();
                                $("#checkout").removeClass("disabled");
                            }else{
                                $("#checkout").addClass("disabled");
                                $("#totalCart").remove();
                            }
                            $("#cart").html(response.cart);
                            if(img_info.attr("src") == image_available){
                                img_info.attr("src", image_selected);
                                
                            }else{
                                img_info.attr("src", image_available);
                                $("[data-order="+ info_id +"]").remove();
                                $("[data-modal="+ info_id +"]").remove();

                                if($("#ticketOrder li").length == 0){
                                    $("#ticketOrder").append('<li id="emptyCart" class="list-group-item d-flex justify-content-between lh-condensed"><h6 class="mt-1">Please add a ticket</h6></li>');
                                }
                            }
                            $("#totalAmount").html("₱" + response.total_amount);
                        }
                    });
                });
            }
        });
    });
    
    $("#ticketOrder a").click(function(e){
        e.preventDefault();
        e.stopImmediatePropagation();

        var info_href = $(this).attr("href");
        var info_id = $(this).data('remove');

        $.ajax({
            type: "GET",
            url: info_href,
            success: function(response){
                var img_info = $("img[id="+info_id+"]");

                if(response.cart != 0){
                    $("#emptyCart").remove();
                    $("#checkout").removeClass("disabled");
                }else{
                    $("#checkout").addClass("disabled");
                    $("#totalCart").remove();
                }
                
                $("#cart").html(response.cart);
                if(img_info.attr("src") == image_available){
                    img_info.attr("src", image_selected);
                    
                }else{
                    img_info.attr("src", image_available);
                    $("[data-order="+ info_id +"]").remove();
                    $("[data-modal="+ info_id +"]").remove();

                    if($("#ticketOrder li").length == 0){
                        $("#ticketOrder").append('<li id="emptyCart" class="list-group-item d-flex justify-content-between lh-condensed"><h6 class="mt-1">Please add a ticket</h6></li>');
                    }
                }
                $("#totalAmount").html("₱" + response.total_amount);
            }
        });
    });
});