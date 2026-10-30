from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand
from django.db.models import FileField

from portfolio.models import Profile, Project, SiteSettings, TechBadge


class Command(BaseCommand):
    help = "Envoie vers le stockage configuré (bucket S3) les fichiers du dossier media/ utilisés par le site."

    def handle(self, *args, **options):
        names = set()
        for obj in [SiteSettings.load(), Profile.load(), *Project.objects.all(), *TechBadge.objects.all()]:
            for field in obj._meta.concrete_fields:
                value = getattr(obj, field.name) if isinstance(field, FileField) else None
                if value:
                    names.add(value.name)

        sent = 0
        for name in sorted(names):
            local = Path(settings.MEDIA_ROOT) / name
            if not local.exists():
                self.stdout.write(self.style.WARNING(f"Introuvable en local : {name}"))
                continue
            if default_storage.exists(name):
                self.stdout.write(f"Déjà en ligne : {name}")
                continue
            with local.open("rb") as fh:
                saved = default_storage.save(name, File(fh))
            if saved != name:
                self.stdout.write(self.style.WARNING(f"Enregistré sous un autre nom : {saved}"))
            self.stdout.write(self.style.SUCCESS(f"Envoyé : {name}"))
            sent += 1
        self.stdout.write(self.style.SUCCESS(f"{sent} fichier(s) envoyé(s)."))
