# Portfolio Django

Portfolio bilingue (FR / EN), mode clair / sombre, animé, entièrement piloté depuis l'admin.

## Installation

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Lancer le projet

```bash
python manage.py migrate
python manage.py seed_portfolio   # pré-remplit le contenu FR + EN (sans écraser tes modifications)
python manage.py createsuperuser  # crée ton compte admin
python manage.py runserver
```

- Site : http://127.0.0.1:8000/ (ajoute `?lang=en` pour partager la version anglaise)
- Admin : http://127.0.0.1:8000/admin/
- Tests : `python manage.py test portfolio`

## Ce que tu peux gérer depuis l'admin (/admin/)

| Rubrique | Contenu |
|---|---|
| **Apparence & réglages** | Thème et langue par défaut, 2 couleurs d'accent, fonds clair/sombre, polices, arrondi des cartes, activation de chaque animation (chargement, halo souris, effet 3D, bandeau), boutons FR/EN et clair/sombre, formulaire de contact, SEO, favicon |
| **Profil** | Nom, photo, badges, disponibilité, titres, mots animés, sous-titre, boutons, citation, bio, coordonnées, CV FR et EN, pied de page |
| **Sections de la page** | Renommer, réordonner, masquer chaque section et choisir si elle apparaît dans le menu |
| **Chiffres clés** | Compteurs animés de la section « À propos » |
| **Technologies** | Icônes autour de la photo (position) et bandeau défilant |
| **Compétences / Parcours / Projets** | Cartes, frise chronologique, projets (image ou illustration, lien démo, code source, mise en avant) |
| **Réseaux sociaux** | GitHub, LinkedIn, WhatsApp… avec icône et emplacement (en-tête, pied de page) |
| **Messages reçus** | Messages du formulaire de contact, marquage lu/non lu, bouton « Répondre » |

Chaque texte a une version française et une version anglaise côte à côte.
**Laisse le champ anglais vide pour réutiliser le texte français.**

### Icônes

Les icônes viennent de [Font Awesome 6 (gratuit)](https://fontawesome.com/search?o=r&m=free).
Copie la classe, par exemple `fa-solid fa-code` ou `fa-brands fa-github` : l'admin affiche un aperçu en direct.

## Base de données

Le projet utilise SQLite par défaut (aucune config nécessaire). Pour passer à MySQL,
modifie `DATABASES` dans `config/settings.py` et installe `mysqlclient`.

## Compte admin de démo (à supprimer/changer en production)

- Utilisateur : admin
- Mot de passe : admin1234

## Mise en ligne sur Vercel

Vercel ne conserve pas les fichiers entre deux requêtes : la base SQLite et le dossier `media/`
ne servent qu'en local. En ligne, il faut :

- **une base Postgres** (gratuite chez [Neon](https://neon.tech) ou [Supabase](https://supabase.com)) ;
- **un bucket compatible S3** pour les images et le CV (Supabase Storage, Cloudflare R2…).

Supabase fournit les deux dans un seul projet gratuit.

### 1. Créer la base et le bucket (exemple Supabase)

1. Crée un projet sur supabase.com.
2. **Connect** → copie l'URL *Transaction pooler* (port 6543) : c'est ton `DATABASE_URL`.
3. **Storage** → crée un bucket **public** nommé `media`.
4. **Storage → Settings → S3 Access Keys** → crée une clé. Note l'endpoint, la région, l'ID et le secret.

### 2. Copier ton contenu local vers la production

```bash
# a. Exporter le contenu de la base locale (SQLite), avant de créer le .env
python manage.py dumpdata --exclude contenttypes --exclude auth.permission \
       --exclude sessions --exclude admin.logentry -o data.json

# b. Créer le .env (lu automatiquement) et remplir les valeurs de Supabase
cp .env.example .env

# c. Remplir Postgres et le bucket
python manage.py migrate
python manage.py loaddata data.json
python manage.py push_media   # photos, images des projets, CV
rm data.json
```

Supprime ou renomme le `.env` pour retravailler ensuite sur la base locale.

### 3. Déployer

1. Pousse le projet sur GitHub.
2. Sur vercel.com : **Add New → Project** → importe le dépôt (aucun réglage de build à changer).
3. **Settings → Environment Variables** : ajoute toutes les variables du `.env` (sauf `DJANGO_DEBUG`,
   inutile en production). Génère une clé avec :
   `python -c "import secrets; print(secrets.token_urlsafe(50))"`
4. **Deploy**. Le site est sur `https://<projet>.vercel.app`, l'admin sur `/admin/`.

Pour un domaine personnel, ajoute-le dans `DJANGO_ALLOWED_HOSTS` et `DJANGO_CSRF_TRUSTED_ORIGINS`
(ex. `https://monsite.com`).

### Variables d'environnement

| Variable | Rôle |
|---|---|
| `DJANGO_SECRET_KEY` | Clé secrète Django (obligatoire en production) |
| `DJANGO_DEBUG` | `1` en local uniquement |
| `DJANGO_ALLOWED_HOSTS` | Domaines autorisés, séparés par des virgules |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | Origines HTTPS autorisées pour les formulaires (admin, contact) |
| `DATABASE_URL` | Connexion Postgres |
| `AWS_STORAGE_BUCKET_NAME`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` | Bucket et clés S3 |
| `AWS_S3_ENDPOINT_URL`, `AWS_S3_REGION_NAME` | Adresse et région du service S3 |
| `AWS_S3_CUSTOM_DOMAIN` | Adresse publique des fichiers, ex. `<projet>.supabase.co/storage/v1/object/public/media` |
