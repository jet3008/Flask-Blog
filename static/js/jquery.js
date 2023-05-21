// const { event } = require("jquery");

$(document).ready(function() {

    console.log("codigo facilito")
    var messages = "{{ get_flashed_messages() }}";

    $(".producto").on('click', function(event) {
        var vote = $(this).data('badges');
        console.log(vote);

        $.ajax({
            type: 'POST',
            url: '/addCart',
            // contentType: 'application/json;charset=UTF-8',
            data: { 'data': vote },
            success: function(response) {
                var data = JSON.parse(response);
                // console.log(data)
                // console.log(data['html'])
                console.log(jQuery.type(data['html']))
                $("#tableBody").empty();
                $('#tableBody').prepend(data['html']);
            },
            error: function(error) {
                console.log(error)
            }
        })

    });

    $("#cartShow").on('click', function(event) {
        // console.log("cartShow");
        $.ajax({
            type: 'POST',
            url: '/displaycart',
            // data: { 'data': 1 },
            success: function(response) {
                var data = JSON.parse(response);
                // console.log(data)
                // console.log(data['html'])
                // console.log(jQuery.type(data['html']))
                $("#tableBody").empty();
                $('#tableBody').append(data['html']);
                $('#cart').modal('show');
            },
            error: function(error) {
                // console.log(error)
            }
        })
    });

    $("#tableBody").on("click", ".deleterow", function() { //use this way when the html is generated
        // alert("success");
        var productId = $(this).data('badges');
        $(this).closest('tr').remove();
        $.ajax({
            type: 'POST',
            url: '/deleteProduct',
            data: { 'data': productId },
            success: function(response) {
                console.log("entro aqui")
                $(this).closest('tr').remove();
                // $('#tableCart tr:last').after('<tr>...</tr><tr>...</tr>');
            },
            error: function(error) {
                console.log(error)
            }
        })
    });

    // $(".deleterow").click(function() {
    //     console.log("deleterow");
    //     var index = $(this).index();
    //     idProducto = $(this).closest('tr').attr('data-badges');
    // });
    function listen(get) {
        console.log("entro al delete")
    }

    if (typeof messages != 'undefined' && messages != '[]') {
        $('#myModal').modal('toggle');
    };

    function ajax_login() {
        console.log("entre al ajax$");
        $.ajax({
            url: '/ajax-login',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response)
            },
            error: function(error) {
                console.log(error)
            }
        })
    }


    // $( "#login-form" ).on( "submit", function( event ) {
    //     // console.log( $( this ).serialize() );
    //     event.preventDefault();
    //     ajax_login();
    //   });


});

let x = document.querySelectorAll(".moneyFormat");
for (let i = 0, len = x.length; i < len; i++) {
    let num = Number(x[i].innerHTML)
        .toLocaleString('en');
    x[i].innerHTML = num;
    x[i].classList.add("currSign");
}