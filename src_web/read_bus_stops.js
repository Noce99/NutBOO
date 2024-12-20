// CALIBRATION
const px_x_1 = 0;
const px_y_1 = 0;
const px_x_2 = 2182;
const px_y_2 = 1435;
const lat_1 = 44.5212535;
const lon_1 = 11.2610802;
const lat_2 = 44.47755;
const lon_2 = 11.35404;
// END CALIBRATION


const SERVER_IP = "boo.nutlab.it" //"137.204.57.32"
const HTTPS = "https://";
const PORT = "5000";

let passcode;
let team_name;

let maps_is_visible = true;

let canvas;
let questions_panel;
let ctx;

let data;
let loaded_data = false;

let height_in_km;
let width_in_km;

let selected_bus_stop_name;
let sizes_of_the_map;

let selected_stop = -1;
const MIN_ZOOM = 0.00001;
// const MAX_ZOOM =  0.001; // To see Sasso
const MAX_ZOOM =  0.00015; // Default
let zoom_value = MAX_ZOOM; // deg / px
const MIN_LON = 11.2610802;
const MAX_LON = 11.366352213;
const MIN_LAT = 44.464637655;
const MAX_LAT = 44.5212535;
let pointing_lon = 11.34310;
let pointing_lat = 44.49375;

const train_stops = [
    {"lat": 44.47450846747514, "lon": 11.276196994362591, "name": "CASALECCHIO DI RENO"},
    {"lat": 44.48275908146947, "lon": 11.27289656088133, "name": "CASALECCHIO GARIBALDI"},
    {"lat": 44.50375079472428, "lon": 11.27468635485313, "name": "CASTEL DEBOLE"},
    {"lat": 44.515036291999195, "lon": 11.284783688952498, "name": "BORGO PANIGALE"},
    {"lat": 44.5058753612949, "lon": 11.343379184001565, "name": "BOLOGNA CENTRALE"},
    {"lat": 44.48156522412027, "lon": 11.262735588326326, "name": "CASALECCHIO CERETOLO"}
]

const bologna_satellite = new Image;
let bologna_satellite_loaded = false;

let kinetic_scrolling_speed = 0;
let kinetic_scrolling_friction = -0.05;
let kinetic_scrolling_min_speed = 5.0;

let bus_stop_minimum_radius = 2;
let bus_stop_maximum_radius = 5;
let bus_stop_radius_m = (bus_stop_minimum_radius - bus_stop_maximum_radius) / (MAX_ZOOM - MIN_ZOOM);
let bus_stop_radius_q = (MAX_ZOOM*bus_stop_maximum_radius - MIN_ZOOM*bus_stop_minimum_radius) / (MAX_ZOOM - MIN_ZOOM);
let bus_stop_radius = bus_stop_minimum_radius;

let map_names_minimum_size = 13;
let map_names_maximum_size = 50;
let map_names_size_m = (map_names_minimum_size - map_names_maximum_size) / (MAX_ZOOM - MIN_ZOOM);
let map_names_size_q = (MAX_ZOOM*map_names_maximum_size - MIN_ZOOM*map_names_minimum_size) / (MAX_ZOOM - MIN_ZOOM);
let map_name_size = map_names_minimum_size;

let map_left, map_top, map_right, map_bottom;

let image_questions_id = [];

let MAPS = [];


const gps_time_options = {
  year: 'numeric',
  month: 'numeric',
  day: 'numeric',
  hour: '2-digit',
  minute: '2-digit',
  second: '2-digit'
};

gpses_to_print = []

let selected_stop_is_a_train = false;
let selected_team;

