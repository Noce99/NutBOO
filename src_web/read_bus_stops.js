let canvas;
let ctx;
let zoom_value = 100;
let data;
let translation_x = 0;
let translation_y = 0;


document.addEventListener('DOMContentLoaded', function() {
    fetchJSONData();
});

function fetchJSONData() {
    canvas = document.getElementById("myCanvas");
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

function draw_data(){
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (let i=0; i < data.length; i++) {
        ctx.beginPath();
        ctx.arc((parseInt(data[i].x) + translation_x)/zoom_value + canvas.width/2,
            (parseInt(data[i].y) + translation_y)/zoom_value + canvas.height/2,
            2, 0, 2 * Math.PI);
        ctx.closePath();
        ctx.fillStyle = 'rgba(255,0,0,1.0)';
        ctx.fill();
    }
    ctx.beginPath();
    ctx.moveTo(canvas.width/2-0.01*canvas.width, canvas.height/2);
    ctx.lineTo(canvas.width/2+0.01*canvas.width, canvas.height/2);
    ctx.moveTo(canvas.width/2, canvas.height/2-0.01*canvas.height);
    ctx.lineTo(canvas.width/2, canvas.height/2+0.01*canvas.height);
    ctx.strokeStyle = "black";
    ctx.lineWidth = 3;
    ctx.stroke();
}

function zoom(){
    zoom_value -= 10;
    if (zoom_value <= 10) {
        zoom_value = 10
    }
    draw_data();
}

function unzoom(){
    zoom_value += 10;
    if (zoom_value >= 200) {
        zoom_value = 200
    }
    draw_data();
}

function right(){
    translation_x -= 40*zoom_value;
    draw_data();
}

function left(){
    translation_x += 40*zoom_value;
    draw_data();
}

function up(){
    translation_y += 40*zoom_value;
    draw_data();
}

function down(){
    translation_y -= 40*zoom_value;
    draw_data();
}