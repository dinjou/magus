#!/bin/bash
# Auto-generate secrets for MAGUS if they don't exist
set -e

ENV_FILE="${1:-.env}"

# Function to generate a random password
generate_password() {
    python3 -c "from secrets import token_urlsafe; print(token_urlsafe(32))"
}

# Function to generate Django secret key
generate_secret_key() {
    python3 -c "from secrets import token_urlsafe; print(token_urlsafe(50))"
}

# Create .env if it doesn't exist
if [ ! -f "$ENV_FILE" ]; then
    echo "Creating $ENV_FILE with auto-generated secrets..."
    
    cat > "$ENV_FILE" << EOF
# MAGUS Environment Configuration
# Auto-generated on $(date)

# Django Configuration
DEBUG=False
SECRET_KEY=$(generate_secret_key)

# Domain Configuration (CHANGE THIS!)
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost
CSRF_TRUSTED_ORIGINS=http://localhost:5173,http://localhost

# Internal Database (auto-generated, no need to change)
POSTGRES_DB=magus_prod
POSTGRES_USER=magus_user
POSTGRES_PASSWORD=$(generate_password)

# Internal Redis (auto-generated, no need to change)
REDIS_PASSWORD=$(generate_password)

# Email Configuration (Optional)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL=noreply@localhost
EOF
    
    echo "✅ Created $ENV_FILE with auto-generated passwords"
    echo "⚠️  Update ALLOWED_HOSTS, CORS_ALLOWED_ORIGINS, and CSRF_TRUSTED_ORIGINS for your domain"
else
    echo "✅ $ENV_FILE already exists, skipping generation"
fi

