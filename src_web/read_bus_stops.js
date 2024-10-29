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
let selected_bus_stop_i = -1;

document.addEventListener('DOMContentLoaded', function() {
    canvas = document.getElementById("myCanvas");
    fetchJSONData();
    top_right_coordinate_display = document.getElementById("top_right_coordinate_display");
    top_left_scale_display = document.getElementById("top_left_scale_display");
    bottom_right_stop_name_display = document.getElementById("bottom_right_stop_name_display");
    canvas.addEventListener("click", function(event) {
        // Ottieni le coordinate del clic all'interno del canvas
        const rect = canvas.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;
        const lat = y_to_lat(y);
        const lon = x_to_lon(x);

        console.log(x + " " + y)
        console.log(lat.toFixed(4) + " N " + lon.toFixed(4) + " E")
        let min = 0;
        let min_i = -1;
        for (let i=0; i < data.length; i++) {
            let distance = Math.abs(lat - parseFloat(data[i].lat)) + Math.abs(lon - parseFloat(data[i].lon));
            if (min_i === -1 || distance < min){
                min_i = i;
                min = distance;
            }
        }
        console.log("Closer stop: " + data[min_i].name)
        bottom_right_stop_name_display.innerHTML = data[min_i].name;
        selected_bus_stop_i = min_i;
        draw_data();
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
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (let i=0; i < data.length; i++) {
        let radius, color;
        if (i === selected_bus_stop_i){
            radius = 5;
            color = 'rgb(197,19,213)'
        }else{
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
    ctx.moveTo(canvas.width/2-0.01*canvas.width, canvas.height/2);
    ctx.lineTo(canvas.width/2+0.01*canvas.width, canvas.height/2);
    ctx.moveTo(canvas.width/2, canvas.height/2-0.01*canvas.height);
    ctx.lineTo(canvas.width/2, canvas.height/2+0.01*canvas.height);
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

function zoom(){
    zoom_value /= 2;
    draw_data();
}

function unzoom(){
    zoom_value *= 2;
    draw_data();
}

function right(){
    pointing_lon += 40*zoom_value;
    draw_data();
}

function left(){
    pointing_lon -= 40*zoom_value;
    draw_data();
}

function up(){
    pointing_lat += 40*zoom_value;
    draw_data();
}

function down(){
    pointing_lat -= 40*zoom_value;
    draw_data();
}

