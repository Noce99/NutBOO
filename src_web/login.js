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
        body: JSON.stringify({message: passcode})
    });
    const data = await response.json();
    console.log("POSTPassCode response:", data);
    return data["team"]
}

function login(){
    let input = document.getElementById("passcode");
    let answer = postPassCode(input.value);
    input.innerHTML = answer
}