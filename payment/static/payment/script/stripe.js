var checkOutButton = document.getElementById('checkout-button');
    checkOutButton.addEventListener('click', function(){
        stripe.redirectToCheckout({
            sessionId:  session
        }).then(function (result){
        });
    });