from django.core.management.base import BaseCommand

from portfolio.models import (
    Experience, Profile, Project, SiteSettings, SkillCategory, SocialLink, Stat, TechBadge,
)

PROFILE = dict(
    full_name="Tamankeu Songny Yves-Malcom",
    short_name="Yves-Malcom",
    role_badge="Développeur junior en génie logiciel",
    role_badge_en="Junior Software Engineer",
    available=True,
    availability_text="Disponible pour un poste",
    availability_text_en="Open to new opportunities",
    typed_prefix="Je conçois des",
    typed_prefix_en="I build",
    typed_words="applications web, plateformes SIG, automatisations, solutions IA",
    typed_words_en="web applications, GIS platforms, automations, AI solutions",
    hero_subtitle=(
        "Diplômé de l'Institut Africain d'Informatique (IAI), je conçois des applications web "
        "avec Python (Django, Flask), des bases de données relationnelles et des workflows "
        "automatisés — jusqu'aux plateformes SIG de cartographie."
    ),
    hero_subtitle_en=(
        "A graduate of the African Institute of Computer Science (IAI), I build web applications "
        "with Python (Django, Flask), relational databases and automated workflows — "
        "all the way to GIS mapping platforms."
    ),
    bio_paragraph1=(
        "Développeur junior en génie logiciel, diplômé de l'Institut Africain d'Informatique (IAI). "
        "Je conçois des applications web avec Python (Django/Flask), des bases de données "
        "relationnelles et des automatisations de workflows. Mon stage à l'Agence de Régulation "
        "des Télécommunications m'a permis de contribuer à une plateforme SIG web pour le suivi "
        "des sites télécoms."
    ),
    bio_paragraph1_en=(
        "Junior software engineer, graduate of the African Institute of Computer Science (IAI). "
        "I build web applications with Python (Django/Flask), relational databases and workflow "
        "automations. My internship at the Telecommunications Regulatory Board (ART) let me "
        "contribute to a web GIS platform for monitoring telecom sites."
    ),
    bio_paragraph2=(
        "Curieux et adaptable, j'ai aussi des notions d'outils de gestion d'entreprise (ERP Odoo) "
        "et de parc informatique (GLPI). Autonome, rigoureux et doté d'un bon esprit d'équipe, "
        "je souhaite rejoindre une équipe informatique pour réaliser des solutions fiables et "
        "performantes."
    ),
    bio_paragraph2_en=(
        "Curious and adaptable, I also have a working knowledge of business tools (Odoo ERP) and "
        "IT asset management (GLPI). Autonomous, rigorous and a strong team player, I'm looking "
        "to join an IT team to deliver reliable, high-performing solutions."
    ),
    email="songnyyves90@gmail.com",
    phone="674 353 738",
    location="Yaoundé, Cameroun",
    location_en="Yaoundé, Cameroon",
    footer_text="© 2026 Tamankeu Songny — Tous droits réservés.",
    footer_text_en="© 2026 Tamankeu Songny — All rights reserved.",
)

BADGES = [
    dict(label="Python", icon_class="fa-brands fa-python", text_color="#5fb3e3", position="top-left", order=1),
    dict(label="Django", icon_class="", text_color="#3ddc97", position="bottom-left", order=2),
    dict(label="PostgreSQL", icon_class="fa-solid fa-database", text_color="#6ea8e8", position="bottom-right", order=3),
    dict(label="SIG", icon_class="fa-solid fa-map-location-dot", text_color="#5fe3a1", position="top-right", order=4),
    dict(label="Flask", icon_class="fa-solid fa-flask", text_color="#c8ccd6", show_around_photo=False, order=5),
    dict(label="FastAPI", icon_class="fa-solid fa-bolt", text_color="#05998b", show_around_photo=False, order=6),
    dict(label="Java", icon_class="fa-brands fa-java", text_color="#e76f00", show_around_photo=False, order=7),
    dict(label="Laravel", icon_class="fa-brands fa-laravel", text_color="#ff2d20", show_around_photo=False, order=8),
    dict(label="PHP", icon_class="fa-brands fa-php", text_color="#8892bf", show_around_photo=False, order=9),
    dict(label="JavaScript", icon_class="fa-brands fa-js", text_color="#f7df1e", show_around_photo=False, order=10),
    dict(label="HTML5", icon_class="fa-brands fa-html5", text_color="#e8673c", show_around_photo=False, order=11),
    dict(label="CSS3", icon_class="fa-brands fa-css3-alt", text_color="#4c8fe8", show_around_photo=False, order=12),
    dict(label="SQL", icon_class="fa-solid fa-table", text_color="#f5b25f", show_around_photo=False, order=13),
    dict(label="QGIS", icon_class="fa-solid fa-earth-africa", text_color="#93b023", show_around_photo=False, order=14),
    dict(label="n8n", icon_class="fa-solid fa-diagram-project", text_color="#ff6d5a", show_around_photo=False, order=15),
    dict(label="Git", icon_class="fa-brands fa-git-alt", text_color="#f05032", show_around_photo=False, order=16),
    dict(label="IA / LLMs", icon_class="fa-solid fa-brain", text_color="#b28cff", show_around_photo=False, order=17),
    dict(label="Flutter", icon_class="fa-brands fa-google-play", text_color="#54c5f8", show_around_photo=False, order=18),
]

