let maps_is_visible = true;

let canvas;
let questions_panel;
let ctx;

let data;
let height_in_km;
let width_in_km;
let top_right_coordinate_display;
let top_left_scale_display;
let bottom_right_stop_name_display;
let bottom_left_click_coordinate_display;
let selected_bus_stop_i = -1;
const MIN_ZOOM = 0.00001;
const MAX_ZOOM = 0.00008;
let zoom_value = MAX_ZOOM; // deg / px
const MIN_LON = 11.256635603112843;
const MAX_LON = 11.365479808365757;
const MIN_LAT = 44.47267601010103;
const MAX_LAT = 44.50946314343433;
let pointing_lon = 11.34310;
let pointing_lat = 44.49375;

const bologna_satellite = new Image;
let bologna_satellite_loaded = false;

let kinetic_scrolling_speed = 0;
let kinetic_scrolling_friction = -0.05;
let kinetic_scrolling_min_speed = 5.0;

let bus_stop_radius = 2;

document.addEventListener('DOMContentLoaded', function() {
    canvas = document.getElementById("myCanvas");
    questions_panel = document.getElementById("questions_panel");
    fetchJSONData();
    top_right_coordinate_display = document.getElementById("top_right_coordinate_display");
    top_left_scale_display = document.getElementById("top_left_scale_display");
    bottom_right_stop_name_display = document.getElementById("bottom_right_stop_name_display");
    bottom_left_click_coordinate_display = document.getElementById("bottom_left_click_coordinate_display");

    bologna_satellite.src = "./Bologna.jpg";
    bologna_satellite.onload = function() {
        bologna_satellite_loaded = true;
        console.log("Loaded Bologna.jpg!")
        draw_data();
    }


    canvas.addEventListener("click", function(event) {
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
    });
    let pointer_down_start_x;
    let pointer_down_start_y;
    let pointer_down_pointing_lon;
    let pointer_down_pointing_lat;
    let mouse_is_pressed;

    let pointers = [];
    let initialDistance = 0;
    let starting_scroll;
    let start_y;
    let start_t;
    let last_t;
    let last_y;

    canvas.addEventListener("pointerdown", function(event) {
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
    });

    canvas.addEventListener("pointermove", function(event) {
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
            draw_data();
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
            draw_data();
        }
    });

    canvas.addEventListener("pointerup", function(event) {
        mouse_is_pressed = false;

        // pinch-to-zoom
        pointers = pointers.filter(p => p.pointerId !== event.pointerId);

        if (pointers.length < 2) {
            initialDistance = 0;
        }
    });

    canvas.addEventListener("pointercancel", function(event) {
        mouse_is_pressed = false;

        // pinch-to-zoom
        pointers = pointers.filter(p => p.pointerId !== event.pointerId);

        if (pointers.length < 2) {
            initialDistance = 0;
        }
    });

    canvas.addEventListener("wheel", function(event) {
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
    });

    questions_panel.addEventListener("click", function(event){
        // console.log("Suca");
        // questions_panel.scrollTo({
        //  top: 100,
        //  behavior: "smooth"
        //});
    });

    questions_panel.addEventListener("pointerdown", function(event) {
        start_y = event.clientY;
        start_t = Date.now() / 1000;
        last_t = start_t;
        last_y = start_y;
        mouse_is_pressed = true;
        starting_scroll = questions_panel.scrollTop;
        kinetic_scrolling_speed  = 0;
    });

    questions_panel.addEventListener("pointermove", function(event) {
        if (!mouse_is_pressed) return;
        let this_y = event.clientY;
        let this_t = Date.now() / 1000;
        kinetic_scrolling_speed = (this_y - last_y) / (this_t - start_t);
        questions_panel.scrollTo({
          top: starting_scroll+(-this_y+start_y),
          behavior: "instant"
        });
        last_y = this_y;
        last_t = this_t;
    });

    questions_panel.addEventListener("pointerup", function(event) {
        mouse_is_pressed = false;
        scroll_kinetic()
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
        if (bologna_satellite_loaded){
            print_bologna_in_correct_position(ctx, canvas.width, canvas.height);
            console.log(zoom_value)
        }
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
        questions_panel.style.visibility = "visible"
    }else{
        maps_is_visible = true;
        canvas.style.visibility = "visible";
        let question_map = document.getElementById("question_map");
        question_map.innerHTML = "Domande"
        questions_panel.style.visibility = "hidden"
    }
}

// 4028, 1009 --> 11.342787 44.494055
// 3000, 514 --> 11.320800 44.501614
const m_lat_to_y = (1009 - 514) / (44.494055 - 44.501614);
const q_lat_to_y = (44.494055*514 - 44.501614*1009) / (44.494055  - 44.501614);
const m_lon_to_x = (4028 - 3000) / (11.342787 - 11.320800);
const q_lon_to_x = (11.342787 *3000 - 11.320800*4028) / (11.342787 - 11.320800);

function lat_to_y_image(lat){
    return lat*m_lat_to_y  + q_lat_to_y;
}

function lon_to_x_image(lon){
    return lon*m_lon_to_x  + q_lon_to_x;
}

function y_image_to_lat(y){
    return (y-q_lat_to_y)/m_lat_to_y;
}

function x_image_to_lon(x){
    return (x-q_lon_to_x)/m_lon_to_x;
}


function print_bologna_in_correct_position(ctx, width, height){
    let lon_top_left_canvas = x_to_lon(0);
    let lat_top_left_canvas = y_to_lat(0);
    let lon_top_left_image = x_image_to_lon(0);
    let lat_top_left_image = y_image_to_lat(0);

    let lon_bottom_right_canvas = x_to_lon(canvas.width);
    let lat_bottom_right_canvas = y_to_lat(canvas.height);
    let lon_bottom_right_image = x_image_to_lon(bologna_satellite.width);
    let lat_bottom_right_image = y_image_to_lat(bologna_satellite.height);

    let sx;
    let sy;
    let sWidth;
    let sHeight;
    let dx;
    let dy;
    let dWidth;
    let dHeight;


    if (lon_top_left_canvas < lon_top_left_image){
        sx = 0;
        dx = lon_to_x(lon_top_left_image);

    }else{
        sx = lon_to_x_image(lon_top_left_canvas);
        dx = 0;
    }

    if (lat_top_left_canvas > lat_top_left_image){
        sy = 0;
        dy = lat_to_y(lat_top_left_image);

    }else{
        sy = lat_to_y_image(lat_top_left_canvas);
        dy = 0;
    }

    if (lon_bottom_right_canvas > lon_bottom_right_image){
        sWidth = bologna_satellite.width - sx;
        dWidth = lon_to_x(lon_bottom_right_image) - dx;
    }else{
        sWidth = lon_to_x_image(lon_bottom_right_canvas) - sx;
        dWidth = canvas.width - dx;
    }

    if (lat_bottom_right_canvas < lat_bottom_right_image){
        sHeight = bologna_satellite.height - sy;
        dHeight = lat_to_y(lat_bottom_right_image) - dy;
    }else{
        sHeight = lat_to_y_image(lat_bottom_right_canvas) - sy;
        dHeight = canvas.height - dy;
    }
    ctx.drawImage(bologna_satellite, sx, sy, sWidth, sHeight, dx, dy, dWidth, dHeight);
}

function scroll_kinetic(){
    if (Math.abs(kinetic_scrolling_speed) > kinetic_scrolling_min_speed){

        kinetic_scrolling_speed = kinetic_scrolling_friction*kinetic_scrolling_speed+kinetic_scrolling_speed;
        console.log(kinetic_scrolling_speed)
        questions_panel.scrollBy({
            top: -kinetic_scrolling_speed/10,
            behavior: "instant"
        });
        setTimeout(scroll_kinetic, 10);
    }else{
        kinetic_scrolling_speed  = 0;
    }
}