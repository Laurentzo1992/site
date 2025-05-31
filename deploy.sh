#!/bin/bash

# === CONFIGURATION ===
DOMAIN="oser-bf.org"
EMAIL="infos@oser-bf.org"

echo "➡️  [1/6] Construction des conteneurs Docker..."
docker-compose up --build -d

echo "➡️  [2/6] Attente du démarrage des services..."
sleep 10

echo "➡️  [3/6] Génération des certificats SSL Let's Encrypt..."
docker-compose run --rm certbot \
  certonly --webroot \
  --webroot-path=/var/www/site/static \
  --email "$EMAIL" \
  --agree-tos \
  --no-eff-email \
  -d "$DOMAIN"

if [ $? -eq 0 ]; then
  echo "✅ Certificats SSL générés avec succès."
else
  echo "❌ Échec de la génération des certificats SSL."
  exit 1
fi

echo "➡️  [4/6] Redémarrage du reverse proxy Nginx avec HTTPS..."
docker-compose restart nginx

echo "➡️  [5/6] Création de la tâche cron pour le renouvellement SSL..."

(crontab -l 2>/dev/null; echo "0 3 * * 1 cd $(pwd) && docker-compose run --rm certbot renew --quiet && docker-compose restart nginx") | crontab -

echo "✅ Déploiement terminé avec succès !"
echo "🌐 Votre application est disponible sur : https://$DOMAIN"
