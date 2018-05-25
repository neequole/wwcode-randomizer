function sendHttpRequest(method, url, callback) {
    var xhr = new XMLHttpRequest();
    xhr.open(method, url, true);
    xhr.send();
    xhr.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            callback(this.responseText);
        }
    }
}


function newQuote() {
    document.getElementById('quote-holder').innerHTML = "Catchin` one...";
    sendHttpRequest('GET', '/quote', function (response) {
        document.getElementById('quote-holder').innerHTML = response;
    });
}

function downloadCSV() {
    var downloadLink = document.getElementById('download-link');
    downloadLink.innerHTML = 'Downloading...';
    sendHttpRequest('GET', '/download', function (response) {
        downloadLink.innerHTML = 'Download';
    });
}

newQuote();