SKILLS = [
    dict(icon_class="fa-solid fa-code", title="Développement Web & Backend",
         title_en="Web & Backend Development",
         description="Applications web complètes, du modèle de données à l'interface, avec Python, PHP ou Java.",
         description_en="Full web applications, from data model to interface, with Python, PHP or Java.",
         tag_line="Python · Django · Flask · FastAPI · Java · Laravel · HTML5 · CSS3 · JavaScript", order=1),
    dict(icon_class="fa-solid fa-database", title="Bases de données", title_en="Databases",
         description="Conception, optimisation et interrogation de bases relationnelles, y compris spatiales.",
         description_en="Designing, optimising and querying relational databases, spatial ones included.",
         tag_line="SQL · MySQL · PostgreSQL · PostGIS", order=2),
    dict(icon_class="fa-solid fa-map-location-dot", title="SIG & Cartographie", title_en="GIS & Mapping",
         description="Plateformes web cartographiques : données spatiales, visualisation et consultation.",
         description_en="Web mapping platforms: spatial data, visualisation and map browsing tools.",
         tag_line="QGIS · OpenStreetMap · GeoDjango · GeoJSON", order=3),
    dict(icon_class="fa-solid fa-gears", title="Automatisation & Outils", title_en="Automation & Tools",
         description="Automatisation de workflows de données et travail collaboratif versionné.",
         description_en="Data workflow automation and version-controlled teamwork.",
         tag_line="n8n · Git · Visual Studio Code", order=4),
    dict(icon_class="fa-solid fa-brain", title="IA & Analyse de données", title_en="AI & Data Analysis",
         description="Intégration de LLMs en local et analyse de données pour des cas d'usage concrets.",
         description_en="Local LLM integration and data analysis for real-world use cases.",
         tag_line="Ollama · LLM · Pandas · NumPy · scikit-learn · Matplotlib", order=5),
    dict(icon_class="fa-solid fa-briefcase", title="Outils métier", title_en="Business Tools",
         description="Notions d'ERP (ventes, stocks, CRM, facturation PME) et de gestion de parc informatique "
                     "(incidents, ticketing).",
         description_en="Working knowledge of ERP (sales, stock, CRM, SME invoicing) and IT asset management "
                        "(incidents, ticketing).",
         tag_line="Odoo (ERP) · GLPI (ITSM)", order=6),
]

