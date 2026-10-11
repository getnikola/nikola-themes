document.addEventListener("DOMContentLoaded", function () {
  // Post/page titles render as <h2>, nested under the site's own <h1> brand.
  // Whatever heading level an author starts their content at, its shallowest
  // heading should land here so it always nests correctly under the title.
  var TARGET_FLOOR = 3;

  document.querySelectorAll(".entry-content").forEach(function (container) {
    var headings = Array.prototype.slice.call(
      container.querySelectorAll("h1, h2, h3, h4, h5, h6")
    );
    if (headings.length === 0) return;

    var minLevel = Math.min.apply(
      null,
      headings.map(function (h) {
        return parseInt(h.tagName.charAt(1), 10);
      })
    );

    var offset = TARGET_FLOOR - minLevel;
    if (offset === 0) return;

    headings.forEach(function (h) {
      var currentLevel = parseInt(h.tagName.charAt(1), 10);
      var newLevel = Math.min(6, Math.max(1, currentLevel + offset));
      if (newLevel === currentLevel) return;

      var replacement = document.createElement("h" + newLevel);
      Array.prototype.forEach.call(h.attributes, function (attr) {
        replacement.setAttribute(attr.name, attr.value);
      });
      while (h.firstChild) {
        replacement.appendChild(h.firstChild);
      }
      h.parentNode.replaceChild(replacement, h);
    });
  });
});
