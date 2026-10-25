/* ilkyazs.com — table sorting, row ↔ image hover, placeholders, embeds, lightbox, email. */
(function () {
  "use strict";
  var SITE = window.SITE || {};
  var MAP = {};

  function path(src) {
    try { return decodeURI((src || "").replace(location.origin, "")); } catch (e) { return src; }
  }
  function info(src) { return MAP[path(src)] || null; }

  function cargoUrl(i, small) {
    if (!small || i.video) return i.cargo;
    return i.cargo.replace(/\/(t\/original|w\/\d+\/q\/\d+)\/i\//, "/w/800/q/80/i/");
  }

  function placeholder(src) {
    var d = document.createElement("div");
    d.className = "ph";
    var i = info(src);
    if (i && i.w && i.h) d.style.aspectRatio = i.w + " / " + i.h;
    d.textContent = path(src).split("/").pop();
    d.title = "Add this file at " + path(src).replace(/^\//, "");
    d.dataset.src = src;
    return d;
  }

  // a file that isn't in the repository yet -> Cargo copy (if switched on) or grey placeholder
  function missing(el) {
    var src = el.dataset.src || el.getAttribute("src");
    var i = info(src);
    if (SITE.showCargoImages && i && i.cargo && !el.dataset.triedCargo) {
      el.dataset.triedCargo = "1";
      el.dataset.src = src;
      el.src = cargoUrl(i, !!el.closest(".tile"));
      return;
    }
    var ph = placeholder(src);
    var row = el.closest(".row");
    if (row && i && i.w && i.h) ph.style.flexGrow = (i.w / i.h).toFixed(3);
    el.replaceWith(ph);
  }

  function watch(el) {
    if (el.dataset.watched) return;
    el.dataset.watched = "1";
    el.addEventListener("error", function () { missing(el); });
    if (el.tagName === "IMG" && el.complete && el.naturalWidth === 0) missing(el);
    if (el.tagName === "VIDEO" && el.error) missing(el);
  }

  // images in a gallery row share one height
  function weightRows() {
    document.querySelectorAll(".b-gallery .row > img, .b-gallery .row > video").forEach(function (el) {
      var i = info(el.getAttribute("src"));
      if (i && i.w && i.h) el.style.flexGrow = (i.w / i.h).toFixed(3);
    });
  }

  function embeds() {
    document.querySelectorAll(".embed[data-url]").forEach(function (box) {
      var url = box.dataset.url, src = null, m;
      if ((m = url.match(/(?:youtu\.be\/|youtube\.com\/(?:watch\?v=|embed\/|shorts\/))([\w-]{6,})/)))
        src = "https://www.youtube-nocookie.com/embed/" + m[1] + "?rel=0&modestbranding=1";
      else if ((m = url.match(/vimeo\.com\/(?:video\/)?(\d+)/)))
        src = "https://player.vimeo.com/video/" + m[1];
      else if (/soundcloud\.com/.test(url)) {
        src = url.replace(/color=%23[0-9a-f]{6}/i, "color=%23" + getComputedStyle(document.documentElement).getPropertyValue("--accent").trim().replace("#", ""));
        box.classList.add("is-audio");
      }
      if (!src) { box.innerHTML = '<a href="' + url + '">' + url + "</a>"; return; }
      box.innerHTML = '<iframe src="' + src + '" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen loading="lazy"></iframe>';
    });
  }

  // hovering a row lights up its image, and the other way round
  function hoverLinks() {
    var byKey = {};
    document.querySelectorAll("[data-key]").forEach(function (el) {
      (byKey[el.dataset.key] = byKey[el.dataset.key] || []).push(el);
    });
    Object.keys(byKey).forEach(function (k) {
      byKey[k].forEach(function (el) {
        el.addEventListener("mouseenter", function () { byKey[k].forEach(function (x) { x.classList.add("is-hot"); }); });
        el.addEventListener("mouseleave", function () { byKey[k].forEach(function (x) { x.classList.remove("is-hot"); }); });
      });
    });
    document.querySelectorAll("tbody tr[data-href]").forEach(function (tr) {
      tr.addEventListener("click", function (e) {
        if (e.target.closest("a")) return;
        var href = tr.dataset.href;
        if (/^https?:/.test(href) && href.indexOf(location.host) < 0) window.open(href, "_blank", "noopener");
        else location.href = href;
      });
    });
  }

  // click a column header to sort; the image grid follows the table order
  function sorting() {
    document.querySelectorAll("table[data-sortable]").forEach(function (table) {
      var body = table.tBodies[0];
      var grid = table.closest(".archive") && table.closest(".archive").querySelector("[data-grid]");
      table.querySelectorAll("th[data-sort]").forEach(function (th) {
        th.addEventListener("click", function () {
          var key = th.dataset.sort, num = th.hasAttribute("data-num");
          var asc = th.classList.contains("is-sorted") ? !th.classList.contains("asc") : !num;
          table.querySelectorAll("th").forEach(function (h) { h.classList.remove("is-sorted", "asc"); });
          th.classList.add("is-sorted"); if (asc) th.classList.add("asc");
          var rows = Array.prototype.slice.call(body.rows);
          rows.sort(function (a, b) {
            var x = a.dataset[key] || "", y = b.dataset[key] || "";
            var r = num ? (parseFloat(x) || 0) - (parseFloat(y) || 0) : x.localeCompare(y, undefined, { sensitivity: "base" });
            return asc ? r : -r;
          });
          rows.forEach(function (r) { body.appendChild(r); });
          if (grid) rows.forEach(function (r) {
            var t = grid.querySelector('.tile[data-key="' + r.dataset.key + '"]');
            if (t) grid.appendChild(t);
          });
        });
      });
    });
  }

  function lightbox() {
    var lb = document.querySelector(".lightbox");
    if (!lb) return;
    var big = lb.querySelector("img");
    document.addEventListener("click", function (e) {
      var t = e.target;
      if (t.tagName === "IMG" && t.classList.contains("zoomable")) { big.src = t.currentSrc || t.src; lb.hidden = false; }
      else if (!lb.hidden && lb.contains(t)) lb.hidden = true;
    });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") lb.hidden = true; });
  }

  function email() {
    document.querySelectorAll("a.email[data-u]").forEach(function (a) {
      a.addEventListener("click", function (e) { e.preventDefault(); location.href = "mailto:" + a.dataset.u + "@" + a.dataset.d; });
    });
  }

  function init() {
    document.querySelectorAll("main img, main video").forEach(watch);
    weightRows(); embeds(); hoverLinks(); sorting(); lightbox(); email();
  }

  fetch(SITE.mediaMap || "/assets/media-map.json")
    .then(function (r) { return r.ok ? r.json() : {}; })
    .catch(function () { return {}; })
    .then(function (m) { MAP = m || {}; init(); });
})();