PROJECTS = [
    dict(status_label="Projet personnel", status_label_en="Personal project",
         title="Entreprend237", icon_class="fa-solid fa-handshake", is_featured=True,
         description=(
             "Plateforme camerounaise qui met en relation porteurs de projets, investisseurs et "
             "souteneurs : profils vérifiés, opportunités d'investissement, messagerie et visio, "
             "accords et paiements mobiles, business plans assistés par IA. Sécurité renforcée "
             "(double authentification, limitation des connexions) et sauvegardes vérifiées."),
         description_en=(
             "Cameroonian platform connecting project founders, investors and supporters: verified "
             "profiles, investment opportunities, messaging and video calls, agreements and mobile "
             "payments, AI-assisted business plans. Hardened security (two-factor authentication, "
             "login throttling) and verified backups."),
         tech_stack="Django, PostgreSQL, Tailwind CSS, NotchPay, Twilio, Jitsi, IA", repo_url="https://github.com/Malcom-coder-sys/Entreprend237", order=1),
    dict(status_label="Projet personnel", status_label_en="Personal project",
         title="Agent IA d'analyse de données", title_en="AI Data Analysis Agent",
         icon_class="fa-solid fa-robot", is_featured=True,
         description=(
             "Agent conversationnel qui interroge une base de données en langage naturel : "
             "il génère et exécute les requêtes SQL, répond en français, propose des graphiques "
             "et peut ajouter des enregistrements. Tableau de bord des ventes, historique des "
             "conversations et authentification."),
         description_en=(
             "Conversational agent that queries a database in plain language: it writes and runs "
             "the SQL, answers in French, suggests charts and can insert records. Includes a sales "
             "dashboard, conversation history and authentication."),
         tech_stack="Django, LangGraph, LangChain, Ollama, MySQL, Plotly, Pandas",
         repo_url="https://github.com/Malcom-coder-sys/agent-web", order=2),
    dict(status_label="Projet de stage", status_label_en="Internship project",
         title="Plateforme SIG des sites télécoms", title_en="Telecom Sites GIS Platform",
         icon_class="fa-solid fa-tower-cell",
         description=(
             "Plateforme SIG web de l'Agence de Régulation des Télécommunications pour la "
             "cartographie et le suivi des sites télécoms et de leurs servitudes : données "
             "spatiales, visualisation et outils de consultation cartographique."),
         description_en=(
             "Web GIS platform for the Telecommunications Regulatory Board, mapping and monitoring "
             "telecom sites and their easements: spatial data, visualisation and map browsing tools."),
         tech_stack="Django, GeoDjango, PostgreSQL, PostGIS, GeoJSON", repo_url="https://github.com/ART-Malcom/sig-art", order=3),
    dict(status_label="Site d'entreprise", status_label_en="Business website",
         title="MOVE&CO", icon_class="fa-solid fa-truck-fast",
         description=(
             "Site d'une entreprise de déménagement, transport de colis et aménagement intérieur à "
             "Yaoundé : services, galerie filtrable et demande en ligne. Espace administrateur avec "
             "statistiques, graphiques et suivi des commandes."),
         description_en=(
             "Website for a moving, parcel delivery and interior fitting company in Yaoundé: services, "
             "filterable gallery and online requests. Admin area with statistics, charts and order "
             "tracking."),
         tech_stack="Django, MySQL, JavaScript, Chart.js", repo_url="https://github.com/Malcom-coder-sys/Move-co", order=4),
    dict(status_label="Projet personnel", status_label_en="Personal project",
         title="Prédiction du risque cardiaque", title_en="Heart Disease Risk Prediction",
         icon_class="fa-solid fa-heart-pulse",
         description=(
             "Application qui estime le risque de maladie cardiaque à partir des données cliniques "
             "d'un patient grâce à un modèle Random Forest, affiche la probabilité et le niveau de "
             "risque, puis génère un rapport PDF."),
         description_en=(
             "App that estimates a patient's heart disease risk from clinical data with a Random "
             "Forest model, shows the probability and risk level, then generates a PDF report."),
         tech_stack="Django, scikit-learn, NumPy, joblib, ReportLab", repo_url="https://github.com/Malcom-coder-sys/cardic-app", order=5),
    dict(status_label="Projet personnel", status_label_en="Personal project",
         title="Gestion École", title_en="School Management",
         icon_class="fa-solid fa-school",
         description=(
             "Application de gestion d'une école primaire avec deux espaces : la directrice gère "
             "élèves et classes depuis son tableau de bord, les enseignants consultent leur classe. "
             "Notes, absences et bulletins en cours de développement."),
         description_en=(
             "Primary school management app with two areas: the head teacher manages pupils and "
             "classes from a dashboard, teachers view their class. Grades, absences and report cards "
             "in progress."),
         tech_stack="Flask, SQLAlchemy, Flask-Login, MySQL", repo_url="https://github.com/Malcom-coder-sys/Gestion_ecole", order=6),
    dict(status_label="Projet personnel", status_label_en="Personal project",
         title="Medicare AI", icon_class="fa-solid fa-hospital-user",
         description=(
             "Plateforme de gestion médicale : comptes par rôle (patient, médecin, administrateur), "
             "dossiers patients, profils de médecins et prise de rendez-vous avec suivi du statut. "
             "Consultations et ordonnances en cours de développement."),
         description_en=(
             "Medical management platform: role-based accounts (patient, doctor, admin), patient "
             "records, doctor profiles and appointment booking with status tracking. Consultations "
             "and prescriptions in progress."),
         tech_stack="Django, Python", repo_url="https://github.com/Malcom-coder-sys/Medicaire", order=7),
    dict(status_label="Projet personnel", status_label_en="Personal project",
         title="Gestion de stock", title_en="Stock Management",
         icon_class="fa-solid fa-boxes-stacked",
         description=(
             "Application de gestion de stock : catalogue de produits, enregistrement des entrées "
             "et sorties de stock, et tableau de bord de synthèse."),
         description_en=(
             "Stock management app: product catalogue, stock in/out movements and a summary dashboard."),
         tech_stack="Laravel, PHP, Vite", repo_url="https://github.com/Malcom-coder-sys/Stock", order=8),
    dict(status_label="Projet d'équipe", status_label_en="Team project",
         title="MobiLink", icon_class="fa-solid fa-bus",
         description=(
             "Frontend d'une plateforme de mobilité inter-urbaine camerounaise, avec "
             "paiement mobile (MTN MoMo, Orange Money) intégré."),
         description_en=(
             "Frontend of a Cameroonian intercity mobility platform with built-in mobile "
             "payments (MTN MoMo, Orange Money)."),
         tech_stack="Next.js, React, TypeScript, Tailwind CSS", repo_url="https://github.com/Kymkeyssel/revue-de-projet", order=9),
    dict(status_label="Projet personnel", status_label_en="Personal project",
         title="Rappel Vocal", icon_class="fa-solid fa-microphone-lines",
         description=(
             "Application de rappels vocaux pour Linux : rappels ponctuels, quotidiens ou "
             "hebdomadaires, notification système et lecture du message à voix haute avec "
             "une synthèse vocale 100 % hors-ligne. Une API permet de piloter les rappels "
             "depuis n8n."),
         description_en=(
             "Voice reminder app for Linux: one-off, daily or weekly reminders, desktop "
             "notification and the message read aloud with fully offline text-to-speech. "
             "An API lets n8n drive the reminders."),
         tech_stack="Django, Piper TTS, APScheduler, MySQL, n8n",
         repo_url="https://github.com/Malcom-coder-sys/Rappel", order=10),
]

