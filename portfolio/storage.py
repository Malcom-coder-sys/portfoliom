import re
import unicodedata

from storages.backends.s3 import S3Storage


def safe_name(name):
    """« projects/Prédiction IA.png » → « projects/Prediction_IA.png » (les buckets S3 refusent les accents)."""
    ascii_name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    return re.sub(r"[^A-Za-z0-9._/-]+", "_", ascii_name)


class MediaStorage(S3Storage):
    """Stockage S3 des fichiers envoyés depuis l'admin, avec des noms sans accents ni espaces."""

    def get_valid_name(self, name):
        return safe_name(super().get_valid_name(name))

    def get_available_name(self, name, max_length=None):
        return super().get_available_name(safe_name(name), max_length)
