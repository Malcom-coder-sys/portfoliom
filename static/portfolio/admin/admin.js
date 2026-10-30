/* Petits plus pour l'admin du portfolio. */
document.addEventListener("DOMContentLoaded", function () {
  var body = document.body;

  // Barre latérale sur mobile.
  document.querySelectorAll("[data-sidebar-toggle]").forEach(function (btn) {
    btn.addEventListener("click", function () { body.classList.toggle("pf-sidebar-open"); });
  });
  document.querySelectorAll("[data-sidebar-close]").forEach(function (el) {
    el.addEventListener("click", function () { body.classList.remove("pf-sidebar-open"); });
  });

  // Menu utilisateur.
  var user = document.querySelector(".pf-user");
  if (user) {
    var toggle = user.querySelector("[data-menu-toggle]");
    toggle.addEventListener("click", function (e) {
      e.stopPropagation();
      var open = user.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open);
    });
    document.addEventListener("click", function (e) {
      if (!user.contains(e.target)) { user.classList.remove("is-open"); toggle.setAttribute("aria-expanded", false); }
    });
  }
  document.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    body.classList.remove("pf-sidebar-open");
    if (user) user.classList.remove("is-open");
  });

  // « titre (FR) : » → « titre » + étiquette FR colorée (formulaires et en-têtes de listes).
  var langPattern = /\s*\((FR|EN)\)\s*(:?)\s*$/;
  document.querySelectorAll(".aligned label, .aligned legend, #result_list thead th .text a, #result_list thead th .text span").forEach(function (el) {
    var node = Array.prototype.find.call(el.childNodes, function (n) {
      return n.nodeType === 3 && n.textContent.trim();
    });
    if (!node) return;
    node.textContent = node.textContent.replace(/\s*:\s*$/, "");
    if (!langPattern.test(node.textContent)) return;
    var lang = node.textContent.match(langPattern)[1];
    node.textContent = node.textContent.replace(langPattern, "");
    var tag = document.createElement("span");
    tag.className = "pf-lang pf-lang-" + lang.toLowerCase();
    tag.textContent = lang;
    node.after(tag);
  });

  // Aperçu en direct des icônes Font Awesome.
  document.querySelectorAll(".icon-field").forEach(function (wrap) {
    var input = wrap.querySelector("input");
    var icon = wrap.querySelector(".icon-field-preview i");
    input.addEventListener("input", function () { icon.className = input.value.trim(); });
  });

  // Valeur hexadécimale à côté des sélecteurs de couleur.
  document.querySelectorAll("input[type=color]").forEach(function (input) {
    var wrap = document.createElement("span");
    wrap.className = "pf-color";
    input.before(wrap);
    wrap.appendChild(input);
    var label = document.createElement("span");
    label.className = "color-value";
    label.textContent = input.value;
    wrap.appendChild(label);
    input.addEventListener("input", function () { label.textContent = input.value; });
  });

  // Afficher / masquer le mot de passe (connexion).
  document.querySelectorAll("[data-reveal-password]").forEach(function (btn) {
    var input = btn.parentElement.querySelector("input");
    btn.addEventListener("click", function () {
      var show = input.type === "password";
      input.type = show ? "text" : "password";
      btn.innerHTML = show ? '<i class="fa-regular fa-eye-slash"></i>' : '<i class="fa-regular fa-eye"></i>';
    });
  });
});