document.addEventListener('DOMContentLoaded', function() {
    fetchJSONData();
    const url_parameters = new URLSearchParams(window.location.search);
    let a_team_name = document.getElementById("team_name");
    a_team_name.innerHTML = url_parameters.get("team_name")
    team_name = url_parameters.get("team_name")
    passcode = url_parameters.get("passcode")
    if (team_name === "Admin"){
        admin_Setup();
    }else{
        fetchJSONQuestions();
    }

    canvas = document.getElementById("myCanvas");
    ctx = canvas.getContext("2d");
    draw_data();
    questions_panel = document.getElementById("questions_panel");

    selected_bus_stop_name = document.getElementById("selected_bus_stop_name");
    selected_bus_stop_name.innerHTML = "Select a Bus Stop (Red Dots)!"
    sizes_of_the_map = document.getElementById("sizes_of_the_map");

    bologna_satellite.src = "./Sfondosfocatissimo_epsg4326.jpg";
    bologna_satellite.onload = function() {
        bologna_satellite_loaded = true;
        console.log("Loaded Sfondosfocatissimo_epsg4326.jpg!")
        draw_data();
    }

    let map_rect = canvas.getBoundingClientRect();
    map_left = map_rect.left;
    map_top = map_rect.top;
    map_right = map_rect.right;
    map_bottom = map_rect.bottom;

    if (team_name !== "Test") {
        setTimeout(ask_for_live_gps, 500);
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
        let minimum_distance_bus = min;
        let minimum_distance_name = data[min_i].name;
        let min_train = 0;
        let min_train_i = -1
        for (let i=0; i < train_stops.length; i++) {
            let distance = Math.abs(lat - parseFloat(train_stops[i].lat)) + Math.abs(lon - parseFloat(train_stops[i].lon));
            if (min_train_i === -1 || distance < min_train) {
                min_train_i = i;
                min_train = distance;
            }
        }
        if (min_train < minimum_distance_bus){
            minimum_distance_name = train_stops[min_train_i].name;
            selected_bus_stop_name.style.color = 'rgb(8,197,16)';
            selected_stop_is_a_train = true;
            selected_stop = min_train_i;
        }else{
            selected_bus_stop_name.style.color = 'rgb(255,118,0)';
            selected_stop_is_a_train = false;
            selected_stop = min_i;
        }
        selected_bus_stop_name.innerHTML = minimum_distance_name;

        // console.log(lat.toFixed(4) + " N " + lon.toFixed(4) + " E"); // SELECTED BUS COORDINATE
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
            const currentDistance = getDistance(pointers[0], pointers[1]);
            const scaleChange = currentDistance / initialDistance;
            zoom_value /= scaleChange;
            if (zoom_value < MIN_ZOOM) {
                zoom_value = MIN_ZOOM;
            } else if (zoom_value > MAX_ZOOM) {
                zoom_value = MAX_ZOOM;
            }
            bus_stop_radius = zoom_value*bus_stop_radius_m + bus_stop_radius_q;
            map_name_size = zoom_value*map_names_size_m + map_names_size_q;
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
        bus_stop_radius = zoom_value*bus_stop_radius_m + bus_stop_radius_q;
        map_name_size = zoom_value*map_names_size_m + map_names_size_q;
        draw_data();
    });

    canvas.addEventListener("mouseleave", function(event) {
        mouse_is_pressed = false;
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
        if (event.clientX < map_left || event.clientX > map_right || event.clientY < map_top || event.clientY > map_bottom){
            mouse_is_pressed = false;
            kinetic_scrolling_speed = 0;
            return;
        }
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

    questions_panel.addEventListener("pointercancel", function(event) {
        mouse_is_pressed = false;
        kinetic_scrolling_speed = 0;
    });
});

function fetchJSONData() {
    fetch("data/bus_stops.json").then((res) => {
        if (!res.ok) {
                throw new Error(`HTTP error! Status: ${res.status}`);
        }
        return res.json();
    }).then((d) => {
        data=d;
        loaded_data = true;
    }).catch((error) =>
        console.error("Unable to fetch data:", error)
    );
}

async function admin_Setup(){
    const response = await fetch(`${HTTPS}${SERVER_IP}:${PORT}/get_teams`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({"passcode": passcode})
    });
    if (response.status === 200) {
        const teams_name = await response.json();
        let divElement = document.getElementById("questions_panel");
        const newH1 = document.createElement("h1");
        newH1.innerHTML = "Select a team:";
        divElement.appendChild(newH1);
        const newSelect = document.createElement("select");
        for (let i=0; i<teams_name.length; i++){
            const newOption = document.createElement("option");
            newOption.value = teams_name[i];
            newOption.text = teams_name[i];
            newSelect.add(newOption);
            newSelect.addEventListener("change", function(event) {
              selected_team = event.target.value;
              fetchJSONAnswers();
            });
        }
        selected_team = newSelect.value;
        divElement.appendChild(newSelect);
        fetchJSONQuestions();
    }
}

let answer_to_send = {}

