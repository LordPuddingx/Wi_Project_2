function deleteBooking() {
    alert("Fahrtbuchung erfolgreich storniert!");
}

// Nur eine Checkbox auswählbar bei Tab "Auf Rechnung"
function onlyOne(checkbox) {
    var checkboxes = document.getElementsByName('check')
    checkboxes.forEach((item) => {
        if (item !== checkbox) item.checked = false
    })
}
