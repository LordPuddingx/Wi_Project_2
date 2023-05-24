var a = 0;
const radio = document.querySelectorAll('input[name="genehmingungsfrei"]');

function checkRadio()
{
    let data = {
        voll_teilstationaere_Behandlung: radio[0].checked,
        vor_nachstationaere_Behandlung: radio[1].checked,
        ambulante_Behandlung: radio[2].checked,
        anderer_Grund: radio[3].checked,
        anderer_Grund_Kommentar: document.getElementById("einsczwei").value
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
