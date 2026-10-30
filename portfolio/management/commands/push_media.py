from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand
from django.db.models import FileField

from portfolio.models import Profile, Project, SiteSettings, TechBadge
from portfolio.storage import safe_name


class Command(BaseCommand):
    help = "Envoie vers le stockage configuré (bucket S3) les fichiers du dossier media/ utilisés par le site."

    def handle(self, *args, **options):
        sent = 0
        uploaded = set()
        for obj in [SiteSettings.load(), Profile.load(), *Project.objects.all(), *TechBadge.objects.all()]:
            for field in obj._meta.concrete_fields:
                value = getattr(obj, field.name) if isinstance(field, FileField) else None
                if not value:
                    continue
                name = value.name
                remote = safe_name(name)
                local = Path(settings.MEDIA_ROOT) / name

                if remote not in uploaded:
                    if default_storage.exists(remote):
                        self.stdout.write(f"Déjà en ligne : {remote}")
                    elif not local.exists():
                        self.stdout.write(self.style.WARNING(f"Introuvable en local : {name}"))
                        continue
                    else:
                        with local.open("rb") as fh:
                            remote = default_storage.save(remote, File(fh))
                        self.stdout.write(self.style.SUCCESS(f"Envoyé : {remote}"))
                        sent += 1
                    uploaded.add(remote)

                if remote != name:
                    setattr(obj, field.name, remote)
                    obj.save(update_fields=[field.name])
                    self.stdout.write(f"Renommé : {name} → {remote}")
        self.stdout.write(self.style.SUCCESS(f"{sent} fichier(s) envoyé(s)."))
