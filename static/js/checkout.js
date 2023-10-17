$(document).ready(function () {

    $('.payWithRazorpay').click(function (e) {
        e.preventDefault();

        var fname = $("[name='fname']").val();
        var lname = $("[name='lname']").val();
        var email = $("[name='email']").val();
        var phone = $("[name='phone']").val();
        var address = $("[name='address']").val();
        var city = $("[name='city']").val();
        var state = $("[name='state']").val();
        var country = $("[name='country']").val();
        var pincode = $("[name='pincode']").val();

        if (fname == "" || lname == "" || email == "" || phone == ""|| address == "" || city == "" || state == "" || country == "" || pincode == "")
        {
            swal("Banza wiyandike!", "All fields are mandatory!", "error");
            return false;
        }
        else
        {
            $.ajax({
                method: "GET",
                url: "/proceed-to-pay",
                success: function (response) {
                    // console.log(response);
                    var options = {
                        "key": "YOUR_KEY_ID",// Enter the key ID generated from the Dashboard
                        "amount": "50000",
                        "currency": "FRw",
                        "name":"Acme Corp",
                        "description": "Test transaction",
                        "image": "https://example.com/your_logo",
                        "order_id": "order_Chezbs0984",
                        "handler": function (response){
                            alert(response.razorpay_payment_id);
                            alert(response.razorpay_order_id);
                            alert(response.razorpay_signature);
                        },
                        "prefill": {
                            "name": "fablo",
                            "email":"sbackend8@gmail.com",
                            "contact": "0789105277"
                        },
                        "notes": {
                            "address": "Razorpay Corporate Office"
                        },
                        "theme": {
                            "color": "#3399cc"
                        }
                    };
                    var rzp1 = new Razorpay(options);
                    rzp1.open();
                }
            });
          
        }


        
    });
})