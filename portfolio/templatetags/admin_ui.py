from django import template
from django.urls import reverse

from ..models import (
    ContactMessage, Experience, Profile, Project, SkillCategory, SocialLink, Stat, TechBadge,
)

register = template.Library()

# Navigation latérale de l'admin : (titre du groupe, [(app, modèle, icône, libellé)]).
NAV = [
    ("Site", [
        ("portfolio", "SiteSettings", "fa-palette", "Apparence"),
        ("portfolio", "Profile", "fa-id-card", "Profil"),
        ("portfolio", "Section", "fa-table-columns", "Sections"),
    ]),
    ("Contenu", [
        ("portfolio", "Stat", "fa-chart-simple", "Chiffres clés"),
        ("portfolio", "TechBadge", "fa-microchip", "Technologies"),
        ("portfolio", "SkillCategory", "fa-layer-group", "Compétences"),
        ("portfolio", "Experience", "fa-route", "Parcours"),
        ("portfolio", "Project", "fa-folder-open", "Projets"),
        ("portfolio", "SocialLink", "fa-share-nodes", "Réseaux sociaux"),
    ]),
    ("Communication", [
        ("portfolio", "ContactMessage", "fa-inbox", "Messages"),
    ]),
    ("Accès", [
        ("auth", "User", "fa-users", "Utilisateurs"),
        ("auth", "Group", "fa-user-shield", "Groupes"),
    ]),
]


@register.simple_tag(takes_context=True)
def admin_nav(context):
    """Groupes de navigation, filtrés selon les droits de l'utilisateur."""
    request = context["request"]
    urls = {
        (app["app_label"], model["object_name"]): model.get("admin_url")
        for app in context.get("available_apps", [])
        for model in app["models"]
    }
    unread = ContactMessage.objects.filter(is_read=False).count()
    groups = []
    for title, items in NAV:
        links = []
        for app, model, icon, label in items:
            url = urls.get((app, model))
            if not url:
                continue
            links.append({
                "url": url,
                "icon": icon,
                "label": label,
                "active": request.path.startswith(url),
                "badge": unread if model == "ContactMessage" and unread else None,
            })
        if links:
            groups.append({"title": title, "links": links})
    return groups


@register.simple_tag
def dashboard():
    profile = Profile.load()
    projects = Project.objects.all()
    unread = ContactMessage.objects.filter(is_read=False).count()

    # Part des textes traduits en anglais (champs « _en » remplis).
    translatable = [
        (profile, ["role_badge", "hero_subtitle", "cta_label", "intro_quote", "bio_paragraph1", "bio_paragraph2"]),
        *[(p, ["title", "description", "status_label"]) for p in projects],
        *[(s, ["title", "description"]) for s in SkillCategory.objects.all()],
    ]
    pairs = [(getattr(o, f), getattr(o, f + "_en")) for o, fields in translatable for f in fields]
    pairs = [(fr, en) for fr, en in pairs if fr]
    translated = round(100 * sum(1 for _, en in pairs if en) / len(pairs)) if pairs else 100

    checklist = [
        ("Photo de profil", bool(profile.photo), "fa-camera"),
        ("CV à télécharger", bool(profile.cv_file), "fa-file-arrow-down"),
        ("Présentation rédigée", bool(profile.bio_paragraph1), "fa-pen-nib"),
        ("Au moins 2 réseaux sociaux", SocialLink.objects.count() >= 2, "fa-share-nodes"),
        ("Un projet avec un lien", projects.exclude(link_url="", repo_url="").exists(), "fa-link"),
        ("Une capture d'écran de projet", projects.exclude(image="").exists(), "fa-image"),
        (f"Traduction anglaise ({translated} %)", translated >= 90, "fa-language"),
    ]
    done = sum(1 for _, ok, _ in checklist if ok)

    profile_url = reverse("admin:portfolio_profile_change", args=[profile.pk])
    return {
        "profile": profile,
        "kpis": [
            {"label": "Projets publiés", "value": projects.filter(is_visible=True).count(),
             "hint": f"sur {projects.count()} au total", "icon": "fa-folder-open", "tone": "green",
             "url": reverse("admin:portfolio_project_changelist")},
            {"label": "Compétences", "value": SkillCategory.objects.count(),
             "hint": f"{TechBadge.objects.count()} technologies", "icon": "fa-layer-group", "tone": "blue",
             "url": reverse("admin:portfolio_skillcategory_changelist")},
            {"label": "Étapes du parcours", "value": Experience.objects.count(),
             "hint": f"{Stat.objects.count()} chiffres clés", "icon": "fa-route", "tone": "violet",
             "url": reverse("admin:portfolio_experience_changelist")},
            {"label": "Messages non lus", "value": unread,
             "hint": f"{ContactMessage.objects.count()} reçus au total", "icon": "fa-inbox", "tone": "amber",
             "url": reverse("admin:portfolio_contactmessage_changelist") + "?is_read__exact=0"},
        ],
        "checklist": checklist,
        "completion": round(100 * done / len(checklist)),
        "messages": ContactMessage.objects.all()[:5],
        "shortcuts": [
            ("Modifier le profil", "fa-id-card", profile_url),
            ("Couleurs & animations", "fa-palette", reverse("admin:portfolio_sitesettings_changelist")),
            ("Ajouter un projet", "fa-plus", reverse("admin:portfolio_project_add")),
            ("Ajouter une compétence", "fa-layer-group", reverse("admin:portfolio_skillcategory_add")),
            ("Organiser les sections", "fa-table-columns", reverse("admin:portfolio_section_changelist")),
            ("Réseaux sociaux", "fa-share-nodes", reverse("admin:portfolio_sociallink_changelist")),
        ],
    }
