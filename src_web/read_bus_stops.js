let canvas;
let ctx;
let zoom_value = 100;
let translation_x = 0;
let translation_y = 0;

function fetchJSONData() {
    canvas = document.getElementById("myCanvas");
    ctx = canvas.getContext("2d");
    ctx.fillStyle = "red";
    fetch("data/bus_stops.json").then((res) => {
        if (!res.ok) {
                throw new Error(`HTTP error! Status: ${res.status}`);
        }
        return res.json();
    }).then((data) =>
        draw_data(data)
    ).catch((error) =>
        console.error("Unable to fetch data:", error)
    );
}

function draw_data(data){
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (let i=0; i < data.length; i++) {
       ctx.fillRect(parseInt(data[i].x)/zoom_value + translation_x,
           parseInt(data[i].y)/zoom_value + translation_y, 5, 5);
    }
}

function zoom(){
    zoom_value -= 10;
    fetchJSONData();
}

function unzoom(){
    zoom_value += 10;
    fetchJSONData();
}

function right(){
    translation_x -= 10;
    fetchJSONData();
}

function left(){
    translation_x += 10;
    fetchJSONData();
}

function up(){
    translation_y += 10;
    fetchJSONData();
}

function down(){
    translation_y -= 10;
    fetchJSONData();
}