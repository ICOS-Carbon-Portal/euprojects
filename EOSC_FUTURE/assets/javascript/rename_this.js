function my_function(e) {
    const checkBoxes = document.getElementsByClassName('infrastructure-checkbox')
    let dataObjects = [];
    for (let i = 0; i < checkBoxes.length; i++) {
        dataObjects = { ...dataObjects, [checkBoxes.item(i).id]: checkBoxes.item(i).checked}
    }
    const jsonData = JSON.stringify(dataObjects)
    const xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
        console.log("Result will be sent to server");
    }
    xhttp.open("POST", "/", true);
    xhttp.send(jsonData);
}

function resizeIframe(frameObject) {
    frameObject.style.height = frameObject.contentWindow.document.documentElement.scrollHeight + 'px';
  }
