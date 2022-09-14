
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

function hide(elements) {
    elements = elements.length ? elements : [elements];
    for (var index = 0; index < elements.length; index++) {
        elements[index].style.display = 'none';
    }
}

function show_success(powerstate, response) {
    document.getElementById('success_info_modal').style.display = 'inline';
    document.getElementById('success_info_message_box').innerHTML = "Successfully " + powerstate + " " + response.ipAddress
}

function hide_success_info_modal() {
    document.getElementById('success_info_modal').style.display = 'none';
}


function show_error(powerstate, response) {
    document.getElementById('error_info_modal').style.display = 'inline';
    document.getElementById('error_info_message_box').innerHTML = "Something went wrong"
}

function hide_error_info_modal() {
    document.getElementById('error_info_modal').style.display = 'none';
}


function powerstate_host(ipAddress, machine_name, machine_type, zone, project, powerstate) {
    document.getElementById('progress_modal').style.display = 'inline';
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
                document.getElementById('progress_modal').style.display = 'none';
                show_success(powerstate, response);
            } else {
                document.getElementById('progress_modal').style.display = 'none';
                show_error();
            }
        },
        error: function (err) {
            console.log(err);
        }
    });
}