SOCIALS = [
    dict(label="GitHub", icon_class="fa-brands fa-github", url="https://github.com/Malcom-coder-sys", order=1),
    dict(label="Email", icon_class="fa-solid fa-envelope", url=f"mailto:{PROFILE['email']}", order=3),
]

EXPERIENCES = [
    dict(kind="work", title="Stagiaire Développeur SIG", title_en="GIS Developer Intern",
         organization="Agence de Régulation des Télécommunications (ART)", location="Bafoussam",
         icon_class="fa-solid fa-map-location-dot",
         description=(
             "Contribution au développement d'une plateforme SIG web pour la cartographie et le suivi "
             "des sites télécoms et de leurs servitudes.\n"
             "Manipulation et requêtes de données spatiales avec Django, Python et PostgreSQL/PostGIS.\n"
             "Implémentation d'interfaces de visualisation et d'outils de consultation cartographique."),
         description_en=(
             "Contributed to a web GIS platform for mapping and monitoring telecom sites and their "
             "easements.\n"
             "Handled and queried spatial data with Django, Python and PostgreSQL/PostGIS.\n"
             "Implemented visualisation interfaces and map browsing tools."),
         order=1),
    dict(kind="work", title="Stagiaire Développeur Web & Automatisation",
         title_en="Web Development & Automation Intern",
         organization="OPTIMO Cameroun", location="Douala", icon_class="fa-solid fa-gears",
         description=(
             "Conception et optimisation de bases de données relationnelles sous MySQL.\n"
             "Mise en place d'automatismes de workflows de données avec n8n.\n"
             "Développement de modules web complémentaires avec Django."),
         description_en=(
             "Designed and optimised relational databases with MySQL.\n"
             "Set up automated data workflows with n8n.\n"
             "Built additional web modules with Django."),
         order=2),
    dict(kind="work", title="Stagiaire Développeur PHP", title_en="PHP Developer Intern",
         organization="EUREKA", location="Douala", icon_class="fa-brands fa-php",
         description=(
             "Programmation en PHP, analyse de problèmes et résolution technique au sein de l'équipe.\n"
             "Collaboration avec d'autres stagiaires sur des projets applicatifs de groupe."),
         description_en=(
             "PHP programming, problem analysis and technical troubleshooting within the team.\n"
             "Worked with fellow interns on group application projects."),
         order=3),
    dict(kind="work", title="Stagiaire Support Informatique", title_en="IT Support Intern",
         organization="ZARATOURA", icon_class="fa-solid fa-headset",
         description="Prise en main des équipements informatiques et assistance bureautique auprès du personnel.",
         description_en="Set up IT equipment and provided office software support to staff.",
         order=4),
    dict(kind="education", title="Diplôme d'Ingénieur de Travaux Informatiques",
         title_en="Computer Engineering Degree (Ingénieur de Travaux)",
         organization="Institut Africain d'Informatique (IAI)", order=5),
    dict(kind="education", title="Licence Professionnelle", title_en="Professional Bachelor's Degree",
         organization="Institut Africain d'Informatique (IAI)", order=6),
    dict(kind="education", title="Diplôme de Technicien Supérieur (DTS)", title_en="Higher Technician Diploma (DTS)",
         organization="Institut Africain d'Informatique (IAI)", order=7),
    dict(kind="education", title="Baccalauréat D", title_en="Baccalaureate (Science, series D)",
         order=8),
]

