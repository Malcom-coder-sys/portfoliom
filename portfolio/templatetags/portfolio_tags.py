from django import template
from django.template.defaultfilters import linebreaksbr
from django.utils.html import conditional_escape, format_html

register = template.Library()

# Textes fixes de l'interface (FR, EN).
UI = {
    "menu": ("Menu", "Menu"),
    "close": ("Fermer", "Close"),
    "scroll": ("Défiler", "Scroll"),
    "download_cv": ("Télécharger mon CV", "Download my resume"),
    "live": ("Voir le projet", "Live demo"),
    "source": ("Code source", "Source code"),
    "coming_soon": ("Lien bientôt disponible", "Link coming soon"),
    "featured": ("À la une", "Featured"),
    "no_projects": ("Aucun projet pour le moment.", "No projects yet."),
    "name": ("Ton nom", "Your name"),
    "email": ("Ton e-mail", "Your email"),
    "subject": ("Sujet", "Subject"),
    "message": ("Ton message", "Your message"),
    "send": ("Envoyer le message", "Send message"),
    "email_label": ("E-mail", "Email"),
    "phone_label": ("Téléphone", "Phone"),
    "location_label": ("Localisation", "Location"),
    "copy_hint": ("Cliquer pour copier", "Click to copy"),
    "write_me": ("Écris-moi directement", "Or write to me directly"),
    "back_top": ("Haut de page", "Back to top"),
    "crafted": ("Conçu et développé avec", "Designed & built with"),
    "by": ("par", "by"),
}

# Messages utilisés par le JavaScript.
JS_UI = {
    "fr": {
        "sending": "Envoi en cours…",
        "sent": "Merci ! Ton message a bien été envoyé.",
        "error": "Oups, vérifie les champs et réessaie.",
        "copied": "Copié dans le presse-papiers !",
        "throttled": "Patiente quelques secondes avant de renvoyer un message.",
    },
    "en": {
        "sending": "Sending…",
        "sent": "Thanks! Your message has been sent.",
        "error": "Oops, please check the fields and try again.",
        "copied": "Copied to clipboard!",
        "throttled": "Please wait a few seconds before sending another message.",
    },
}


def _both(fr, en, lines=False):
    fr, en = fr or "", en or fr or ""
    if lines:
        fr, en = linebreaksbr(fr), linebreaksbr(en)
    if fr == en:
        return conditional_escape(fr)
    return format_html('<span data-l="fr">{}</span><span data-l="en">{}</span>', fr, en)


@register.simple_tag
def tr(obj, field, lines=False):
    """Affiche un champ dans les deux langues : {% tr profile "hero_subtitle" %}.

    La version anglaise est lue dans `<champ>_en` ; vide, le français est réutilisé.
    """
    if obj is None:
        return ""
    return _both(getattr(obj, field, ""), getattr(obj, f"{field}_en", ""), lines)


@register.simple_tag
def ui(key):
    fr, en = UI.get(key, (key, key))
    return _both(fr, en)
