let api_url = "{{api_prefix}}"
let basicParrotImage = api_url + '/left';
let percentageDecimal = 1.0;

function parrotify() {
    const parrotOverlayImage = document.getElementById("overlay").value;
    const parrotSpeed = document.getElementById("range_speed").value;
    const parrotOverlayOffsetX = document.getElementById("range_offset_x").value;
    const parrotOverlayOffsetY = document.getElementById("range_offset_y").value;
    const newImprovedParrot = basicParrotImage + "?overlay=" + parrotOverlayImage + "&size=" + percentageDecimal + "&offset_x=" + parrotOverlayOffsetX + "&offset_y=" + parrotOverlayOffsetY + "&speed=" + parrotSpeed;
    const newImprovedSmallParrot = newImprovedParrot + "&resize=128x128";
    const newImprovedIconParrot = newImprovedParrot + "&resize=32x32";
    document.getElementById("parrotImage").src = newImprovedParrot;
    document.getElementById("parrotImageURL").value = newImprovedParrot;
}

function showErrorMessage(error){
    document.getElementById("error").innerHTML = error;
    document.getElementById("parrotImage").src = basicParrotImage;
}

function getImageSize(url) {
    if(url.length > 300){
        showErrorMessage("Please enter a shorter image URL");
        return;
    }
    let image = new Image();
    image.onerror = function () {
        showErrorMessage("Please enter a valid image URL");
    }
    image.onload = function () {
        imageHeightOriginal = this.height;
        imageWidthOriginal = this.width;
        document.getElementById("error").innerHTML = ""
        parrotify();
    }
    image.src = url;
}

function show_speed(newValue) {
    document.getElementById("speed").innerHTML = newValue;
}

function change_size_percent(percentage) {
    percentageDecimal = percentage / 100.0;
    parrotify();
}

function show_size_percent(newValue) {
    document.getElementById("size_percent").innerHTML = newValue;
}

function show_offset_x(newValue) {
    document.getElementById("offset_x").innerHTML = newValue;
}

function show_offset_y(newValue) {
    document.getElementById("offset_y").innerHTML = newValue;
}

function removeSelectedElement() {
    const parrotchoices = document.getElementsByClassName('parrotchoice');
    for (let j = 0; j < parrotchoices.length; j++) {
        if(parrotchoices[j].classList.contains("selected")){
            parrotchoices[j].classList.remove("selected");
        }
    }
}

function determineSelectedParrot(el) {
    const choice = el.childNodes[1].innerHTML;
    switch(choice) {
        case "Left":
            basicParrotImage = api_url + '/left';
            parrotify()
            break;
        case "Right":
            basicParrotImage = api_url + '/right';
            parrotify()
            break;
        case "Middle":
            basicParrotImage = api_url + '/middle';
            parrotify()
            break;
        case "Conga":
            basicParrotImage = api_url + '/conga';
            parrotify()
            break;
        case "Bored":
            basicParrotImage = api_url + '/bored';
            parrotify()
            break;
        default:
            basicParrotImage = api_url + '/left';
            parrotify()
    }
}

window.addEventListener('load', function () {
    const parrotchoices = document.getElementsByClassName('parrotchoice');
    for (let i = 0; i < parrotchoices.length; i++) {
        parrotchoices[i].addEventListener('click', function () {
            if (this.classList.contains("selected")) {
                this.classList.remove("selected");
            } else {
                removeSelectedElement();
                this.classList.add("selected");
                determineSelectedParrot(this);
            }
        })
    }
});

function copyImageURL() {
    const elem = document.createElement('textarea');
    elem.value = window.location.origin + '/' + document.getElementById("parrotImage").getAttribute("src").replace(/^\/+/g, '');
    document.body.appendChild(elem);
    elem.select();
    elem.setSelectionRange(0, 99999); /* For mobile devices */
    document.getElementById("copy-tooltip").style.display = "inline";
    document.execCommand('copy');
    setTimeout( function() {
        document.getElementById("copy-tooltip").style.display = "none";
    }, 1000);
    document.body.removeChild(elem);
}

function downloadImage() {
    const url = window.location.origin + '/' + document.getElementById("parrotImage").getAttribute("src").replace(/^\/+/g, '');
    const a = document.createElement('a');
    a.href = url;
    a.download = url.split(/api\/v1\/parrots\/|images\//).pop().split('?')[0];
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}