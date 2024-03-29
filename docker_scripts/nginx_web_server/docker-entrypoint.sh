#!/bin/bash

# bash script to install nginx web server and configure it
# to serve django application server running in a docker container on port 8000 as a reverse proxy

# check if nginx is already installed then skip installation or else install nginx
if [ -x "$(command -v nginx)" ]; then
    echo "Nginx already installed. Skipping installation."

elif command -v apt-get &> /dev/null; then
    echo "Nginx is not installed. Installing Nginx..."
    apt-get update -y && apt-get install nginx -y
else
    echo "Package manager not found. Please install nginx manually."
    exit 1
fi

# check if ssl certificate already exists then skip installation
if grep -q "ssl_certificate" /etc/nginx/sites-available/hairsol; then
    echo "SSL certificate already exists. Skipping installation."
    service nginx stop
    nginx -g 'daemon off;'
    exit 0
fi

# Remove the default nginx config file and symlink
rm -f /etc/nginx/sites-available/default
rm -f /etc/nginx/sites-enabled/default

# Remove the hairsol config file and symlink if they exist
rm -f /etc/nginx/sites-available/hairsol
rm -f /etc/nginx/sites-enabled/hairsol

# Create a new nginx config file for hairsol
tee /etc/nginx/sites-available/hairsol > /dev/null <<'EOF'
server {
    server_name malzahra.tech;

    location / {
        proxy_pass http://hairsol:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Error pages
    error_page 500 502 503 504 /50x.html;
    location = /50x.html {
        root /usr/share/nginx/html;
    }

    listen 80;
    listen [::]:80;
}
EOF

# Create a symlink to enable the hairsol config
ln -s -f /etc/nginx/sites-available/hairsol /etc/nginx/sites-enabled/

# Test the nginx config
nginx -t

# Reload nginx to apply changes
service nginx reload

# uninstall certbot if it is already installed
apt-get remove -y certbot python3-certbot-nginx && apt-get autoremove -y


# Install Certbot and obtain SSL certificate
apt-get install -y certbot python3-certbot-nginx

# Run Certbot to obtain SSL certificate for the domain in non-interactive mode
certbot --nginx -d malzahra.tech --email abiolaadedayo1993@gmail.com --agree-tos --non-interactive

# Check the exit status of the Certbot command then stop nginx and start it in the foreground if successful
if [ $? -eq 0 ]; then
    echo "SSL configuration  passed."
else
    echo "SSL configuration failed. Please check Certbot logs for details."
    exit 1
fi

# Stop nginx
service nginx stop

# Start nginx in the foreground
nginx -g 'daemon off;'



