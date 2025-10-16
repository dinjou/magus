#!/bin/bash
# MAGUS Interactive Setup Script
# Generates secure passwords and configures your instance

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Banner
echo -e "${BLUE}"
cat << "EOF"
  __  __    _    ____ _   _ ____  
 |  \/  |  / \  / ___| | | / ___| 
 | |\/| | / _ \| |  _| | | \___ \ 
 | |  | |/ ___ \ |_| | |_| |___) |
 |_|  |_/_/   \_\____|\___/|____/ 
                                   
Personal Time Tracking & Life Analytics
EOF
echo -e "${NC}"

echo -e "${GREEN}=== MAGUS Setup ===${NC}\n"

# Check if .env already exists
if [ -f ".env" ]; then
    echo -e "${YELLOW}⚠️  .env file already exists!${NC}"
    read -p "Do you want to overwrite it? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Setup cancelled. Existing .env preserved."
        exit 0
    fi
    # Backup existing .env
    cp .env .env.backup.$(date +%Y%m%d_%H%M%S)
    echo -e "${GREEN}✓${NC} Backed up existing .env"
fi

# Check for existing Docker volumes that could cause credential mismatches
echo -e "\n${BLUE}Checking for existing Docker volumes...${NC}"

# Try to check for volumes, handle permission errors gracefully
DOCKER_CMD="docker"
if ! docker volume ls &>/dev/null; then
    if [ "$EUID" -ne 0 ]; then
        echo -e "${YELLOW}⚠️  Need elevated permissions to check Docker volumes${NC}"
        echo "   Run this script with sudo to enable volume cleanup"
        DOCKER_CMD="sudo docker"
    fi
fi

EXISTING_VOLUMES=$($DOCKER_CMD volume ls --format '{{.Name}}' 2>/dev/null | grep '^magus_' || true)

if [ ! -z "$EXISTING_VOLUMES" ]; then
    echo -e "${YELLOW}⚠️  Found existing MAGUS Docker volumes:${NC}"
    echo "$EXISTING_VOLUMES" | sed 's/^/  - /'
    echo
    echo -e "${RED}WARNING:${NC} Existing database volumes may have different credentials than your new .env!"
    echo "This WILL cause authentication failures on startup."
    echo
    read -p "Remove all existing MAGUS volumes and start fresh? (RECOMMENDED: y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}Removing existing volumes...${NC}"
        FAILED_REMOVALS=""
        echo "$EXISTING_VOLUMES" | while read vol; do
            if $DOCKER_CMD volume rm "$vol" 2>/dev/null; then
                echo -e "${GREEN}✓${NC} Removed $vol"
            else
                echo -e "${RED}✗${NC} Could not remove $vol"
                FAILED_REMOVALS="$FAILED_REMOVALS $vol"
            fi
        done
        
        if [ ! -z "$FAILED_REMOVALS" ]; then
            echo -e "${YELLOW}⚠️${NC}  Some volumes couldn't be removed. Try:"
            echo "   sudo docker compose -f docker-compose.prod.yml down"
            echo "   sudo docker volume rm magus_postgres_data magus_redis_data"
        else
            echo -e "${GREEN}✓${NC} All old volumes removed - fresh start guaranteed"
        fi
    else
        echo -e "${RED}⚠️  WARNING:${NC} Keeping existing volumes will likely cause startup failures!"
        echo ""
        echo "Before starting MAGUS, you MUST run:"
        echo -e "  ${BLUE}sudo docker compose -f docker-compose.prod.yml down${NC}"
        echo -e "  ${BLUE}sudo docker volume rm magus_postgres_data magus_redis_data${NC}"
        echo ""
        echo "Otherwise, database authentication will fail."
    fi
fi

echo -e "\n${BLUE}Step 1: Domain Configuration${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo
echo "Enter the domain(s) or IP(s) you'll use to access MAGUS."
echo "Examples:"
echo "  - localhost (for local development)"
echo "  - 192.168.1.100 (for local network access)"
echo "  - magus.example.com (for production)"
echo "  - magus.example.com,192.168.1.100 (multiple, comma-separated)"
echo
read -p "Domain(s)/IP(s) [default: localhost]: " DOMAINS
DOMAINS=${DOMAINS:-localhost}

# Clean up input (remove spaces)
DOMAINS=$(echo "$DOMAINS" | tr -d ' ')

# Always include localhost and 127.0.0.1 for local access
if [[ ! "$DOMAINS" == *"localhost"* ]]; then
    DOMAINS="localhost,${DOMAINS}"
fi
if [[ ! "$DOMAINS" == *"127.0.0.1"* ]]; then
    DOMAINS="127.0.0.1,${DOMAINS}"
fi

echo -e "${GREEN}✓${NC} Allowed hosts: ${DOMAINS}"

echo -e "\n${BLUE}Step 2: Environment Mode${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo
echo "Select deployment mode:"
echo "  1) Production (recommended for most users)"
echo "  2) Development (debug mode, verbose logging)"
echo
read -p "Mode [1]: " MODE_CHOICE
MODE_CHOICE=${MODE_CHOICE:-1}

if [ "$MODE_CHOICE" = "2" ]; then
    DEBUG="True"
    echo -e "${YELLOW}⚠️${NC}  Debug mode enabled"
else
    DEBUG="False"
    echo -e "${GREEN}✓${NC} Production mode"
