function registration(vollstaendig) {
    if (vollstaendig != null || vollstaendig != "Invalid") {
        alert("Registrierung erfolgreich abgeschlossen!");
        console.log(vollstaendig);     
    } else {
        alert("Registrierung nicht erfolgreich abgeschlossen!");
        console.log(vollstaendig);
    }
}

function booked() {
    alert("Fahrtbuchung erfolgreich angelegt!");      
}

function deleteBooking() {
    alert("Fahrtbuchung erfolgreich storniert!");
}

function onlyOne(checkbox) {
    var checkboxes = document.getElementsByName('check')
    checkboxes.forEach((item) => {
        if (item !== checkbox) item.checked = false
    })
}
