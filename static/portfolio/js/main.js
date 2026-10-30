/* Portfolio — interactions et animations. Aucune dépendance. */
(function () {
  "use strict";

  var root = document.documentElement;
  var body = document.body;
  var noMotion = root.classList.contains("no-motion");
  var finePointer = matchMedia("(hover: hover) and (pointer: fine)").matches;
  var UI = JSON.parse(document.getElementById("ui-strings").textContent);
  var $ = function (sel, ctx) { return (ctx || document).querySelector(sel); };
  var $$ = function (sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); };
  var store = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} },
  };
  var t = function (key) { return (UI[root.dataset.lang] || UI.fr)[key]; };

  /* ---------- Notification ---------- */
  var toastEl = $(".toast"), toastTimer;
  function toast(message, isError) {
    $("span", toastEl).textContent = message;
    toastEl.classList.toggle("is-error", !!isError);
    $("i", toastEl).className = isError ? "fa-solid fa-circle-exclamation" : "fa-solid fa-circle-check";
    toastEl.classList.add("is-visible");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { toastEl.classList.remove("is-visible"); }, 3600);
  }

  /* ---------- Écran de chargement puis animation d'entrée ---------- */
  function ready() { root.classList.add("is-ready"); }
  var preloader = $(".preloader");
  if (preloader && !noMotion) {
    body.classList.add("is-loading");
    var bar = $(".preloader-bar span"), count = $(".preloader-count");
    var progress = 0, loaded = document.readyState === "complete", start = performance.now(), done = false;
    window.addEventListener("load", function () { loaded = true; });
    var finish = function () {
      if (done) return;
      done = true;
      bar.style.setProperty("--p", 1);
      count.textContent = 100;
      preloader.classList.add("is-done");
      body.classList.remove("is-loading");
      setTimeout(ready, 250);
      setTimeout(function () { preloader.remove(); }, 1100);
    };
    // On n'attend jamais plus de 3 s, même si une ressource externe traîne.
    setTimeout(finish, 3000);
    (function tick(now) {
      if (done) return;
      var target = loaded ? 100 : Math.min(90, (now - start) / 12);
      progress += (target - progress) * 0.12;
      bar.style.setProperty("--p", progress / 100);
      count.textContent = Math.round(progress);
      if (target === 100 && progress > 99.5) return finish();
      requestAnimationFrame(tick);
    })(start);
  } else {
    if (preloader) preloader.remove();
    requestAnimationFrame(ready);
  }

  /* ---------- Thème clair / sombre (révélation circulaire) ---------- */
  var themeBtn = $(".theme-toggle");
  if (themeBtn) {
    themeBtn.addEventListener("click", function (e) {
      var next = root.dataset.theme === "dark" ? "light" : "dark";
      var apply = function () { root.dataset.theme = next; store.set("pf-theme", next); };
      if (noMotion || !document.startViewTransition) return apply();
      var x = e.clientX, y = e.clientY;
      var r = Math.hypot(Math.max(x, innerWidth - x), Math.max(y, innerHeight - y));
      document.startViewTransition(apply).ready.then(function () {
        root.animate(
          { clipPath: ["circle(0px at " + x + "px " + y + "px)", "circle(" + r + "px at " + x + "px " + y + "px)"] },
          { duration: 700, easing: "cubic-bezier(.7,0,.3,1)", pseudoElement: "::view-transition-new(root)" }
        );
      });
    });
  }

  /* ---------- Langue FR / EN ---------- */
  function applyLang(lang) {
    root.dataset.lang = lang;
    root.lang = lang;
    $$("[data-href-" + lang + "]").forEach(function (a) { a.href = a.getAttribute("data-href-" + lang); });
    typed.restart();
    moveIndicator();
  }
  var langBtn = $(".lang-toggle");
  if (langBtn) {
    langBtn.addEventListener("click", function () {
      var next = root.dataset.lang === "fr" ? "en" : "fr";
      store.set("pf-lang", next);
      if (noMotion) return applyLang(next);
      root.classList.add("lang-switching");
      setTimeout(function () {
        applyLang(next);
        root.classList.remove("lang-switching");
      }, 250);
    });
  }

  /* ---------- Texte tapé au clavier ---------- */
  var typed = (function () {
    var el = $(".typed"), timer, words = [], w = 0, c = 0, deleting = false;
    function load() {
      var raw = el.getAttribute("data-words-" + root.dataset.lang) || el.getAttribute("data-words-fr") || "";
      words = raw.split(",").map(function (s) { return s.trim(); }).filter(Boolean);
    }
    function step() {
      var word = words[w] || "";
      if (noMotion) { el.textContent = word; return; }
      c += deleting ? -1 : 1;
      el.textContent = word.slice(0, c);
      var delay = deleting ? 40 : 85;
      if (!deleting && c === word.length) { deleting = true; delay = 1800; }
      else if (deleting && c === 0) { deleting = false; w = (w + 1) % words.length; delay = 350; }
      timer = setTimeout(step, delay);
    }
    return {
      restart: function () {
        if (!el) return;
        clearTimeout(timer); load(); w = 0; c = 0; deleting = false;
        timer = setTimeout(step, 400);
      },
    };
  })();
  typed.restart();
  $$("[data-href-" + root.dataset.lang + "]").forEach(function (a) { a.href = a.getAttribute("data-href-" + root.dataset.lang); });

  /* ---------- Navigation : verre dépoli, masquage, section active ---------- */
  var nav = $("#nav"), indicator = $(".nav-indicator");
  var navLinks = $$(".nav-links a");
  var activeLink = null;

  function moveIndicator() {
    if (!indicator) return;
    if (!activeLink || !activeLink.offsetWidth) { indicator.style.opacity = 0; return; }
    indicator.style.opacity = 1;
    indicator.style.width = activeLink.offsetWidth + "px";
    indicator.style.transform = "translateX(" + activeLink.offsetLeft + "px)";
  }
  function setActive(key) {
    var link = navLinks.filter(function (a) { return a.dataset.nav === key; })[0] || null;
    if (link === activeLink) return;
    navLinks.forEach(function (a) { a.classList.toggle("is-active", a === link); });
    activeLink = link;
    moveIndicator();
  }
  var sectionObserver = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) setActive(entry.target.id === "home" ? null : entry.target.id);
    });
  }, { rootMargin: "-45% 0px -50% 0px" });
  $$("main > section[id]").forEach(function (s) { sectionObserver.observe(s); });
  addEventListener("resize", moveIndicator);

  /* ---------- Défilement : barre de progression, retour en haut, nav ---------- */
  var progressBar = $(".scroll-progress"), toTop = $(".to-top");
  var timelineLine = $(".timeline-line"), lastY = 0, ticking = false;

  function onScroll() {
    var y = scrollY, max = root.scrollHeight - innerHeight;
    var p = max > 0 ? y / max : 0;
    progressBar.style.setProperty("--progress", p);
    toTop.style.setProperty("--progress", p);
    toTop.classList.toggle("is-visible", y > innerHeight * 0.6);
    nav.classList.toggle("is-scrolled", y > 20);
    if (!body.classList.contains("menu-open")) nav.classList.toggle("is-hidden", y > lastY && y > 400);
    lastY = y;
    if (timelineLine) {
      var r = timelineLine.getBoundingClientRect();
      var tl = Math.min(1, Math.max(0, (innerHeight * 0.6 - r.top) / r.height));
      timelineLine.style.setProperty("--tl", tl);
    }
    ticking = false;
  }
  addEventListener("scroll", function () {
    if (!ticking) { requestAnimationFrame(onScroll); ticking = true; }
  }, { passive: true });
  onScroll();
  toTop.addEventListener("click", function () { scrollTo({ top: 0, behavior: noMotion ? "auto" : "smooth" }); });

  /* ---------- Menu mobile ---------- */
  var burger = $(".burger"), mobileMenu = $(".mobile-menu");
  function toggleMenu(open) {
    body.classList.toggle("menu-open", open);
    burger.setAttribute("aria-expanded", open);
    mobileMenu.setAttribute("aria-hidden", !open);
    nav.classList.remove("is-hidden");
  }
  burger.addEventListener("click", function () { toggleMenu(!body.classList.contains("menu-open")); });
  $$("a", mobileMenu).forEach(function (a) { a.addEventListener("click", function () { toggleMenu(false); }); });
  addEventListener("keydown", function (e) { if (e.key === "Escape") toggleMenu(false); });

  /* ---------- Apparition au défilement + compteurs ---------- */
  $$("[data-stagger]").forEach(function (group) {
    $$("[data-reveal]", group).forEach(function (el, i) { el.style.setProperty("--i", i); });
  });

  function countUp(el) {
    var end = parseInt(el.dataset.count, 10) || 0, startTime = null;
    if (noMotion) return;
    (function frame(now) {
      if (!startTime) startTime = now;
      var k = Math.min(1, (now - startTime) / 1600);
      el.textContent = Math.round(end * (1 - Math.pow(1 - k, 4)));
      if (k < 1) requestAnimationFrame(frame);
    })(performance.now());
  }

  var revealObserver = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;
      var el = entry.target;
      el.classList.add("is-in");
      $$("[data-count]", el).forEach(countUp);
      revealObserver.unobserve(el);
      // Une fois apparu, on rend la main aux transitions normales (survol, 3D…).
      var delay = 1100 + (parseInt(el.style.getPropertyValue("--i"), 10) || 0) * 90;
      setTimeout(function () { el.removeAttribute("data-reveal"); el.classList.remove("is-in"); }, delay);
    });
  }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
  $$("[data-reveal]").forEach(function (el) { revealObserver.observe(el); });

  /* ---------- Effets à la souris ---------- */
  if (finePointer && !noMotion) {
    // Halo lumineux
    var glow = $(".cursor-glow");
    if (glow) {
      var gx = innerWidth / 2, gy = innerHeight / 2, tx = gx, ty = gy;
      addEventListener("pointermove", function (e) { tx = e.clientX; ty = e.clientY; glow.classList.add("is-on"); });
      document.addEventListener("pointerleave", function () { glow.classList.remove("is-on"); });
      (function loop() {
        gx += (tx - gx) * 0.12; gy += (ty - gy) * 0.12;
        glow.style.transform = "translate3d(" + gx + "px," + gy + "px,0)";
        requestAnimationFrame(loop);
      })();
    }

    // Projecteur + inclinaison 3D des cartes
    var tilt = body.classList.contains("has-tilt");
    $$(".card").forEach(function (card) {
      card.addEventListener("pointermove", function (e) {
        var r = card.getBoundingClientRect();
        var px = (e.clientX - r.left) / r.width, py = (e.clientY - r.top) / r.height;
        card.style.setProperty("--mx", px * 100 + "%");
        card.style.setProperty("--my", py * 100 + "%");
        if (tilt && card.classList.contains("tilt")) {
          card.style.transform = "perspective(900px) rotateX(" + (0.5 - py) * 7 + "deg) rotateY(" + (px - 0.5) * 7 + "deg) translateY(-4px)";
        }
      });
      card.addEventListener("pointerleave", function () { card.style.transform = ""; });
    });

    // Boutons magnétiques
    $$(".magnetic").forEach(function (btn) {
      btn.addEventListener("pointermove", function (e) {
        var r = btn.getBoundingClientRect();
        var dx = e.clientX - r.left - r.width / 2, dy = e.clientY - r.top - r.height / 2;
        btn.style.transform = "translate(" + dx * 0.25 + "px," + dy * 0.35 + "px)";
      });
      btn.addEventListener("pointerleave", function () { btn.style.transform = ""; });
    });

    // Parallaxe de la photo
    var frame = $("[data-parallax]"), hero = $(".hero");
    if (frame) {
      hero.addEventListener("pointermove", function (e) {
        var dx = e.clientX / innerWidth - 0.5, dy = e.clientY / innerHeight - 0.5;
        frame.style.transform = "translate(" + dx * -18 + "px," + dy * -18 + "px)";
        $$(".tech-badge", frame).forEach(function (b, i) {
          var k = (i % 2 ? 1 : -1) * (14 + i * 4);
          b.style.translate = dx * k + "px " + dy * k + "px";
        });
      });
      hero.addEventListener("pointerleave", function () { frame.style.transform = ""; });
    }
  }

  /* ---------- Copier l'e-mail ---------- */
  $$("[data-copy]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var value = btn.dataset.copy;
      var done = function () { toast(t("copied")); };
      if (navigator.clipboard) navigator.clipboard.writeText(value).then(done, function () { location.href = "mailto:" + value; });
      else location.href = "mailto:" + value;
    });
  });

  /* ---------- Formulaire de contact ---------- */
  var form = $(".contact-form");
  if (form) {
    var submit = $("button[type=submit]", form), label = $(".btn-label", submit);
    var labelHTML = label.innerHTML;

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var invalid = $$("input[required], textarea[required]", form).filter(function (f) {
        var bad = !f.checkValidity();
        f.closest(".field").classList.toggle("is-invalid", bad);
        return bad;
      });
      if (invalid.length) { invalid[0].focus(); return toast(t("error"), true); }

      submit.disabled = true;
      label.textContent = t("sending");
      fetch(form.action, {
        method: "POST",
        body: new FormData(form),
        headers: { "X-Requested-With": "XMLHttpRequest" },
        credentials: "same-origin",
      })
        .then(function (res) { return res.json().then(function (data) { return { status: res.status, data: data }; }); })
        .then(function (r) {
          if (r.data.ok) { form.reset(); toast(t("sent")); }
          else toast(t(r.data.reason === "throttled" ? "throttled" : "error"), true);
        })
        .catch(function () { toast(t("error"), true); })
        .then(function () { submit.disabled = false; label.innerHTML = labelHTML; });
    });

    $$(".field input, .field textarea", form).forEach(function (f) {
      f.addEventListener("input", function () { f.closest(".field").classList.remove("is-invalid"); });
    });
  }
})();
