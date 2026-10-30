from urllib.parse import quote

from django import forms
from django.contrib import admin, messages
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import (
    ContactMessage, Experience, Profile, Project, Section, SiteSettings, SkillCategory, SocialLink,
    Stat, TechBadge,
)

admin.site.site_header = "Portfolio · Administration"
admin.site.site_title = "Portfolio admin"
admin.site.index_title = "Gérer le contenu du portfolio"
# La navigation latérale est fournie par templates/admin/base.html.
admin.site.enable_nav_sidebar = False

# Ordre d'affichage des modèles sur l'accueil de l'admin.
ADMIN_ORDER = [
    "SiteSettings", "Profile", "Section", "Stat", "TechBadge", "SkillCategory",
    "Experience", "Project", "SocialLink", "ContactMessage",
]
_default_get_app_list = admin.AdminSite.get_app_list


def _ordered_app_list(self, request, app_label=None):
    app_list = _default_get_app_list(self, request, app_label)
    for app in app_list:
        if app["app_label"] == "portfolio":
            app["name"] = "Contenu du portfolio"
            app["models"].sort(
                key=lambda m: ADMIN_ORDER.index(m["object_name"]) if m["object_name"] in ADMIN_ORDER else 99
            )
    return app_list


admin.AdminSite.get_app_list = _ordered_app_list


# ---------------------------------------------------------------------------
# Widgets
# ---------------------------------------------------------------------------

class ColorInput(forms.TextInput):
    input_type = "color"


class IconInput(forms.TextInput):
    """Champ texte avec aperçu en direct de l'icône Font Awesome."""

    template_name = "portfolio/widgets/icon_input.html"

    def __init__(self, attrs=None):
        super().__init__({"class": "vTextField icon-input", "placeholder": "fa-solid fa-code", **(attrs or {})})


COLOR_FIELDS = {"accent_color", "accent_color_2", "dark_background", "light_background", "text_color"}


class PortfolioAdmin(admin.ModelAdmin):
    """Base commune : sélecteur de couleur et aperçu d'icône automatiques."""

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name in COLOR_FIELDS:
            kwargs["widget"] = ColorInput
        elif db_field.name == "icon_class":
            kwargs["widget"] = IconInput
        return super().formfield_for_dbfield(db_field, request, **kwargs)


def icon_preview(obj, field="icon_class"):
    value = getattr(obj, field, "")
    if not value:
        return "—"
    return format_html('<i class="{}" style="font-size:1.25rem;width:1.6rem;text-align:center"></i>', value)


def image_preview(file, size=56, round_=False):
    if not file:
        return "—"
    radius = "50%" if round_ else "8px"
    return format_html(
        '<img src="{}" style="width:{}px;height:{}px;object-fit:cover;border-radius:{}">',
        file.url, size, size, radius,
    )


class SingletonAdmin(PortfolioAdmin):
    """Pas de liste : on va directement au formulaire de l'unique instance."""

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = self.model.load()
        return redirect(reverse(f"admin:portfolio_{self.model._meta.model_name}_change", args=[obj.pk]))

    def response_change(self, request, obj):
        if "_continue" not in request.POST and "_addanother" not in request.POST:
            self.message_user(request, "Modifications enregistrées. Elles sont déjà visibles sur le site.",
                              messages.SUCCESS)
            return redirect(request.path)
        return super().response_change(request, obj)


# ---------------------------------------------------------------------------
# Réglages & profil
# ---------------------------------------------------------------------------

@admin.register(SiteSettings)
class SiteSettingsAdmin(SingletonAdmin):
    fieldsets = (
        ("Thème & langue", {
            "description": "Ce que voit un visiteur à sa première visite. Il peut ensuite changer avec les boutons du menu.",
            "fields": (("default_theme", "default_language"), ("show_theme_toggle", "show_language_toggle")),
        }),
        ("Couleurs", {
            "description": "Les deux couleurs créent les dégradés (titres, boutons, anneau de la photo).",
            "fields": (("accent_color", "accent_color_2"), ("dark_background", "light_background")),
        }),
        ("Typographie & formes", {"fields": (("heading_font", "body_font"), "border_radius")}),
        ("Animations", {
            "fields": (
                ("enable_animations", "enable_preloader"),
                ("enable_cursor_glow", "enable_tilt"),
                "show_marquee",
            ),
        }),
        ("Contact", {"fields": ("enable_contact_form",)}),
        ("Référencement (SEO)", {
            "classes": ("collapse",),
            "fields": ("site_title", ("meta_description", "meta_description_en"), "favicon"),
        }),
    )


