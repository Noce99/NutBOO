let maps_is_visible = true;

let canvas;
let ctx;
let zoom_value = 0.001; // deg / px
let data;
let pointing_lon = 11.34310;
let pointing_lat = 44.49375;
let height_in_km;
let width_in_km;
let top_right_coordinate_display;
let top_left_scale_display;
let bottom_right_stop_name_display;
let bottom_left_click_coordinate_display;
let selected_bus_stop_i = -1;
const MIN_ZOOM = 0.00001;
const MAX_ZOOM = 0.005;
const MIN_LON = 11.21;
const MAX_LON = 11.45;
const MIN_LAT = 44.4;
const MAX_LAT = 44.57;

document.addEventListener('DOMContentLoaded', function() {
    canvas = document.getElementById("myCanvas");
    fetchJSONData();
    top_right_coordinate_display = document.getElementById("top_right_coordinate_display");
    top_left_scale_display = document.getElementById("top_left_scale_display");
    bottom_right_stop_name_display = document.getElementById("bottom_right_stop_name_display");
    bottom_left_click_coordinate_display = document.getElementById("bottom_left_click_coordinate_display");
    canvas.addEventListener("click", function(event) {
        if (maps_is_visible) {
            const rect = canvas.getBoundingClientRect();
            const x = event.clientX - rect.left;
            const y = event.clientY - rect.top;

            const lat = y_to_lat(y);
            const lon = x_to_lon(x);

            let min = 0;
            let min_i = -1;
            for (let i = 0; i < data.length; i++) {
                let distance = Math.abs(lat - parseFloat(data[i].lat)) + Math.abs(lon - parseFloat(data[i].lon));
                if (min_i === -1 || distance < min) {
                    min_i = i;
                    min = distance;
                }
            }
            bottom_right_stop_name_display.innerHTML = data[min_i].name;
            bottom_left_click_coordinate_display.innerHTML = lat.toFixed(4) + " N " +
                lon.toFixed(4) + " E";
            selected_bus_stop_i = min_i;
            draw_data();

            ctx.beginPath();
            ctx.arc(x, y, 2, 0, 2 * Math.PI);
            ctx.closePath();
            ctx.fillStyle = 'rgb(241,229,162)';
            ctx.strokeStyle = 'rgb(241,229,162)';
            ctx.fill();
            ctx.stroke();
        }
    });
    let pointer_down_start_x;
    let pointer_down_start_y;
    let pointer_down_pointing_lon;
    let pointer_down_pointing_lat;
    let mouse_is_pressed;

    let pointers = [];
    let initialDistance = 0;

    canvas.addEventListener("pointerdown", function(event) {
        if (maps_is_visible) {
            pointer_down_start_x = event.clientX;
            pointer_down_start_y = event.clientY;
            mouse_is_pressed = true;
            pointer_down_pointing_lon = pointing_lon;
            pointer_down_pointing_lat = pointing_lat;

            // pinch-to-zoom
            pointers.push(event);

            if (pointers.length === 2) {
                initialDistance = getDistance(pointers[0], pointers[1]);
            }
        }
    });

    canvas.addEventListener("pointermove", function(event) {
        if (maps_is_visible) {
            if (pointers.length === 1) {
                if (!mouse_is_pressed) return;

                let end_x = event.clientX;
                let end_y = event.clientY;
                pointing_lon = pointer_down_pointing_lon + (pointer_down_start_x - end_x) * zoom_value;
                pointing_lat = pointer_down_pointing_lat - (pointer_down_start_y - end_y) * zoom_value;
                if (pointing_lon < MIN_LON) {
                    pointing_lon = MIN_LON;
                } else if (pointing_lon > MAX_LON) {
                    pointing_lon = MAX_LON;
                }
                if (pointing_lat < MIN_LAT) {
                    pointing_lat = MIN_LAT;
                } else if (pointing_lat > MAX_LAT) {
                    pointing_lat = MAX_LAT;
                }
            }

            // pinch-to-zoom
            for (let i = 0; i < pointers.length; i++) {
                if (pointers[i].pointerId === event.pointerId) {
                    pointers[i] = event;
                    break;
                }
            }

            if (pointers.length === 2) {
                // Calcola la distanza attuale e confrontala con quella iniziale
                const currentDistance = getDistance(pointers[0], pointers[1]);
                const scaleChange = currentDistance / initialDistance;
                zoom_value /= scaleChange;
                if (zoom_value < MIN_ZOOM) {
                    zoom_value = MIN_ZOOM;
                } else if (zoom_value > MAX_ZOOM) {
                    zoom_value = MAX_ZOOM;
                }
                initialDistance = currentDistance;
            }
            draw_data();
        }
    });

    canvas.addEventListener("pointerup", function(event) {
        if (maps_is_visible) {
            mouse_is_pressed = false;

            // pinch-to-zoom
            pointers = pointers.filter(p => p.pointerId !== event.pointerId);

            if (pointers.length < 2) {
                initialDistance = 0;
            }
        }
    });

    canvas.addEventListener("pointercancel", function(event) {
        if (maps_is_visible) {
            mouse_is_pressed = false;

            // pinch-to-zoom
            pointers = pointers.filter(p => p.pointerId !== event.pointerId);

            if (pointers.length < 2) {
                initialDistance = 0;
            }
        }
    });

    canvas.addEventListener("wheel", function(event) {
        if (maps_is_visible) {
            if (event.deltaY < 0) {
                zoom_value /= 2;
                if (zoom_value < MIN_ZOOM) {
                    zoom_value = MIN_ZOOM;
                }
            } else {
                zoom_value *= 2;
                if (zoom_value > MAX_ZOOM) {
                    zoom_value = MAX_ZOOM;
                }
            }
            draw_data();
        }
    });
});

