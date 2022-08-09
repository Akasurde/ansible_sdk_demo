function sayHello(ipAddress) {
    alert(ipAddress);
    $.ajax({
        type: "POST",
        url: "/ping_host",

        // set content type header to use Flask response.get_json()
        contentType: "application/json",

        // convert data/object to JSON to send
        data: JSON.stringify({ipAddress: ipAddress}),

        // expect JSON data in return (e.g. Flask jsonify)
        dataType: "json",

        // handle response
        success: function(response) {
            console.log(response);
        },
        error: function(err) {
            console.log(err);
        }
      });


}

