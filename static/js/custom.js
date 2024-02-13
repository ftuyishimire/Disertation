$(document).ready(function () {
    $('.increment-btn').click(function (e) {
        e.preventDefault();

        var inc_value = $(this).closest('.product_data').find('.qty-input').val();
        var value = parseInt(inc_value, 10);
        value = isNaN(value) ? 0 : value;
        if (value < 10) {
            value++;
            $(this).closest('.product_data').find('.qty-input').val(value);
        }
    });

    $('.decrement-btn').click(function (e) {
        e.preventDefault();

        var dec_value = $(this).closest('.product_data').find('.qty-input').val();
        var value = parseInt(dec_value, 10);
        value = isNaN(value) ? 0 : value;
        if (value > 1) {
            value--;
            $(this).closest('.product_data').find('.qty-input').val(value);
        }
    });

    $('.addToCartBtn').click(function (e) {
        e.preventDefault();
    
        // Find the closest .product_data container
        var productContainer = $(this).closest('.product_data');
    
        // Find product_id and product_qty within the productContainer
        var product_id = productContainer.find('.prod_id').val();
        var product_qty = productContainer.find('.qty-input').val();
    
        // Check if the product_id and product_qty are found
        if (!product_id || !product_qty) {
            console.error('Product information not found.');
            return;
        }
    
        var token = $('input[name=csrfmiddlewaretoken]').val();
    
        // Disable the button during the AJAX request
        $(this).prop('disabled', true);
    
        $.ajax({
            method: "POST",
            url: "/add-to-cart",
            data: {
                'product_id': product_id,
                'product_qty': product_qty,
                csrfmiddlewaretoken: token
            },
            success: function (response) {
                console.log(response);
                alertify.success(response.status);
            },
            error: function (xhr, textStatus, errorThrown) {
                console.error("Error adding to cart:", errorThrown);
            },
            complete: function () {
                // Re-enable the button after the AJAX request is complete
                $(this).prop('disabled', false);
            }
        });
    });
    

    $('.addToWishlist').click(function (e) {
        e.preventDefault();
    
        // Find the closest .product_data container
        var productContainer = $(this).closest('.product_data');
    
        // Find product_id within the productContainer
        var product_id = productContainer.find('.prod_id').val();
    
        // Check if the product_id is found
        if (!product_id) {
            console.error('Product ID not found.');
            return;
        }
    
        var token = $('input[name=csrfmiddlewaretoken]').val();
    
        // Store $(this) in a variable
        var $wishlistButton = $(this);
    
        // Disable the button during the AJAX request
        $wishlistButton.prop('disabled', true);
    
        $.ajax({
            method: "POST",
            url: "/add-to-wishlist",
            data: {
                'product_id': product_id,
                csrfmiddlewaretoken: token
            },
            success: function (response) {
                alertify.success(response.status);
            },
            error: function (xhr, textStatus, errorThrown) {
                console.error("Error adding to wishlist:", errorThrown);
            },
            complete: function () {
                // Re-enable the button after the AJAX request is complete
                $wishlistButton.prop('disabled', false);
            }
        });
    });
    
    
    

    $('.changeQuantity').click(function (e){
        e.preventDefault();

        var product_id = $(this).closest('.product_data').find(' .prod_id ').val();
        var product_qty = $(this).closest('.product_data').find(' .qty-input ').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            method: "POST",
            url: "/updatecart",
            data: {
                'product_id': product_id,
                'product_qty': product_qty,
                csrfmiddlewaretoken: token
            },
            success: function (response) {
                // alertify.success(response.status)
            }
        })

    });
    
    $(document).on('click', '.delete-cart-item', function (e) {
        e.preventDefault();

        var product_id = $(this).closest('.product_data').find(' .prod_id ').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            method: "POST",
            url: "/delete-cart-item",
            data: {
                'product_id': product_id,
                csrfmiddlewaretoken: token
            },
            success: function(response){
                alertify.success(response.status)
                $('.cartdata').load(location.href + " .cartdata");
            }
        });
    });

    $('.delete-wishlist-item').click(function (e) {
        e.preventDefault();
    
        // Find the closest .product_data container
        var productContainer = $(this).closest('.product_data');
    
        // Find product_id within the productContainer
        var product_id = productContainer.find('.prod_id').val();
    
        // Check if the product_id is found
        if (!product_id) {
            console.error('Product ID not found.');
            return;
        }
    
        var token = $('input[name=csrfmiddlewaretoken]').val();
    
        // Disable the button during the AJAX request
        $(this).prop('disabled', true);
    
        $.ajax({
            method: "POST",
            url: "/delete-wishlist-item",
            data: {
                'product_id': product_id,
                csrfmiddlewaretoken: token
            },
            success: function (response) {
                alertify.success(response.status);
                $('.wishdata').load(location.href + " .wishdata");
            },
            error: function (xhr, textStatus, errorThrown) {
                console.error("Error deleting from wishlist:", errorThrown);
                console.log(xhr.responseText);  // Log the full response text for more details
            },
            complete: function () {
                // Re-enable the button after the AJAX request is complete
                $(this).prop('disabled', false);
            }
        });
    });
    
    

    $('#paypal-button').click(function (e) {
        e.preventDefault();

        // Make an AJAX request to the 'paypalcheckout' view to get the total price
        $.ajax({
            method: "GET",
            url: "/paypalcheckout",
            success: function (response) {
                // Call the PayPal API to initiate the payment
                paypal.Buttons({
                    createOrder: function (data, actions) {
                        return actions.order.create({
                            purchase_units: [
                                {
                                    amount: {
                                        value: response.total_price,
                                    },
                                },
                            ],
                        });
                    },
                    onApprove: function (data, actions) {
                        return actions.order.capture().then(function (details) {
                            // Payment is successful, you can redirect or handle it as needed
                            alert('Payment successful! Transaction ID: ' + details.id);
                        });
                    },
                }).render('#paypal-button-container'); // Render the PayPal button
            },
        });
    });
    
});
