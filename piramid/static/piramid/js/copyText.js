function copyFunc() {
    var copyText = document.getElementById("copyText");

    copyText.select();

    document.execCommand("copy");

    alert("Copied the text: " + copyText.value);
}