@admin.register(Profile)
class ProfileAdmin(SingletonAdmin):
    readonly_fields = ("photo_preview",)
    fieldsets = (
        ("Identité", {
            "fields": (("full_name", "short_name"), ("photo", "photo_preview")),
        }),
        ("Badges de l'en-tête", {
            "fields": (("role_badge", "role_badge_en"), "available",
                       ("availability_text", "availability_text_en")),
        }),
        ("Section d'accueil", {
            "description": "Chaque texte existe en français et en anglais. Laisse l'anglais vide pour réutiliser le français.",
            "fields": (
                ("greeting", "greeting_en"),
                ("hero_title_line1", "hero_title_line1_en"),
                ("hero_title_line2", "hero_title_line2_en"),
                ("typed_prefix", "typed_prefix_en"),
                ("typed_words", "typed_words_en"),
                ("hero_subtitle", "hero_subtitle_en"),
                ("cta_label", "cta_label_en", "cta_link"),
                ("cta2_label", "cta2_label_en", "cta2_link"),
            ),
        }),
        ("À propos", {
            "fields": (
                ("intro_quote", "intro_quote_en"),
                ("bio_paragraph1", "bio_paragraph1_en"),
                ("bio_paragraph2", "bio_paragraph2_en"),
            ),
        }),
        ("Coordonnées & CV", {
            "description": "Les liens GitHub, LinkedIn, WhatsApp… se gèrent dans « Réseaux sociaux ».",
            "fields": (("email", "phone"), ("location", "location_en"), ("cv_file", "cv_file_en")),
        }),
        ("Pied de page", {"fields": (("footer_text", "footer_text_en"),)}),
    )

    @admin.display(description="aperçu")
    def photo_preview(self, obj):
        return image_preview(obj.photo, 110, round_=True)


# ---------------------------------------------------------------------------
# Structure de la page
# ---------------------------------------------------------------------------

