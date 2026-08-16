#!/bin/bash
set -e

# === CONFIGURATION ===
DOMAIN="oser-bf.org"
EMAIL="infos@oser-bf.org"

if [ ! -f .env ]; then
  echo "❌ Fichier .env manquant. Copiez .env.example vers .env et renseignez les valeurs avant de continuer."
  exit 1
fi

echo "➡️  [1/7] Construction des images Docker..."
docker compose build

echo "➡️  [2/7] Démarrage de la base de données et de Redis..."
docker compose up -d db redis

echo "➡️  [3/7] Préparation du certificat (placeholder si aucun certificat n'existe encore)..."
if ! docker compose run --rm --entrypoint sh certbot -c "[ -f /etc/letsencrypt/live/$DOMAIN/fullchain.pem ]"; then
  docker compose run --rm --entrypoint sh certbot -c "
    mkdir -p /etc/letsencrypt/live/$DOMAIN &&
    openssl req -x509 -nodes -newkey rsa:2048 -days 1 \
      -keyout /etc/letsencrypt/live/$DOMAIN/privkey.pem \
      -out /etc/letsencrypt/live/$DOMAIN/fullchain.pem \
      -subj '/CN=$DOMAIN'
  "
  NEEDS_REAL_CERT=1
else
  NEEDS_REAL_CERT=0
fi

echo "➡️  [4/7] Démarrage de l'application (Django, Celery, Nginx)..."
docker compose up -d django celery_worker celery_beat nginx

if [ "$NEEDS_REAL_CERT" -eq 1 ]; then
  echo "➡️  [5/7] Génération du certificat SSL Let's Encrypt..."
  docker compose run --rm --entrypoint sh certbot -c "
    rm -rf /etc/letsencrypt/live/$DOMAIN /etc/letsencrypt/archive/$DOMAIN /etc/letsencrypt/renewal/$DOMAIN.conf &&
    certbot certonly --webroot \
      --webroot-path=/var/www/site/static \
      --email $EMAIL \
      --agree-tos \
      --no-eff-email \
      -d $DOMAIN
  "

  if [ $? -eq 0 ]; then
    echo "✅ Certificat SSL généré avec succès."
  else
    echo "❌ Échec de la génération du certificat SSL."
    exit 1
  fi

  echo "➡️  [6/7] Redémarrage de Nginx avec le certificat définitif..."
  docker compose restart nginx
else
  echo "➡️  [5/7] Certificat SSL déjà présent, pas de nouvelle demande."
  echo "➡️  [6/7] (rien à faire)"
fi

echo "➡️  [7/7] Création de la tâche cron pour le renouvellement SSL..."
(crontab -l 2>/dev/null; echo "0 3 * * 1 cd $(pwd) && docker compose run --rm certbot renew --quiet && docker compose restart nginx") | crontab -

echo "✅ Déploiement terminé avec succès !"
echo "🌐 Votre application est disponible sur : https://$DOMAIN"
