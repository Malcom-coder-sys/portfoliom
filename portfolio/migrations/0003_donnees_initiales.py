from django.db import migrations

BOOTSTRAP_TO_FA = {
    "bi-code-slash": "fa-solid fa-code",
    "bi-database": "fa-solid fa-database",
    "bi-robot": "fa-solid fa-robot",
    "bi-graph-up": "fa-solid fa-chart-line",
    "bi-phone": "fa-solid fa-mobile-screen",
    "bi-cpu": "fa-solid fa-microchip",
}

BADGES = {
    "Py": ("Python", "fa-brands fa-python"),
    "Dj": ("Django", ""),
    "SQL": ("SQL", "fa-solid fa-database"),
}

SECTIONS = [
    # key, nav FR, nav EN, eyebrow FR, eyebrow EN, title FR, title EN, subtitle FR, subtitle EN
    ("about", "À propos", "About", "Introduction", "Introduce", "Qui suis-je ?", "Who am I?", "", ""),
    ("skills", "Compétences", "Skills", "Ce que je fais", "What I do", "Mes compétences", "My skills",
     "Les domaines dans lesquels j'apporte de la valeur.", "The areas where I bring value."),
    ("experience", "Parcours", "Journey", "Parcours", "Journey", "Formation & expériences",
     "Education & experience", "", ""),
    ("projects", "Projets", "Projects", "Portfolio", "Portfolio", "Mes projets", "My projects",
     "Quelques projets académiques et personnels récents.", "A few recent academic and personal projects."),
    ("contact", "Contact", "Contact", "Contact", "Contact", "Travaillons ensemble", "Let's work together",
     "Un projet, un stage, une question ? Écris-moi, je réponds rapidement.",
     "A project, an internship, a question? Drop me a line, I reply quickly."),
]


def forwards(apps, schema_editor):
    SkillCategory = apps.get_model("portfolio", "SkillCategory")
    TechBadge = apps.get_model("portfolio", "TechBadge")
    Profile = apps.get_model("portfolio", "Profile")
    SocialLink = apps.get_model("portfolio", "SocialLink")
    Section = apps.get_model("portfolio", "Section")
    SiteSettings = apps.get_model("portfolio", "SiteSettings")

    for skill in SkillCategory.objects.filter(icon_class__startswith="bi-"):
        skill.icon_class = BOOTSTRAP_TO_FA.get(skill.icon_class, "fa-solid fa-code")
        skill.save(update_fields=["icon_class"])

    for badge in TechBadge.objects.filter(label__in=BADGES):
        badge.label, badge.icon_class = BADGES[badge.label]
        badge.save(update_fields=["label", "icon_class"])

    profile = Profile.objects.first()
    if profile and not SocialLink.objects.exists():
        links = [
            ("GitHub", "fa-brands fa-github", profile.github_url),
            ("LinkedIn", "fa-brands fa-linkedin-in", profile.linkedin_url),
            ("Email", "fa-solid fa-envelope", f"mailto:{profile.email}" if profile.email else ""),
        ]
        for order, (label, icon, url) in enumerate(links, start=1):
            if url:
                SocialLink.objects.create(label=label, icon_class=icon, url=url, order=order)

    for order, row in enumerate(SECTIONS, start=1):
        key, nav, nav_en, eb, eb_en, title, title_en, sub, sub_en = row
        Section.objects.get_or_create(key=key, defaults=dict(
            nav_label=nav, nav_label_en=nav_en, eyebrow=eb, eyebrow_en=eb_en,
            title=title, title_en=title_en, subtitle=sub, subtitle_en=sub_en, order=order,
        ))

    SiteSettings.objects.get_or_create(pk=1)


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0002_bilingue_et_reglages"),
    ]

    operations = [
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