async function fetchJSONQuestions() {
    const response = await fetch(`${HTTPS}${SERVER_IP}:${PORT}/questions`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({"passcode": passcode})
    });
    if (response.status === 200) {
        const qa = await response.json();
        let divElement = document.getElementById("questions_panel");

        image_questions_id.length = 0;
        for (let i = 0; i < qa.length; i++) {
            const newH1 = document.createElement("h1");
            newH1.innerHTML = "Domanda " + qa[i]["question_id"].toString() + ":";
            const newP = document.createElement("p");
            newP.innerHTML = qa[i]["question"].toString();
            divElement.appendChild(newH1);
            divElement.appendChild(newP);

            if (qa[i]["type_of_answer"] === "text") {
                const newI = document.createElement("input");
                newI.type = "text";
                newI.classList.add("answer");
                newI.id = "answer_" + qa[i]["question_id"].toString();
                newI.addEventListener("input", function () {
                    const now = Date.now()
                    answer_to_send[qa[i]["question_id"]] = now
                    setTimeout(send_answer, 1000, passcode, qa[i]["question_id"], newI.value, now);
                });

                divElement.appendChild(newI);
            } else {
                image_questions_id.push(qa[i]["question_id"].toString());
                const newI = document.createElement("input");
                newI.type = "file";
                newI.classList.add("answer_file");
                newI.id = "answer_" + qa[i]["question_id"].toString();
                newI.addEventListener("change", function (event) {
                    upload_file(newI, qa[i]["question_id"]);
                });
                divElement.appendChild(newI);
                const newB = document.createElement("button");
                newB.classList.add("answer-button");
                newB.onclick = () => {
                    document.getElementById("answer_" + qa[i]["question_id"].toString()).click();
                };

                newB.innerHTML = "Select an Image";
                divElement.appendChild(newB);
                const newImg = document.createElement("img");
                newImg.id = "image_" + qa[i]["question_id"].toString();
                divElement.appendChild(newImg);
            }
        }
    }else{
        const qa = await response;
        console.log(qa)
    }
    if (team_name !== "Test") {
        const map_response = await fetch(`${HTTPS}${SERVER_IP}:${PORT}/maps`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({"passcode": passcode})
        });
        if (map_response.status === 200) {
            console.log("MAPS:")
            MAPS = await map_response.json();
            console.log(MAPS)
        } else {
            console.log(await map_response.json())
        }
    }
    setTimeout(fetchJSONAnswers, 1000);
}

