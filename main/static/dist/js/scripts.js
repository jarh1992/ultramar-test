function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});

function actModModal(id_modal, app) {
    let boxId = "box" + id_modal.slice(3);
    let modal = $("#modal" + id_modal);
    if (app === 1) {
        let chChecked = $("#" + boxId + " input:checkbox:checked");
        let check = chChecked.length === 1 ? chChecked[0] : chChecked[1];
        if (id_modal.slice(3) === 'B' || id_modal.slice(3) === 'V') {
            modal.find("#m-id_prev").val(check.name);
        } else if (id_modal.slice(3) === 'U') {
            $("#m-id_u").val(check.name);
        }
    }

    modal.modal();
}

function verifyHeadCheckbox(boxId, headchck, modbutton, delbutton) {
    let box = document.getElementById(boxId);
    let elements = box.getElementsByTagName('input');

    let x = document.getElementById(headchck).checked;
    let count = 0;
    let numcheckbox = 0;

    for (let i = 0; i < elements.length; i++) {
        if (elements[i].id === 'chck') {
            numcheckbox += 1;
            if (x) {
                elements[i].checked = true;
                document.getElementById(delbutton).disabled = false;
                count += 1;
            } else {
                for (let k = 0; k < elements.length; k++) {
                    elements[k].checked = false;
                    document.getElementById(delbutton).disabled = true;
                    document.getElementById(modbutton).disabled = true;
                }
            }
        }

    }
    if (count === 1 && numcheckbox === 1) {
        document.getElementById(modbutton).disabled = false;
    }
}

function verifyBodyCheckbox(boxId, headchck, modbutton, delbutton) {
    let box = document.getElementById(boxId);
    let elements = box.getElementsByTagName('input');
    let numCheckbox = 0;
    let count = 0;
    for (let i = 0; i < elements.length; i++) {
        if (elements[i].id === 'chck') {
            numCheckbox += 1;
            if (elements[i].checked === true) {
                count += 1;
            }
        }
    }
    if (numCheckbox === 1 && count === 1) {
        document.getElementById(headchck).checked = true;
        document.getElementById(delbutton).disabled = false;
        document.getElementById(modbutton).disabled = false;
    } else if (count === numCheckbox) {
        document.getElementById(headchck).checked = true;
        document.getElementById(delbutton).disabled = false;
        document.getElementById(modbutton).disabled = true;
    } else {
        if (count === 1) {
            document.getElementById(headchck).checked = false;
            document.getElementById(delbutton).disabled = false;
            document.getElementById(modbutton).disabled = false;
        } else if (count === 0) {
            document.getElementById(headchck).checked = false;
            document.getElementById(delbutton).disabled = true;
            document.getElementById(modbutton).disabled = true;
        } else {
            document.getElementById(headchck).checked = false;
            document.getElementById(delbutton).disabled = false;
            document.getElementById(modbutton).disabled = true;
        }
    }
}

function deleteItem(boxID, get_url) {
    let chChecked = $("#" + boxID + " input:checkbox:checked");
    let items = [];
    for (let i = 0; i < chChecked.length; i++) {
        items.push(chChecked[i].name);
    }
    let request = $.ajax({
        type: "GET",
        url: get_url,
        data: {
            'type': boxID.slice(3),
            'data': JSON.stringify(items)
        },
        success: function () {
            window.location.reload();
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            alert("some error " + String(errorThrown) + "\n" + String(textStatus) + "\n" + String(XMLHttpRequest.responseText));
        }
    });
}

function checkboxselected() {
    let cbSel;
    let elements = document.getElementsByTagName('input');
    for (let i = 0; i < elements.length; i++) {
        if (elements[i].checked === true) {
            cbSel = elements[i];
        }
    }
    return cbSel.name;
}

function getFormData(form) {
    let unindexed_array = form.serializeArray();
    let indexed_array = {};

    $.map(unindexed_array, function (n, i) {
        indexed_array[n['name']] = n['value'];
    });

    return indexed_array;
}
