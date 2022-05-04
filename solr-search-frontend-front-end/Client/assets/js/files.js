//Services
const SEARCH_SERVICE = `http://localhost:8093/query`;
const SUGGESTION_SERVICE = `http://localhost:8093/suggest`;
//DOM Elements
const SEARCH_INPUT = document.getElementById("SearchInput");
const SEARCH_BUTTON = document.getElementById("buttonSearch");
const CONTAINER_RESULTS = document.getElementById("results-container");
const CONTAINER_SUGGESTION = document.getElementById("suggestion-container");
const CLEAN_FILTERS_BUTTON = document.getElementById("CleanFilter");
const SUGGESTION_TAG = document.getElementById("correction");
const TABLE_CONTAINER_RESULTS = document.getElementById("t-body-results");
const UPLOAD_INPUT = document.getElementById("file");
const UPLOAD_BUTTON = document.getElementById("upload-file-btn");
const UPLOAD_ALERT_ERR = document.getElementById("upload-alert");
const UPLOAD_ALERT_SUCCESS = document.getElementById("upload-alert-success");
const SEARCH_ALERT = document.getElementById("search-alert");
const LOADING_BUTTON = document.getElementById("loading-btn");

//Lists
var suggestions = [];
var docs = [];
var correction = {};

//Functions
function fileValidation() {
    var filePath = UPLOAD_INPUT.value;

    // Allowing file type
    var allowedExtensions = /(\.pdf)$/i;

    if (!allowedExtensions.exec(filePath)) {
        UPLOAD_INPUT.value = "";
        return false;
    } else {
        return true;
    }
}

function autocomplete(inp, arr) {
    if (suggestions.length == 0) {
        return;
    }
    var currentFocus;
    inp.addEventListener("input", function(e) {
        var a,
            b,
            i,
            val = this.value;
        closeAllLists();
        if (!val) {
            return false;
        }
        currentFocus = -1;
        a = document.createElement("DIV");
        a.setAttribute("id", this.id + "autocomplete-list");
        a.setAttribute("class", "autocomplete-items");
        this.parentNode.appendChild(a);
        for (i = 0; i < suggestions.length; i++) {
            if (
                suggestions[i].substr(0, val.length).toUpperCase() == val.toUpperCase()
            ) {
                b = document.createElement("DIV");
                b.innerHTML =
                    "<strong>" + suggestions[i].substr(0, val.length) + "</strong>";
                b.innerHTML += suggestions[i].substr(val.length);
                b.innerHTML += "<input type='hidden' value='" + suggestions[i] + "'>";
                b.addEventListener("click", function(e) {
                    inp.value = this.getElementsByTagName("input")[0].value;
                    closeAllLists();
                });
                a.appendChild(b);
            }
        }
    });

    function closeAllLists(elmnt) {
        var x = document.getElementsByClassName("autocomplete-items");
        for (var i = 0; i < x.length; i++) {
            if (elmnt != x[i] && elmnt != inp) {
                x[i].parentNode.removeChild(x[i]);
            }
        }
    }
    document.addEventListener("click", function(e) {
        closeAllLists(e.target);
    });
}

const generateResults = (docs, container) => {
    if (docs.length == 0) {
        TABLE_CONTAINER_RESULTS.innerHTML =
            "<tr> <td class='dataTables-empty' colspan='4'>No se enccontró ningún resultado</td> </tr>";
        return;
    }

    let TemplateHTML = ``;
    let counter = 1;
    docs.forEach((element) => {
        TemplateHTML += `<tr>
        <th scope="row">${counter++}</th>
        <td>${element["title"]}</td>
        <td>
            <span class="badge bg-info">
                <i class="bi bi-eye"></i>
                <a href="http://localhost:8094/file/${
                  encodeURIComponent(element["title"])
                }"> Visualizar</a>
            </span>
        </td>
        <td>
            <span class="badge bg-success">
            <i class="bi bi-download"></i>
            <a href="http://localhost:8094/download/${encodeURIComponent(element["title"])}"
            download="${element["title"]}"> Descargar</a>
            </span>
        </td>
      </tr>`;
    });
    TABLE_CONTAINER_RESULTS.innerHTML = TemplateHTML;
};