async function fetchJSONAnswers() {
    let a_team_name;
    if (team_name === "Admin"){
        a_team_name = selected_team;
    }else{
        a_team_name = team_name;
    }
    if (a_team_name === undefined){
        setTimeout(fetchJSONAnswers, 1000);
    }else {
        const response = await fetch(`${HTTPS}${SERVER_IP}:${PORT}/answers`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({"passcode": passcode, "team_name": a_team_name})
        });
        if (response.status === 200) {
            const answers = await response.json();
            console.log("Answers:", answers);
            for (let i = 0; i < answers.length; i++) {
                if (!image_questions_id.includes(answers[i]["question_id"].toString())) {
                    const id_to_get = "answer_" + answers[i]["question_id"].toString();
                    let input_text = document.getElementById(id_to_get);
                    if (input_text) {
                        input_text.value = answers[i]["answer"][answers[i]["answer"].length - 1]
                    }
                }
            }
        } else {
            console.log(`Error while reading answers! ${response.status}`);
        }
        console.log(`image_questions_id.length = ${image_questions_id.length}`)
        for (let i = 0; i < image_questions_id.length; i++) {
            const photo_response = await fetch(`${HTTPS}${SERVER_IP}:${PORT}/photo_answers`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({"passcode": passcode, "question_id": image_questions_id[i]})
            });
            const an_image = await photo_response.blob()
            if (response.status === 200) {
                const url = window.URL.createObjectURL(an_image);
                const id_to_get = "image_" + image_questions_id[i];
                document.getElementById(id_to_get).src = url;
            } else {
                console.log(`Error while reading photo answers! ${response.status}`);
            }
        }
    }
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
    if (maps_is_visible && loaded_data) {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        if (bologna_satellite_loaded){
            print_bologna_in_correct_position(ctx, canvas.width, canvas.height);
        }
        for (let i = 0; i < data.length; i++) {
            let radius, color;
            if (i === selected_stop && !selected_stop_is_a_train) {
                radius = bus_stop_radius * 2;
                color = 'rgb(197,19,213)';
            } else {
                radius = bus_stop_radius;
                color = 'rgba(255, 0, 0, 1.0)';
            }
            ctx.beginPath();
            ctx.arc(lon_to_x(parseFloat(data[i].lon)), lat_to_y(parseFloat(data[i].lat)),
                radius, 0, 2 * Math.PI);
            ctx.closePath();
            ctx.fillStyle = color;
            ctx.fill();
        }

        for (let i = 0; i < train_stops.length; i++) {
            let radius, color;
            if (i === selected_stop && selected_stop_is_a_train){
                radius = bus_stop_radius * 2.5;
                color = 'rgb(197,19,213)';
            }else{
                radius = bus_stop_radius * 1.5;
                color = 'rgb(18,223,116)';
            }
            ctx.beginPath();
            ctx.arc(lon_to_x(parseFloat(train_stops[i].lon)), lat_to_y(parseFloat(train_stops[i].lat)),
                radius, 0, 2 * Math.PI);
            ctx.closePath();
            ctx.fillStyle = color;
            ctx.fill();
        }

        // LET'S DRAW MAPS AREAS
        for (let i=0; i < MAPS.length; i++) {
            ctx.fillStyle = `rgba(${MAPS[i]["r"]}, ${MAPS[i]["g"]}, ${MAPS[i]["b"]}, 0.5)`;
            ctx.beginPath();
            for (let ii = 0; ii < MAPS[i]["lat"].length; ii++) {
                if (ii === 0) {
                    ctx.moveTo(lon_to_x(MAPS[i]["lon"][ii]), lat_to_y(MAPS[i]["lat"][ii]));
                } else {
                    ctx.lineTo(lon_to_x(MAPS[i]["lon"][ii]), lat_to_y(MAPS[i]["lat"][ii]));
                }
            }
            ctx.closePath();
            ctx.fill();
            ctx.font = `${map_name_size}px Arial`;
            ctx.fillStyle = `rgba(${MAPS[i]["r"]}, ${MAPS[i]["g"]}, ${MAPS[i]["b"]}, 1.0)`;
            ctx.fillText(MAPS[i]["name"], lon_to_x(MAPS[i]["name_lon"]), lat_to_y(MAPS[i]["name_lat"]));

        }
        // LIVE GPS
        for (let ii=0; ii<gpses_to_print.length; ii++){
            ctx.beginPath();
            const an_x = lon_to_x(parseFloat(gpses_to_print[ii][3]));
            const an_y = lat_to_y(parseFloat(gpses_to_print[ii][2]));
            const gps_name = gpses_to_print[ii][0];
            const date = new Date(gpses_to_print[ii][1] * 1000);
            const formattedDate = new Intl.DateTimeFormat('it-IT', gps_time_options).format(date);
            let text_to_show;
            if (zoom_value < (MAX_ZOOM+MIN_ZOOM)/2) {
                text_to_show = gps_name + formattedDate
            }else{
                text_to_show = gps_name
            }
            ctx.font = "15px Arial";
            let textMetrics = ctx.measureText(text_to_show);
            let textWidth = textMetrics.width;
            ctx.arc(an_x, an_y,10, 0, 2 * Math.PI);
            ctx.closePath();
            ctx.fillStyle = 'rgb(95,255,0)';
            ctx.fill();
            ctx.fillStyle = 'rgb(0,0,0)'; // Colore del bordo del rettangolo
            ctx.lineWidth = 2;
            ctx.fillRect(an_x, an_y - textMetrics.actualBoundingBoxAscent, textWidth,
                textMetrics.actualBoundingBoxDescent + textMetrics.actualBoundingBoxAscent);
            ctx.fillStyle = 'rgb(209,93,15)';
            ctx.font = "15px Arial";
            ctx.fillText(text_to_show,an_x,an_y);
        }


        // POINTER
        ctx.beginPath();
        ctx.moveTo(canvas.width / 2 - 0.01 * canvas.width, canvas.height / 2);
        ctx.lineTo(canvas.width / 2 + 0.01 * canvas.width, canvas.height / 2);
        ctx.moveTo(canvas.width / 2, canvas.height / 2 - 0.01 * canvas.height);
        ctx.lineTo(canvas.width / 2, canvas.height / 2 + 0.01 * canvas.height);
        ctx.strokeStyle = "black";
        ctx.lineWidth = 1;
        ctx.stroke();

        // Let's update the coordinate displayed on top right corner
        // console.log(pointing_lat.toFixed(4) + " N\n" + pointing_lon.toFixed(4) + " E");
        height_in_km = canvas.height * zoom_value * 110.574;
        width_in_km = canvas.width * zoom_value * 111.320 * Math.cos(pointing_lat);
        sizes_of_the_map.innerHTML = height_in_km.toFixed(2) + " km height " +
            width_in_km.toFixed(2) + " km width\n ";

        // LEGENDA
        ctx.beginPath();
        ctx.lineWidth = "4";
        ctx.strokeStyle = `rgb(4, 108, 53)`;
        ctx.rect(0, 0, 100, 70);
        ctx.fillStyle = `rgb(0, 0, 0)`;
        ctx.fill();
        ctx.stroke();

        ctx.beginPath();
        ctx.arc(25, 20, bus_stop_maximum_radius * 1.5, 0, 2 * Math.PI);
        ctx.closePath();
        ctx.fillStyle = 'rgb(18,223,116)';
        ctx.fill();

        ctx.beginPath();
        ctx.arc(25, 50, bus_stop_maximum_radius, 0, 2 * Math.PI);
        ctx.closePath();
        ctx.fillStyle = 'rgba(255, 0, 0, 1.0)';
        ctx.fill();

        ctx.font = "25px Arial";
        ctx.fillStyle = 'rgb(255,255,255)';
        ctx.fillText("Train",35,30);
        ctx.fillText("Bus",35,60);

    }else{
        setTimeout(draw_data, 100);
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
        selected_bus_stop_name.style.visibility = "hidden"
        sizes_of_the_map.style.visibility = "hidden"

        let question_map = document.getElementById("question_map");
        question_map.innerHTML = "Mappa"
        questions_panel.style.visibility = "visible"

        fetchJSONAnswers();
    }else{
        maps_is_visible = true;
        canvas.style.visibility = "visible";
        selected_bus_stop_name.style.visibility = "visible"
        sizes_of_the_map.style.visibility = "visible"
        let question_map = document.getElementById("question_map");
        question_map.innerHTML = "Domande"
        questions_panel.style.visibility = "hidden"
    }
}