fi

echo -e "\n${BLUE}Step 3: Generating Secure Credentials${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo

# Function to generate secure random password
generate_password() {
    python3 -c "from secrets import token_urlsafe; print(token_urlsafe(32))"
}

# Function to generate Django secret key
generate_secret_key() {
    python3 -c "from secrets import token_urlsafe; print(token_urlsafe(50))"
}

echo -n "Generating Django secret key... "
SECRET_KEY=$(generate_secret_key)
echo -e "${GREEN}✓${NC}"

echo -n "Generating PostgreSQL password... "
POSTGRES_PASSWORD=$(generate_password)
echo -e "${GREEN}✓${NC}"

echo -n "Generating Redis password... "
REDIS_PASSWORD=$(generate_password)
echo -e "${GREEN}✓${NC}"

echo -e "\n${BLUE}Step 4: Email Configuration (Optional)${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo
echo "Email is used for CSV exports. You can skip this and configure later."
echo
read -p "Configure email now? (y/N): " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo
    read -p "SMTP Host (e.g., smtp.gmail.com): " EMAIL_HOST
    read -p "SMTP Port [587]: " EMAIL_PORT
    EMAIL_PORT=${EMAIL_PORT:-587}
    read -p "Use TLS? (Y/n): " -n 1 -r USE_TLS
    echo
    if [[ $USE_TLS =~ ^[Nn]$ ]]; then
        EMAIL_USE_TLS="False"
    else
        EMAIL_USE_TLS="True"
    fi
    read -p "Email Username: " EMAIL_HOST_USER
    read -s -p "Email Password: " EMAIL_HOST_PASSWORD
    echo
    read -p "From Email [noreply@${DOMAINS%%,*}]: " DEFAULT_FROM_EMAIL
    DEFAULT_FROM_EMAIL=${DEFAULT_FROM_EMAIL:-noreply@${DOMAINS%%,*}}
    EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
    echo -e "${GREEN}✓${NC} Email configured"
else
    EMAIL_HOST=""
    EMAIL_PORT="587"
    EMAIL_USE_TLS="True"
    EMAIL_HOST_USER=""
    EMAIL_HOST_PASSWORD=""
    DEFAULT_FROM_EMAIL="noreply@localhost"
    EMAIL_BACKEND="django.core.mail.backends.console.EmailBackend"
    echo -e "${YELLOW}⚠️${NC}  Emails will print to console (dev mode)"
fi

echo -e "\n${BLUE}Step 5: Creating .env file${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo

# Create .env file
cat > .env << EOF
# MAGUS Environment Configuration
# Generated: $(date)

# Django Configuration
DEBUG=${DEBUG}
SECRET_KEY=${SECRET_KEY}

# Domain Configuration
# Add new domains here to enable access from those hostnames/IPs
# CORS and CSRF origins are automatically built from ALLOWED_HOSTS
ALLOWED_HOSTS=${DOMAINS}

# Database Configuration (Internal - Auto-generated)
# These are for the PostgreSQL container and shouldn't need changing
POSTGRES_DB=magus_prod
POSTGRES_USER=magus_user
POSTGRES_PASSWORD=${POSTGRES_PASSWORD}

# Redis Configuration (Internal - Auto-generated)
# Used for caching and Celery task queue
REDIS_PASSWORD=${REDIS_PASSWORD}

# Email Configuration
EMAIL_BACKEND=${EMAIL_BACKEND}
EMAIL_HOST=${EMAIL_HOST}
EMAIL_PORT=${EMAIL_PORT}
EMAIL_USE_TLS=${EMAIL_USE_TLS}
EMAIL_HOST_USER=${EMAIL_HOST_USER}
EMAIL_HOST_PASSWORD=${EMAIL_HOST_PASSWORD}
DEFAULT_FROM_EMAIL=${DEFAULT_FROM_EMAIL}
EOF

echo -e "${GREEN}✓${NC} .env file created"

echo -e "\n${GREEN}=== Setup Complete! ===${NC}\n"

echo "📋 Configuration Summary:"
echo "  • Allowed Hosts: ${DOMAINS}"
echo "  • Debug Mode: ${DEBUG}"
echo "  • Email: $([ -z "$EMAIL_HOST" ] && echo "Console only" || echo "$EMAIL_HOST")"
echo

echo "🚀 Next Steps:"
echo
echo "  1. Start MAGUS:"
echo -e "     ${BLUE}docker compose -f docker-compose.prod.yml up -d${NC}"
echo
echo "  2. Wait for services to be ready (~30 seconds)"
echo
echo "  3. Open in your browser:"
echo -e "     ${BLUE}http://${DOMAINS%%,*}${NC}"
echo
echo "  4. Register your account and start tracking!"
echo

echo "💡 Useful Commands:"
echo -e "  • View logs:    ${BLUE}docker compose -f docker-compose.prod.yml logs -f${NC}"
echo -e "  • Stop:         ${BLUE}docker compose -f docker-compose.prod.yml down${NC}"
echo -e "  • Restart:      ${BLUE}docker compose -f docker-compose.prod.yml restart web${NC}"
echo

echo "📝 Your credentials are saved in .env"
echo "   Keep this file secure and never commit it to version control!"
echo

echo -e "${GREEN}Happy tracking! 📊${NC}"

