/* http://www.randomsnippets.com/2008/02/12/how-to-hide-and-show-your-div/ */
function toggle(showHideDiv, switchTextDiv) {
    var ele = document.getElementById(showHideDiv);
    var text = document.getElementById(switchTextDiv);
    if(ele.style.display == "none") {
        ele.style.display = "block";
        text.innerHTML = "[hide abstract]";
    }
    else {
            ele.style.display = "none";
            text.innerHTML = "[show abstract]";
    }
}
