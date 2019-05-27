$(document).ready(function () {

    guest = JSON.parse(document.getElementById("guest_json").textContent);
    $("#guest_display_name").append("<b>Name: </b>" + guest.display_name);

    var ws_scheme = "wss://";
    if (window.location.protocol == "http:") {
        ws_scheme = "ws://";
    }

    var gyronormMotionSender = {
        gn: new GyroNorm(),
        init: function (handler) {
            this.handler = handler;
            this.gn.init({});
        },
        start: function () {
            this.gn.start(function (data) {
                this.handler(data.do);
            });
        },
        stop: function () {
            this.gn.stop();
        },
    };

    var nativeMotionSender = {
        init: function (handler) {
            return this;
        },
        start: function () {
            window.ondeviceorientation = handler;
        },
        stop: function () {
            window.ondeviceorientation = null;
        }
    };

    function getMotionSender(motion_type) {
        handler = function (data) {
            console.log(data);
            motion_socket.send(JSON.stringify({
                guest: { display_name: guest.display_name },
                euler: {
                    alpha: data.alpha,
                    beta: data.beta,
                    gamma: data.gamma
                }
            }));
            debug_interface.update_motion_data(data);
        };

        switch (motion_type) {
            case "native_euler":
                return nativeMotionSender.init(handler);
            case "gyronorm_euler":
                return gyronormMotionSender.init(handler);
            default:
                return nativeMotionSender.init(handler);
        }
    }

    var DEBUG = true;
    var motion_socket = null;
    var motion_sender = null;

    var guest_socket = new WebSocket(ws_scheme + window.location.host + "/ws/guest/");
    guest_socket.onopen = function (event) {
        console.log('guest_socket.onopen', event);
    };
    guest_socket.onmessage = function (event) {
        console.log('guest_socket.onmessage', event);
        data = JSON.parse(event.data);
        motion_sender = getMotionSender();

        // if (data.queue[0].session_key === guest.session_key) {
        //     console.log('Enabling interact mode', data.queue[0]);
        //     enableInteractMode(data.queue);
        // } else {
        //     console.log('Enabling queue mode', data.queue);
        //     enableQueueMode(data.queue);
        // }

        // switch (data.method) {
        //     case data.method:
        //         return nativeMotionSender.init(handler);
        //     case "gyronorm_euler":
        //         return gyronormMotionSender.init(handler);
        //     default:
        //         return nativeMotionSender.init(handler);
        // }

        // Temp code
        // $("#guest_display_name").append("<b>Name: </b>" + guest.display_name);
        enableQueueMode(data.queue_state);

    };
    guest_socket.onclose = function (event) {
        console.log('guest_socket.onclose', event);
        clean_exit();
    };
    guest_socket.onerror = function (event) {
        console.log('guest_socket.onerror', event);
    };

    function enableQueueMode(queue_state) {
        $("#queue_ui").show();
        $("#interact_ui").hide();
        populateQueueTable(queue_state);
    }

    function enableInteractMode(queue_state) {
        $("#queue_ui").hide();

        motion_socket = new WebSocket(ws_scheme + window.location.host + "/ws/motion/");
        motion_socket.onopen = function (event) {
            console.log('motion_socket.onopen', event);

            $("#start").click(function (e) {
                $(this).hide();
                $("#stop").show();
                motion_sender.start();
            });

            $("#stop").click(function (e) {
                $(this).hide();
                $("#start").show();
                motion_sender.stop();
            });

            $("#exit").click(function (e) {
                motion_sender.stop();
                guest_socket.close();
                motion_socket.close();
                redirect_to_exit();
            });

            $("#interact_ui").show();
            // debug_interface.reveal_queue_ui(queue_state);
        };
        motion_socket.onmessage = function (event) {
            console.log('motion_socket.onmessage:', event);
        };
        motion_socket.onclose = function (event) {
            console.log('motion_socket.close', event);
        };
        motion_socket.onclose = function (event) {
            console.log('motion_socket.onclose', event);
        };
        motion_socket.onerror = function (event) {
            console.log('motion_socket.onerror', event);
        };
    }

    function clean_exit() {
        if (motion_sender != null) { motion_sender.stop(); }
        if (motion_socket != null) { motion_socket.close(); }
        if (guest_socket != null) { guest_socket.close(); }
        window.location.href = "/exit/";
    }

    function populateQueueTable(queue_state) {
        console.log(queue_state);
        table_body = $("#queue_table_body");
        table_body.empty();
        for (var index in queue_state) {
            var item = queue_state[index];
            var row = $("<tr/>");
            row.append("<td>" + index + "</td>");
            row.append("<td>" + item.display_name + "</td>");
            row.append("<td>" + item.session_key + "</td>");
            row.append("</tr>");
            table_body.append(row);
        }

    }

    function DebugInterface(enable) {
        this.update_motion_data = function (data) { };
        this.reveal_queue = function (queue_state) { };
        if (enable) {
            // API
            this.update_motion_data = function (data) {
                for (var key in (data)) {
                    if (typeof data[key] == 'number') {
                        $("#motiondata_" + key).text(data[key].toFixed(2));
                    } else {
                        $("#motiondata_" + key).text(data[key]);
                    }
                }
            };
        }

        this.reveal_queue_ui = function (queue_state) {
            populateQueueTable(queue_state);
            $("#queue_ui").show();
        };

        // UI
        $("#queue_ui_button").click(function () {
            $("#queue_ui").show();
        });
        $("#interact_ui_button").click(function () {
            enableQueueMode();
        });
        $("#debug").css('display', 'inline');
        $("#debug").show();
    }

    debug_interface = new DebugInterface(DEBUG);
});