@admin.register(Section)
class SectionAdmin(PortfolioAdmin):
    list_display = ("__str__", "nav_label", "title", "is_visible", "show_in_nav", "order")
    list_editable = ("is_visible", "show_in_nav", "order")
    list_display_links = ("__str__",)
    fieldsets = (
        (None, {"fields": ("key", ("is_visible", "show_in_nav", "order"))}),
        ("Textes", {
            "fields": (
                ("nav_label", "nav_label_en"),
                ("eyebrow", "eyebrow_en"),
                ("title", "title_en"),
                ("subtitle", "subtitle_en"),
            ),
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        return ("key",) if obj else ()

    def has_add_permission(self, request):
        return Section.objects.count() < len(Section.KEY_CHOICES)

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Stat)
class StatAdmin(PortfolioAdmin):
    list_display = ("icon", "__str__", "label_en", "order")
    list_editable = ("order",)
    list_display_links = ("__str__",)
    fields = (("value", "suffix"), ("label", "label_en"), "icon_class", "order")

    @admin.display(description="")
    def icon(self, obj):
        return icon_preview(obj)


@admin.register(TechBadge)
class TechBadgeAdmin(PortfolioAdmin):
    list_display = ("preview", "label", "show_around_photo", "position", "show_in_marquee", "order")
    list_editable = ("show_around_photo", "position", "show_in_marquee", "order")
    list_display_links = ("label",)
    fieldsets = (
        (None, {"fields": ("label", "icon_class", "icon_image", "text_color", "order")}),
        ("Affichage", {"fields": (("show_around_photo", "position"), "show_in_marquee")}),
    )

    @admin.display(description="")
    def preview(self, obj):
        if obj.icon_image:
            return image_preview(obj.icon_image, 28)
        if obj.icon_class:
            return format_html('<i class="{}" style="color:{};font-size:1.3rem"></i>', obj.icon_class, obj.text_color)
        return format_html('<b style="color:{}">{}</b>', obj.text_color, obj.label[:3])


# ---------------------------------------------------------------------------
# Contenu
# ---------------------------------------------------------------------------

@admin.register(SkillCategory)
class SkillCategoryAdmin(PortfolioAdmin):
    list_display = ("icon", "title", "tag_line", "order")
    list_editable = ("order",)
    list_display_links = ("title",)
    fields = ("icon_class", ("title", "title_en"), ("description", "description_en"), "tag_line", "order")

    @admin.display(description="")
    def icon(self, obj):
        return icon_preview(obj)


@admin.register(Experience)
class ExperienceAdmin(PortfolioAdmin):
    list_display = ("icon", "title", "organization", "location", "kind", "order")
    list_editable = ("order",)
    list_display_links = ("title",)
    list_filter = ("kind",)
    fields = (
        ("kind", "order"),
        ("title", "title_en"),
        ("organization", "location"),
        ("period", "period_en"),
        ("description", "description_en"),
        "icon_class",
    )

    @admin.display(description="")
    def icon(self, obj):
        return format_html('<i class="{}" style="font-size:1.2rem"></i>', obj.icon())


@admin.register(Project)
class ProjectAdmin(PortfolioAdmin):
    list_display = ("thumb", "title", "status_label", "is_featured", "is_visible", "order")
    list_editable = ("is_featured", "is_visible", "order")
    list_display_links = ("title",)
    list_filter = ("is_visible", "is_featured")
    search_fields = ("title", "description", "tech_stack")
    readonly_fields = ("image_preview",)
    fieldsets = (
        (None, {"fields": (("title", "title_en"), ("status_label", "status_label_en"))}),
        ("Description", {"fields": (("description", "description_en"), "tech_stack")}),
        ("Visuel", {
            "description": "Sans capture d'écran, une illustration est générée avec l'icône choisie.",
            "fields": (("image", "image_preview"), "icon_class"),
        }),
        ("Liens", {"fields": (("link_url", "repo_url"),)}),
        ("Affichage", {"fields": (("is_visible", "is_featured", "order"),)}),
    )

    @admin.display(description="")
    def thumb(self, obj):
        return image_preview(obj.image, 48) if obj.image else icon_preview(obj)

    @admin.display(description="aperçu")
    def image_preview(self, obj):
        return image_preview(obj.image, 140)


@admin.register(SocialLink)
class SocialLinkAdmin(PortfolioAdmin):
    list_display = ("icon", "label", "url", "show_in_hero", "show_in_footer", "order")
    list_editable = ("show_in_hero", "show_in_footer", "order")
    list_display_links = ("label",)
    fields = (("label", "icon_class"), "url", ("show_in_hero", "show_in_footer", "order"))

    @admin.display(description="")
    def icon(self, obj):
        return icon_preview(obj)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("status", "name", "email", "subject", "created_at")
    list_display_links = ("name",)
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "email", "subject", "message")
    readonly_fields = ("name", "email", "subject", "message", "created_at", "reply")
    fields = (("name", "email"), "subject", "message", "created_at", "is_read", "reply")
    actions = ["mark_read", "mark_unread"]

    def has_add_permission(self, request):
        return False

    def change_view(self, request, object_id, form_url="", extra_context=None):
        ContactMessage.objects.filter(pk=object_id, is_read=False).update(is_read=True)
        return super().change_view(request, object_id, form_url, extra_context)

    @admin.display(description="", ordering="is_read")
    def status(self, obj):
        if obj.is_read:
            return mark_safe('<i class="fa-regular fa-envelope-open" style="opacity:.5"></i>')
        return mark_safe('<i class="fa-solid fa-envelope" style="color:var(--primary)"></i>')

    @admin.display(description="répondre")
    def reply(self, obj):
        return format_html(
            '<a class="button" href="mailto:{}?subject={}"><i class="fa-solid fa-reply"></i> Répondre par e-mail</a>',
            obj.email, quote("Re: " + (obj.subject or "votre message")),
        )

    @admin.action(description="Marquer comme lu")
    def mark_read(self, request, queryset):
        queryset.update(is_read=True)

    @admin.action(description="Marquer comme non lu")
    def mark_unread(self, request, queryset):
        queryset.update(is_read=False)
