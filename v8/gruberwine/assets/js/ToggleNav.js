/* Toggle between showing and hiding the navigation menu links when the user clicks on
the hamburger menu / bar icon */
function toggleNav() {
  let links = document.getElementById("navlinks");
  let social = document.getElementById("socialNav");
  if (links.style.display === "block") {
    links.style.display = "none";
    social.style.minHeight = "5vh";
  } else {
    links.style.display = "block";
    social.style.minHeight = "32vh";
  }
}
