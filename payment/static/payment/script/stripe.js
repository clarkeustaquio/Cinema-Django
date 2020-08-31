var checkOutButton = document.getElementById('checkout-button');
    checkOutButton.addEventListener('click', function(){
        stripe.redirectToCheckout({
            sessionId:  session
        }).then(function (result){
        });
    });

var checkOutButtonMobile = document.getElementById('checkout-button-mobile');
    checkOutButtonMobile.addEventListener('click', function(){
        stripe.redirectToCheckout({
            sessionId:  session
        }).then(function (result){
        });
    });