from django.core.validators import RegexValidator
from django.db import models

hex_color = RegexValidator(
    r"^#[0-9a-fA-F]{6}$", "Utilise un code couleur hexadécimal, ex : #5fe3a1"
)

ICON_HELP = (
    "Classe Font Awesome, ex : <code>fa-solid fa-code</code>, <code>fa-brands fa-python</code>. "
    '<a href="https://fontawesome.com/search?o=r&amp;m=free" target="_blank">Chercher une icône →</a>'
)


class SingletonModel(models.Model):
    """Modèle à instance unique (profil, réglages du site)."""

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


# ---------------------------------------------------------------------------
# Réglages globaux
# ---------------------------------------------------------------------------

class SiteSettings(SingletonModel):
    THEME_CHOICES = [
        ("dark", "Sombre"),
        ("light", "Clair"),
        ("system", "Selon l'appareil du visiteur"),
    ]
    LANG_CHOICES = [("fr", "Français"), ("en", "English")]
    HEADING_FONTS = [
        ("Space Grotesk", "Space Grotesk (tech, moderne)"),
        ("Sora", "Sora (géométrique)"),
        ("Outfit", "Outfit (rond, amical)"),
        ("Plus Jakarta Sans", "Plus Jakarta Sans (élégant)"),
        ("Syne", "Syne (créatif)"),
        ("Poppins", "Poppins (classique)"),
    ]
    BODY_FONTS = [
        ("Inter", "Inter"),
        ("DM Sans", "DM Sans"),
        ("Manrope", "Manrope"),
        ("Plus Jakarta Sans", "Plus Jakarta Sans"),
        ("Nunito Sans", "Nunito Sans"),
    ]

    site_title = models.CharField("titre de l'onglet", max_length=120, blank=True,
                                  help_text="Vide = nom du profil")
    meta_description = models.CharField("description SEO (FR)", max_length=300, blank=True)
    meta_description_en = models.CharField("description SEO (EN)", max_length=300, blank=True)
    favicon = models.ImageField(upload_to="site/", blank=True, null=True)

    default_theme = models.CharField("thème par défaut", max_length=10,
                                     choices=THEME_CHOICES, default="dark")
    default_language = models.CharField("langue par défaut", max_length=2,
                                        choices=LANG_CHOICES, default="fr")

    accent_color = models.CharField("couleur principale", max_length=7, default="#5fe3a1",
                                    validators=[hex_color])
    accent_color_2 = models.CharField("couleur secondaire (dégradés)", max_length=7,
                                      default="#5fb3e3", validators=[hex_color])
    dark_background = models.CharField("fond du mode sombre", max_length=7, default="#0e0f13",
                                       validators=[hex_color])
    light_background = models.CharField("fond du mode clair", max_length=7, default="#f6f7f4",
                                        validators=[hex_color])
    heading_font = models.CharField("police des titres", max_length=40,
                                    choices=HEADING_FONTS, default="Space Grotesk")
    body_font = models.CharField("police du texte", max_length=40,
                                 choices=BODY_FONTS, default="Inter")
    border_radius = models.PositiveSmallIntegerField(
        "arrondi des cartes (px)", default=18, help_text="0 = angles droits, 28 = très arrondi"
    )

    enable_animations = models.BooleanField(
        "animations activées", default=True,
        help_text="Désactivées automatiquement si le visiteur a demandé moins d'animations.",
    )
    enable_preloader = models.BooleanField("écran de chargement", default=True)
    enable_cursor_glow = models.BooleanField("halo lumineux qui suit la souris", default=True)
    enable_tilt = models.BooleanField("effet 3D sur les cartes", default=True)
    show_marquee = models.BooleanField("bandeau défilant des technologies", default=True)
    show_theme_toggle = models.BooleanField("bouton clair / sombre", default=True)
    show_language_toggle = models.BooleanField("bouton FR / EN", default=True)

    enable_contact_form = models.BooleanField("formulaire de contact", default=True)

    class Meta:
        verbose_name = "Apparence & réglages"
        verbose_name_plural = "Apparence & réglages"

    def __str__(self):
        return "Apparence & réglages du site"

    def google_fonts_url(self):
        families = {self.heading_font, self.body_font}
        params = "&".join(
            "family=" + f.replace(" ", "+") + ":wght@400;500;600;700;800" for f in sorted(families)
        )
        return f"https://fonts.googleapis.com/css2?{params}&family=JetBrains+Mono:wght@400;600&display=swap"


