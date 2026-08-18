#!/bin/bash
set -e

# Ce VPS est mutualise : le HTTPS et le reverse-proxy public sont deja
# geres par le Caddy du projet kbbot (reseau Docker externe "kbbot_backend").
# Ce script ne demarre donc que l'application elle-meme ; Nginx reste
# uniquement joignable en interne sur ce reseau, jamais sur les ports 80/443
# de l'hote. Voir README pour la ligne a ajouter dans /opt/kbbot/Caddyfile.

if [ ! -f .env ]; then
  echo "❌ Fichier .env manquant. Copiez .env.example vers .env et renseignez les valeurs avant de continuer."
  exit 1
fi

if ! docker network inspect kbbot_backend >/dev/null 2>&1; then
  echo "❌ Le reseau Docker externe 'kbbot_backend' n'existe pas sur cette machine."
  echo "   Il est cree par la stack kbbot (Caddy). Verifiez qu'elle tourne deja."
  exit 1
fi

echo "➡️  [1/3] Construction des images Docker..."
docker compose build

echo "➡️  [2/3] Demarrage de la base de donnees et de Redis..."
docker compose up -d db redis

echo "➡️  [3/3] Demarrage de l'application (Django, Celery, Nginx)..."
docker compose up -d django celery_worker celery_beat nginx

echo "✅ Deploiement termine."
echo "ℹ️  Le site n'est pas encore joignable depuis l'exterieur : il faut"
echo "   ajouter oser-bf.org au Caddyfile partage (/opt/kbbot/Caddyfile)"
echo "   puis recharger Caddy. Voir le README."
