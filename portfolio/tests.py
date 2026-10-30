from django.test import TestCase
from django.urls import reverse

from .models import ContactMessage, Profile, Section, SiteSettings


class HomeTests(TestCase):
    def test_home_renders_both_languages(self):
        Profile.objects.create(hero_title_line1="Bonjour", hero_title_line1_en="Hello")
        html = self.client.get(reverse("home")).content.decode()
        self.assertIn('<span data-l="fr">Bonjour</span><span data-l="en">Hello</span>', html)

    def test_english_falls_back_to_french(self):
        Profile.objects.create(hero_title_line1="Salut", hero_title_line1_en="")
        html = self.client.get(reverse("home")).content.decode()
        self.assertNotIn('data-l="en">Salut', html)
        self.assertIn("Salut", html)

    def test_hidden_section_is_not_rendered(self):
        Section.objects.filter(key="projects").update(is_visible=False)
        html = self.client.get(reverse("home")).content.decode()
        self.assertNotIn('id="projects"', html)

    def test_settings_colors_injected(self):
        SiteSettings.objects.update_or_create(pk=1, defaults={"accent_color": "#ff0000"})
        self.assertContains(self.client.get(reverse("home")), "--accent: #ff0000")


class ContactTests(TestCase):
    ajax = {"HTTP_X_REQUESTED_WITH": "XMLHttpRequest"}
    data = {"name": "Ada", "email": "ada@example.com", "message": "Salut"}

    def test_valid_message_is_saved(self):
        response = self.client.post(reverse("contact"), self.data, **self.ajax)
        self.assertEqual(response.json(), {"ok": True})
        self.assertEqual(ContactMessage.objects.count(), 1)

    def test_honeypot_is_silently_dropped(self):
        self.client.post(reverse("contact"), {**self.data, "website": "spam"}, **self.ajax)
        self.assertEqual(ContactMessage.objects.count(), 0)

    def test_second_message_is_throttled(self):
        self.client.post(reverse("contact"), self.data, **self.ajax)
        response = self.client.post(reverse("contact"), self.data, **self.ajax)
        self.assertEqual(response.status_code, 429)

    def test_invalid_message_rejected(self):
        response = self.client.post(reverse("contact"), {"name": "", "email": "x"}, **self.ajax)
        self.assertEqual(response.status_code, 400)