STATS = [
    dict(value=4, suffix="", label="Stages en entreprise", label_en="Company internships",
         icon_class="fa-solid fa-briefcase", order=1),
    dict(value=10, suffix="", label="Projets réalisés", label_en="Projects built",
         icon_class="fa-solid fa-rocket", order=2),
    dict(value=25, suffix="+", label="Technologies maîtrisées", label_en="Technologies mastered",
         icon_class="fa-solid fa-layer-group", order=3),
    dict(value=3, suffix="", label="Diplômes IAI", label_en="IAI degrees",
         icon_class="fa-solid fa-graduation-cap", order=4),
]


def fill_blanks(obj, values, force=False):
    """Complète les champs vides (ou restés à leur valeur par défaut) sans écraser
    ce qui a été saisi dans l'admin. Avec force=True, remplace tout."""
    def untouched(field):
        current = getattr(obj, field)
        return current in ("", None) or current == obj._meta.get_field(field).get_default()

    changed = [f for f, v in values.items() if (force or (v and untouched(f))) and getattr(obj, f) != v]
    for field in changed:
        setattr(obj, field, values[field])
    if changed:
        obj.save()


class Command(BaseCommand):
    help = (
        "Pré-remplit le portfolio avec le contenu de départ (FR + EN). "
        "Sans risque : les champs déjà remplis depuis l'admin ne sont jamais écrasés, "
        "sauf avec --force."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--force", action="store_true",
            help="Remplace le contenu existant par celui du CV (profil, compétences, parcours…).",
        )

    def handle(self, *args, force=False, **options):
        SiteSettings.load()
        fill_blanks(Profile.load(), PROFILE, force)

        for model, rows, key in [
            (TechBadge, BADGES, "label"),
            (SkillCategory, SKILLS, "title"),
            (Project, PROJECTS, "title"),
            (Experience, EXPERIENCES, "title"),
            (Stat, STATS, "label"),
        ]:
            for row in rows:
                obj, created = model.objects.get_or_create(**{key: row[key]}, defaults=row)
                if not created:
                    fill_blanks(obj, row, force)

        for row in SOCIALS:
            SocialLink.objects.get_or_create(label=row["label"], defaults=row)

        self.stdout.write(self.style.SUCCESS("Portfolio pré-rempli avec succès."))