function fetchJSONData() {
    ctx = canvas.getContext("2d");
    ctx.fillStyle = "red";
    fetch("data/bus_stops.json").then((res) => {
        if (!res.ok) {
                throw new Error(`HTTP error! Status: ${res.status}`);
        }
        return res.json();
    }).then((d) => {
        data=d;
        draw_data();
    }).catch((error) =>
        console.error("Unable to fetch data:", error)
    );
}

function lon_to_x(lon) {
    return (lon - pointing_lon) / zoom_value + canvas.width / 2;
}

function x_to_lon(x) {
    return (x - canvas.width / 2) * zoom_value + pointing_lon;
}

function lat_to_y(lat){
    return (-lat + pointing_lat) / zoom_value + canvas.height/2;
}

function y_to_lat(y) {
    return - ((y - canvas.height/2) * zoom_value - pointing_lat);
}

function draw_data(){
    if (maps_is_visible) {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        for (let i = 0; i < data.length; i++) {
            let radius, color;
            if (i === selected_bus_stop_i) {
                radius = 5;
                color = 'rgb(197,19,213)'
            } else {
                radius = 2;
                color = 'rgba(255, 0, 0, 1.0)'
            }
            ctx.beginPath();
            ctx.arc(lon_to_x(parseFloat(data[i].lon)), lat_to_y(parseFloat(data[i].lat)),
                radius, 0, 2 * Math.PI);
            ctx.closePath();
            ctx.fillStyle = color;
            ctx.fill();
        }
        ctx.beginPath();
        ctx.moveTo(canvas.width / 2 - 0.01 * canvas.width, canvas.height / 2);
        ctx.lineTo(canvas.width / 2 + 0.01 * canvas.width, canvas.height / 2);
        ctx.moveTo(canvas.width / 2, canvas.height / 2 - 0.01 * canvas.height);
        ctx.lineTo(canvas.width / 2, canvas.height / 2 + 0.01 * canvas.height);
        ctx.strokeStyle = "black";
        ctx.lineWidth = 1;
        ctx.stroke();

        // Let's update the coordinate displayed on top right corner
        top_right_coordinate_display.innerHTML = pointing_lat.toFixed(4) + " N\n" +
            pointing_lon.toFixed(4) + " E";
        height_in_km = canvas.height * zoom_value * 110.574;
        width_in_km = canvas.width * zoom_value * 111.320 * Math.cos(pointing_lat);
        top_left_scale_display.innerHTML = height_in_km.toFixed(2) + " km height <br> " +
            width_in_km.toFixed(2) + " km width\n ";
    }
}

function getDistance(p1, p2) {
    const dx = p2.clientX - p1.clientX;
    const dy = p2.clientY - p1.clientY;
    return Math.sqrt(dx * dx + dy * dy);
}

function map_questions_switch(){
    if (maps_is_visible) {
        maps_is_visible = false;
        canvas.style.visibility = "hidden";
        let question_map = document.getElementById("question_map");
        question_map.innerHTML = "Mappa"
        let questions_panel = document.getElementById("questions_panel");
        questions_panel.style.visibility = "visible"
    }else{
        maps_is_visible = true;
        canvas.style.visibility = "visible";
        let question_map = document.getElementById("question_map");
        question_map.innerHTML = "Domande"
        let questions_panel = document.getElementById("questions_panel");
        questions_panel.style.visibility = "hidden"
    }
}