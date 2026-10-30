import time

from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .forms import ContactForm
from .models import (
    Experience, Profile, Project, Section, SiteSettings, SkillCategory, SocialLink, Stat, TechBadge,
)
from .templatetags.portfolio_tags import JS_UI

CONTACT_COOLDOWN = 30  # secondes entre deux messages d'un même visiteur


def home(request):
    site = SiteSettings.load()
    skills = SkillCategory.objects.all()
    experiences = Experience.objects.all()
    projects = Project.objects.filter(is_visible=True).order_by("-is_featured", "order")
    technologies = TechBadge.objects.all()

    has_content = {
        "skills": skills.exists(),
        "experience": experiences.exists(),
        "contact": True,
    }
    sections = [
        s for s in Section.objects.filter(is_visible=True) if has_content.get(s.key, True)
    ]

    context = {
        "site": site,
        "profile": Profile.load(),
        "sections": sections,
        "badges": [t for t in technologies if t.show_around_photo],
        "marquee": [t for t in technologies if t.show_in_marquee],
        "skills": skills,
        "experiences": experiences,
        "projects": projects,
        "stats": Stat.objects.all(),
        "socials": SocialLink.objects.all(),
        "js_ui": JS_UI,
    }
    return render(request, "portfolio/home.html", context)


@require_POST
def contact(request):
    is_ajax = request.headers.get("x-requested-with") == "XMLHttpRequest"
    form = ContactForm(request.POST)

    last = request.session.get("last_contact", 0)
    if time.time() - last < CONTACT_COOLDOWN:
        status, payload = 429, {"ok": False, "reason": "throttled"}
    elif not form.is_valid():
        status, payload = 400, {"ok": False, "errors": form.errors}
    else:
        if not form.is_spam():
            form.save()
        request.session["last_contact"] = time.time()
        status, payload = 200, {"ok": True}

    if is_ajax:
        return JsonResponse(payload, status=status)
    return redirect("/#contact")
