function newQuote() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/quote', true);
    xhr.send();
    xhr.onreadystatechange = function() {
        if(this.readyState == 4 && this.status == 200){
            document.getElementById('quote_holder').innerHTML = this.responseText;
        }
    }
}

newQuote();