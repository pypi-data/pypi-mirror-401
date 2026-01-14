# Auth Bridge + Vikunja
# Nginx serves /slack-connect and /matrix-connect, proxies everything else to Vikunja

FROM vikunja/vikunja:0.24.6 AS vikunja

FROM nginx:alpine

# Install supervisor to run multiple processes
RUN apk add --no-cache supervisor

# Copy Vikunja binary and assets
COPY --from=vikunja /app/vikunja /app/vikunja/

# Create directories for connect pages
RUN mkdir -p /usr/share/nginx/html/slack-connect /usr/share/nginx/html/matrix-connect

# Copy our connect pages
COPY connect.html /usr/share/nginx/html/slack-connect/index.html
COPY matrix-connect.html /usr/share/nginx/html/matrix-connect/index.html

# Fix permissions for nginx user
RUN chmod -R 755 /usr/share/nginx/html/slack-connect /usr/share/nginx/html/matrix-connect && \
    chmod 644 /usr/share/nginx/html/slack-connect/index.html /usr/share/nginx/html/matrix-connect/index.html

# Copy nginx config
COPY nginx.conf /etc/nginx/nginx.conf

# Copy supervisor config
COPY supervisord.conf /etc/supervisord.conf

# Create directories for Vikunja
RUN mkdir -p /app/vikunja/files /db

# Vikunja runs on 3456, nginx on 80
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD wget -q --spider http://localhost/api/v1/info || exit 1

WORKDIR /app/vikunja

CMD ["supervisord", "-c", "/etc/supervisord.conf"]