class Section(models.Model):
    """Sections de la page : renommables, réordonnables et masquables."""

    KEY_CHOICES = [
        ("about", "À propos"),
        ("skills", "Compétences"),
        ("experience", "Parcours"),
        ("projects", "Projets"),
        ("contact", "Contact"),
    ]

    key = models.CharField("section", max_length=20, choices=KEY_CHOICES, unique=True)
    nav_label = models.CharField("libellé du menu (FR)", max_length=40)
    nav_label_en = models.CharField("libellé du menu (EN)", max_length=40, blank=True)
    eyebrow = models.CharField("sur-titre (FR)", max_length=60, blank=True)
    eyebrow_en = models.CharField("sur-titre (EN)", max_length=60, blank=True)
    title = models.CharField("titre (FR)", max_length=120)
    title_en = models.CharField("titre (EN)", max_length=120, blank=True)
    subtitle = models.TextField("sous-titre (FR)", blank=True)
    subtitle_en = models.TextField("sous-titre (EN)", blank=True)
    is_visible = models.BooleanField("visible", default=True)
    show_in_nav = models.BooleanField("dans le menu", default=True)
    order = models.PositiveIntegerField("ordre", default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Section de la page"
        verbose_name_plural = "Sections de la page"

    def __str__(self):
        return self.get_key_display()


# ---------------------------------------------------------------------------
# Contenu
# ---------------------------------------------------------------------------

class Profile(SingletonModel):
    """Informations principales du portfolio (une seule instance)."""

    full_name = models.CharField("nom complet", max_length=150, default="Tamankeu Songny Yves-Malcom")
    short_name = models.CharField("nom court / logo", max_length=40, blank=True,
                                  help_text="Affiché dans la barre de navigation. Vide = initiales.")
    photo = models.ImageField(upload_to="profile/", blank=True, null=True)

    role_badge = models.CharField("badge (FR)", max_length=100, default="Développeur Full-Stack Django")
    role_badge_en = models.CharField("badge (EN)", max_length=100, default="Full-Stack Django Developer", blank=True)
    available = models.BooleanField("disponible (pastille verte animée)", default=True)
    availability_text = models.CharField("texte de disponibilité (FR)", max_length=80,
                                         default="Disponible pour un stage", blank=True)
    availability_text_en = models.CharField("texte de disponibilité (EN)", max_length=80,
                                            default="Open to internships", blank=True)

    greeting = models.CharField("salutation (FR)", max_length=60, default="Bonjour, je suis", blank=True)
    greeting_en = models.CharField("salutation (EN)", max_length=60, default="Hi, I'm", blank=True)
    hero_title_line1 = models.CharField("titre ligne 1 (FR)", max_length=100, default="Talk is cheap.")
    hero_title_line1_en = models.CharField("titre ligne 1 (EN)", max_length=100, default="Talk is cheap.", blank=True)
    hero_title_line2 = models.CharField("titre ligne 2 (FR)", max_length=100, default="Show me the code!")
    hero_title_line2_en = models.CharField("titre ligne 2 (EN)", max_length=100, default="Show me the code!", blank=True)
    typed_words = models.CharField(
        "mots animés (FR)", max_length=300, blank=True,
        default="applications web, solutions IA, automatisations",
        help_text="Séparés par des virgules. Défilent après « Je conçois des… ».",
    )
    typed_words_en = models.CharField("mots animés (EN)", max_length=300, blank=True,
                                      default="web applications, AI solutions, automations")
    typed_prefix = models.CharField("préfixe des mots animés (FR)", max_length=60, default="Je conçois des", blank=True)
    typed_prefix_en = models.CharField("préfixe des mots animés (EN)", max_length=60, default="I build", blank=True)
    hero_subtitle = models.TextField("sous-titre (FR)", default=(
        "Étudiant en Licence Génie Logiciel, je conçois et développe des "
        "applications web et mobiles pensées pour des besoins réels."
    ))
    hero_subtitle_en = models.TextField("sous-titre (EN)", blank=True)
    cta_label = models.CharField("bouton principal (FR)", max_length=50, default="Discutons !")
    cta_label_en = models.CharField("bouton principal (EN)", max_length=50, default="Let's chat!", blank=True)
    cta_link = models.CharField("lien du bouton principal", max_length=200, default="#contact")
    cta2_label = models.CharField("bouton secondaire (FR)", max_length=50, default="Voir mes projets", blank=True)
    cta2_label_en = models.CharField("bouton secondaire (EN)", max_length=50, default="See my work", blank=True)
    cta2_link = models.CharField("lien du bouton secondaire", max_length=200, default="#projects", blank=True)

    intro_quote = models.CharField("citation (FR)", max_length=250,
                                   default="Le design, ce n'est pas seulement l'apparence. C'est la façon dont ça fonctionne.")
    intro_quote_en = models.CharField("citation (EN)", max_length=250, blank=True,
                                      default="Design is not just what it looks like. Design is how it works!")
    bio_paragraph1 = models.TextField("paragraphe 1 (FR)", blank=True)
    bio_paragraph1_en = models.TextField("paragraphe 1 (EN)", blank=True)
    bio_paragraph2 = models.TextField("paragraphe 2 (FR)", blank=True)
    bio_paragraph2_en = models.TextField("paragraphe 2 (EN)", blank=True)

    email = models.EmailField(blank=True)
    phone = models.CharField("téléphone", max_length=30, blank=True)
    location = models.CharField("localisation (FR)", max_length=100, blank=True, default="Yaoundé, Cameroun")
    location_en = models.CharField("localisation (EN)", max_length=100, blank=True, default="Yaoundé, Cameroon")
    cv_file = models.FileField("CV (FR)", upload_to="cv/", blank=True, null=True)
    cv_file_en = models.FileField("CV (EN)", upload_to="cv/", blank=True, null=True,
                                  help_text="Facultatif. Sans fichier, le CV français est proposé.")

    footer_text = models.CharField("pied de page (FR)", max_length=200,
                                   default="© 2026 — Tous droits réservés.")
    footer_text_en = models.CharField("pied de page (EN)", max_length=200, blank=True,
                                      default="© 2026 — All rights reserved.")

    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profil"

    def __str__(self):
        return self.full_name

    def initials(self):
        return "".join(p[0] for p in self.full_name.split()[:2]).upper()


class Stat(models.Model):
    """Chiffres clés animés (ex : 6+ projets)."""

    value = models.PositiveIntegerField("valeur")
    suffix = models.CharField("suffixe", max_length=5, blank=True, default="+")
    label = models.CharField("libellé (FR)", max_length=60)
    label_en = models.CharField("libellé (EN)", max_length=60, blank=True)
    icon_class = models.CharField("icône", max_length=80, default="fa-solid fa-rocket", help_text=ICON_HELP)
    order = models.PositiveIntegerField("ordre", default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Chiffre clé"
        verbose_name_plural = "Chiffres clés"

    def __str__(self):
        return f"{self.value}{self.suffix} {self.label}"


class TechBadge(models.Model):
    """Technologie : icône autour de la photo et/ou dans le bandeau défilant."""

    POSITION_CHOICES = [
        ("top-left", "En haut à gauche"),
        ("bottom-left", "En bas à gauche"),
        ("bottom-right", "En bas à droite"),
        ("top-right", "En haut à droite"),
    ]

    label = models.CharField("nom", max_length=40, help_text="Ex : Python, Django, SQL")
    icon_class = models.CharField("icône", max_length=80, blank=True, help_text=ICON_HELP)
    icon_image = models.ImageField(
        "logo (image)", upload_to="tech_badges/", blank=True, null=True,
        help_text="Facultatif, prioritaire sur l'icône. Sans image ni icône, le nom est affiché.",
    )
    text_color = models.CharField("couleur", max_length=7, default="#5fe3a1", validators=[hex_color])
    show_around_photo = models.BooleanField("autour de la photo", default=True)
    position = models.CharField("position autour de la photo", max_length=20,
                                choices=POSITION_CHOICES, default="top-left")
    show_in_marquee = models.BooleanField("dans le bandeau défilant", default=True)
    order = models.PositiveIntegerField("ordre", default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Technologie"
        verbose_name_plural = "Technologies"

    def __str__(self):
        return self.label


class SkillCategory(models.Model):
    """Une carte de compétence (ex : Développement Web, Mobile, IA & Data)."""

    icon_class = models.CharField("icône", max_length=80, default="fa-solid fa-code", help_text=ICON_HELP)
    title = models.CharField("titre (FR)", max_length=100)
    title_en = models.CharField("titre (EN)", max_length=100, blank=True)
    description = models.TextField("description (FR)")
    description_en = models.TextField("description (EN)", blank=True)
    tag_line = models.CharField("technologies", max_length=150,
                                help_text="Séparées par « · » ou des virgules, ex : Django · MySQL · Bootstrap")
    order = models.PositiveIntegerField("ordre", default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Compétence"
        verbose_name_plural = "Compétences"

    def __str__(self):
        return self.title

    def tags(self):
        raw = self.tag_line.replace(",", "·")
        return [t.strip() for t in raw.split("·") if t.strip()]


class Experience(models.Model):
    """Étape du parcours (formation ou expérience)."""

    KIND_CHOICES = [("education", "Formation"), ("work", "Expérience"), ("other", "Autre")]
    KIND_ICONS = {
        "education": "fa-solid fa-graduation-cap",
        "work": "fa-solid fa-briefcase",
        "other": "fa-solid fa-star",
    }

    kind = models.CharField("type", max_length=12, choices=KIND_CHOICES, default="education")
    title = models.CharField("intitulé (FR)", max_length=150)
    title_en = models.CharField("intitulé (EN)", max_length=150, blank=True)
    organization = models.CharField("établissement / entreprise", max_length=150, blank=True)
    location = models.CharField("lieu", max_length=100, blank=True, help_text="Ex : Douala")
    period = models.CharField("période (FR)", max_length=60, blank=True,
                              help_text="Ex : 2023 — aujourd'hui. Vide = non affichée.")
    period_en = models.CharField("période (EN)", max_length=60, blank=True)
    description = models.TextField("description (FR)", blank=True)
    description_en = models.TextField("description (EN)", blank=True)
    icon_class = models.CharField("icône", max_length=80, blank=True,
                                  help_text="Vide = icône selon le type. " + ICON_HELP)
    order = models.PositiveIntegerField("ordre", default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Étape du parcours"
        verbose_name_plural = "Parcours"

    def __str__(self):
        return f"{self.title} — {self.organization}" if self.organization else self.title

    def icon(self):
        return self.icon_class or self.KIND_ICONS.get(self.kind, "fa-solid fa-star")


class Project(models.Model):
    """Un projet affiché dans la section Projets."""

    status_label = models.CharField(
        "statut (FR)", max_length=100, default="Projet personnel",
        help_text="Ex : Projet de fin de licence, Projet académique, Projet personnel…",
    )
    status_label_en = models.CharField("statut (EN)", max_length=100, blank=True)
    title = models.CharField("titre (FR)", max_length=150)
    title_en = models.CharField("titre (EN)", max_length=150, blank=True)
    description = models.TextField("description (FR)")
    description_en = models.TextField("description (EN)", blank=True)
    tech_stack = models.CharField(
        "technologies", max_length=250, help_text="Séparées par des virgules, ex : Django, MySQL, IA"
    )
    icon_class = models.CharField("icône (si pas d'image)", max_length=80,
                                  default="fa-solid fa-laptop-code", help_text=ICON_HELP)
    link_url = models.URLField("lien du projet", blank=True, help_text="Lien vers le projet une fois hébergé")
    repo_url = models.URLField("lien du code source", blank=True)
    image = models.ImageField(
        upload_to="projects/", blank=True, null=True, help_text="Capture d'écran du projet (facultatif)"
    )
    is_featured = models.BooleanField("mis en avant", default=False,
                                      help_text="Affiché en grand format")
    order = models.PositiveIntegerField("ordre", default=0)
    is_visible = models.BooleanField("visible", default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Projet"
        verbose_name_plural = "Projets"

    def __str__(self):
        return self.title

    def tech_list(self):
        return [t.strip() for t in self.tech_stack.split(",") if t.strip()]


class SocialLink(models.Model):
    label = models.CharField("nom", max_length=40, help_text="Ex : GitHub, LinkedIn, WhatsApp")
    icon_class = models.CharField("icône", max_length=80, default="fa-brands fa-github", help_text=ICON_HELP)
    url = models.CharField("lien", max_length=300,
                           help_text="URL complète, mailto:… ou https://wa.me/237…")
    show_in_hero = models.BooleanField("dans l'en-tête", default=True)
    show_in_footer = models.BooleanField("dans le pied de page", default=True)
    order = models.PositiveIntegerField("ordre", default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Réseau social"
        verbose_name_plural = "Réseaux sociaux"

    def __str__(self):
        return self.label


class ContactMessage(models.Model):
    name = models.CharField("nom", max_length=120)
    email = models.EmailField()
    subject = models.CharField("sujet", max_length=200, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField("reçu le", auto_now_add=True)
    is_read = models.BooleanField("lu", default=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Message reçu"
        verbose_name_plural = "Messages reçus"

    def __str__(self):
        return f"{self.name} — {self.subject or self.message[:40]}"
