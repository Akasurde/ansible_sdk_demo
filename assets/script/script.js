function ping_host(ipAddress) {
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

            if (response.success) {
                alert(response.response.ping);
            } else {
                alert("Something went wrong");
            }
        },
        error: function(err) {
            console.log(err);
        }
    });
}

function powerstate_host(ipAddress, machine_name, machine_type, zone, project, powerstate) {
    $.ajax({
        type: "POST",
        url: "/powerstate_host",

        // set content type header to use Flask response.get_json()
        contentType: "application/json",

        // convert data/object to JSON to send
        data: JSON.stringify({
            ipAddress: ipAddress,
            machine_name: machine_name,
            machine_type: machine_type,
            zone: zone,
            project: project,
            powerstate: powerstate
        }),

        // expect JSON data in return (e.g. Flask jsonify)
        dataType: "json",

        // handle response
        success: function (response) {
            console.log(response);

            if (response.success) {
                alert(response);
            } else {
                alert("Something went wrong");
            }
        },
        error: function (err) {
            console.log(err);
        }
    });
}