var a = 0;
const radio = document.querySelectorAll('input[name="genehmingungsfrei"]');
const radio_pflicht = document.querySelectorAll('input[name="genehmingungspflicht"]');
const radio_art = document.querySelectorAll('input[name="art"]');
const radio_aus = document.querySelectorAll('input[name="ausstatt"]');

function checkRadio() {
    let data = {
        voll_teilstationaere_Behandlung: radio[0].checked,
        vor_nachstationaere_Behandlung: radio[1].checked,
        ambulante_Behandlung: radio[2].checked,
        anderer_Grund: radio[3].checked,
        anderer_Grund_Kommentar: document.getElementById("einsczwei").value,

        hochfrequente_Behandlung: radio_pflicht[0].checked,
        vergleichbarer_Ausnahmefall: radio_pflicht[1].checked,
        dauerhafte_Mobilitaetsbeeintraechtigung: radio_pflicht[2].checked,
        anderer_Grund_KTW: radio_pflicht[3].checked,

        taxi: radio_art[0].checked,
        KTW: radio_art[1].checked,
        RTW: radio_art[2].checked,
        NAW: radio_art[3].checked,
        andere: radio_art[4].checked,

        rollstuhl: radio_aus[0].checked,
        tragestuhl: radio_aus[1].checked,
        liegend: radio_aus[2].checked,

        KTW_Begruendung: document.getElementById("zweieinsc").value,
        andere_Begruendung: document.getElementById("zweieinsd").value,
        Begruendung_vier: document.getElementById("zweivier").value,

        date: document.getElementById("zeitpunkt").value,
        behandlungsort: document.getElementById("ort").value,
    };
    var xhr = new XMLHttpRequest();
    var url = "http://127.0.0.1:5000/book";

    xhr.open('POST', url, false);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
        if (xhr.readyState == XMLHttpRequest.DONE) {
            alert("Fahrtbuchung erfolgreich angelegt");
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
