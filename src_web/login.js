SERVER_IP = "boo.nutlab.it" //"137.204.57.32"

async function getData() {
    const response = await fetch('http://127.0.0.1:4989/api/data');
    const data = await response.json();
    console.log('GET response:', data);
}

async function postData() {
    const response = await fetch('http://127.0.0.1:4989/api/data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({message: 'Hallo from JavaScript!'})
    });
    const data = await response.json();
    console.log('POST response:', data);
}

async function postPassCode(passcode) {
    const response = await fetch("https://" + SERVER_IP + ":4989/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({"passcode": passcode})
    });
    const data = await response.json();
    console.log("POSTPassCode response:", data["team"]);
    return data["team"]
}

async function login(){
    let input = document.getElementById("passcode");
    let answer = await postPassCode(input.value);
    if (answer != "Unknown") {
        input.value = "";
        const encoded_answer = encodeURIComponent(answer);
        window.location.href = `show_bus_stops.html?passcode=${encoded_answer}`;
    }else{
        input.value = "This passcode doesn't exists! Please try again!";
    }
}