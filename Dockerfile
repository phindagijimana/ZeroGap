FROM caddy:2-alpine

COPY Caddyfile /etc/caddy/Caddyfile

# Only the assets the site actually serves.
COPY index.html favicon.svg /srv/
COPY css /srv/css
COPY js /srv/js