// 4028, 1009 --> 11.342787 44.494055
// 3000, 514 --> 11.320800 44.501614


const a_x1 = lat_1;
const a_x2 = lat_2;
const a_y1 = px_y_1;
const a_y2 = px_y_2;
const b_x1 = lon_1;
const b_x2 = lon_2;
const b_y1 = px_x_1;
const b_y2 = px_x_2;
const m_lat_to_y = (a_y1 - a_y2) / (a_x1 - a_x2);
const q_lat_to_y = (a_x1*a_y2 - a_x2*a_y1) / (a_x1 - a_x2);
const m_lon_to_x = (b_y1 - b_y2) / (b_x1 - b_x2);
const q_lon_to_x = (b_x1*b_y2 - b_x2*b_y1) / (b_x1 - b_x2);

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
        questions_panel.scrollBy({
            top: -kinetic_scrolling_speed/10,
            behavior: "instant"
        });
        setTimeout(scroll_kinetic, 10);
    }else{
        kinetic_scrolling_speed  = 0;
    }
}

async function ask_for_live_gps(){
    const response = await fetch(`${HTTPS}${SERVER_IP}:${PORT}/live_gps`, {
        method: "POST",
        headers: {
        "Content-Type": "application/json"
        },
        body: JSON.stringify({"passcode": passcode})
    });
    if (response.status === 200) {
        const data = await response.json();
        gpses_to_print.length = 0;
        for (let i = 0; i < data.length; i++) {
            const gps_name = data[i]["gps_name"];
            const time = data[i]["last_location"]["time"];
            const lat = data[i]["last_location"]["lat"];
            const lon = data[i]["last_location"]["lon"];
            console.log(`${gps_name} -> [${time}, ${lat} N, ${lon} E]`);
            gpses_to_print.push([gps_name, time, lat, lon])
        }
        draw_data()
    }else{
        console.log(await response.text());
    }
    setTimeout(ask_for_live_gps, 3000);
}

function send_answer(passcode, answer_id, answer, when_was_launched){
    if (when_was_launched === answer_to_send[answer_id] ) {
        fetch(`${HTTPS}${SERVER_IP}:${PORT}/answer`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({"passcode": passcode, "answer_id": answer_id, "answer": answer})
        });
    }
}

async function upload_file(newI, question_id){
    let file = newI.files[0];
    const formData = new FormData();
    formData.append('photo', file);
    formData.append('question_id', question_id);
    formData.append('passcode', passcode);
    await fetch(`${HTTPS}${SERVER_IP}:${PORT}/photo_upload`, {
        method: 'POST',
        body: formData,
    }).then(response => {
        if (response.ok) {
            alert("Success!");
        } else {
            alert("Error uploading photo!");
        }
    }).catch(error => console.error('Error:', error));
    fetchJSONAnswers();
}