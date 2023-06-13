function booked() {
    let data = {
    };
    var xhr = new XMLHttpRequest();
    var url = "http://127.0.0.1:5000/main";

    xhr.open('POST', url, false);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
        if (xhr.readyState == XMLHttpRequest.DONE) {
            alert("Fahrtbuchung erfolgreich angelegt!");
            window.setTimeout(window.location.reload(), 1000);

        }
    };
    xhr.send(JSON.stringify(data));
}

function deleteBooking() {
    let data = {
    };
    var xhr = new XMLHttpRequest();
    var url = "http://127.0.0.1:5000/main";

    xhr.open('POST', url, false);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
        if (xhr.readyState == XMLHttpRequest.DONE) {
            alert("Fahrtbuchung erfolgreich storniert!");
            window.setTimeout(window.location.reload(), 1000);
        }
    };
    xhr.send(JSON.stringify(data));
}

function onlyOne(checkbox) {
    var checkboxes = document.getElementsByName('check')
    checkboxes.forEach((item) => {
        if (item !== checkbox) item.checked = false
    })
}