const getResponse = async(direction) => {
    try {
        SEARCH_ALERT.style.display = "none"
        let Search = SEARCH_INPUT.value;
        const response = await fetch(direction + `?q=${Search}`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        });
        let data = await response.json();

        if (data != 0) {
            if (
                data["results"]["0"]["responseHeader"]["params"]["json"].includes("~")
            ) {
                SEARCH_ALERT.style.display = "block";
            }
            docs = data["results"]["0"]["response"]["docs"];
            correction = [];
            if ("spellcheck" in data["results"]["0"]) {
                correction = data["results"]["0"]["spellcheck"]["suggestions"];
            }
            generateResults(docs, CONTAINER_RESULTS);
            getCorrection(correction, CONTAINER_SUGGESTION, SUGGESTION_TAG);
        } else {
            CONTAINER_RESULTS.innerHTML = "No se encontraron resultados";
        }
    } catch (error) {
        CONTAINER_RESULTS.innerHTML = "No se encontraron resultados";
    }
};

const getTitlesResponse = async(direction) => {
    try {
        let Search = SEARCH_INPUT.value;
        const response = await fetch(direction + `?q=${Search}`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        });

        let data = await response.json();
        keyWord = SEARCH_INPUT.value;
        if (keyWord == "") {
            return;
        }
        suggestionArray =
            data["results"]["suggest"]["mySuggester"][keyWord]["suggestions"];
        suggestions = getTitleByJSON(suggestionArray);
        autocomplete(SEARCH_INPUT, suggestions);
    } catch (error) {}
};

const getCorrection = (arrayConter, container, tag) => {
    if (arrayConter == 0) {
        return;
    }
    suggestion = arrayConter[1]["suggestion"][0];
    container.style.display = "block";
    tag.innerHTML = `${suggestion}`;
};

const CleanFilter = () => {
    if (docs.length == 0) {
        return;
    }
    generateResults(docs, CONTAINER_RESULTS);
};

const getTitle = (arrayTitles) => {
    let titles = [];
    if (arrayTitles == 0) {
        return titles;
    }
    arrayTitles.forEach((element) => {
        titles.push(element["title"][0]);
    });
    return titles;
};

const getTitleByJSON = (json) => {
    let titles = [];
    if (json == 0) {
        return titles;
    }
    json.forEach((element) => {
        titles.push(element["term"]);
    });
    return titles;
};

const handleFileUploadError = () => {
    UPLOAD_INPUT.value = "";
    LOADING_BUTTON.style.display = "none";
    UPLOAD_ALERT_ERR.style.display = "block";
}

const getResponseFile = async() => {
    try {
        LOADING_BUTTON.style.display = "none";
        UPLOAD_ALERT_ERR.style.display = "none";
        UPLOAD_ALERT_SUCCESS.display = "none"
        if (!fileValidation()) {
            handleFileUploadError()
            return
        }
        LOADING_BUTTON.style.display = "block";
        let formData = new FormData();
        formData.append("file", UPLOAD_INPUT.files[0]);
        let response = await fetch("http://localhost:8094/upload", {
            method: "POST",
            body: formData,
        });

        let data = await response.status;
        const status = response.headers.get("status");
        if (data == 200) {
            LOADING_BUTTON.style.display = "none";
            UPLOAD_ALERT_SUCCESS.style.display = "block";
        } else {
            handleFileUploadError()
            return false;
        }
        console.log(data);
    } catch (error) {
        handleFileUploadError()
    }
};

//Events

SUGGESTION_TAG.addEventListener("click", () => {
    SEARCH_INPUT.value = SUGGESTION_TAG.textContent;
    CONTAINER_SUGGESTION.style.display = "none";
});

SEARCH_BUTTON.addEventListener("click", () => {
    CONTAINER_SUGGESTION.style.display = "None";
    getResponse(SEARCH_SERVICE);
});

SEARCH_INPUT.addEventListener("input", () => {
    getTitlesResponse(SUGGESTION_SERVICE);
});

SEARCH_INPUT.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
        CONTAINER_SUGGESTION.style.display = "None";
        getResponse(SEARCH_SERVICE);
    }
});

UPLOAD_BUTTON.addEventListener("click", () => {
    getResponseFile();
});

//Functions excecution
autocomplete(SEARCH_INPUT, suggestions);