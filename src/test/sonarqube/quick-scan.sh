#!/bin/bash
# SonarQube Scanner - Análisis Rápido
# ===================================

set -e

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}⚡ SonarQube Scanner - Análisis Rápido${NC}"
echo "======================================"

# Cargar configuración
source .env 2>/dev/null || { echo "❌ Archivo .env no encontrado"; exit 1; }

# Configuración rápida
PROJECT_DIR=$(basename "$(pwd)")
PROJECT_KEY="quick-$(echo "$PROJECT_DIR" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g')"

echo -e "${YELLOW}⚡ Análisis rápido del proyecto: $PROJECT_DIR${NC}"

# Crear configuración mínima
cat > sonar-project.properties << EOF
sonar.projectKey=$PROJECT_KEY
sonar.projectName=Quick Scan - $PROJECT_DIR
sonar.projectVersion=quick
sonar.sources=.
sonar.exclusions=**/node_modules/**,**/vendor/**,**/dist/**,**/build/**,**/.git/**
EOF

# Ejecutar análisis rápido (solo issues básicos)
docker run \
    --rm \
    -e SONAR_HOST_URL="$SONAR_HOST_URL" \
    -e SONAR_TOKEN="$SONAR_TOKEN" \
    -e SONAR_SCANNER_OPTS="-Dsonar.qualitygate.wait=false" \
    -v "$(pwd):/usr/src" \
    --user "$(id -u):$(id -g)" \
    sonarsource/sonar-scanner-cli

echo -e "${GREEN}⚡ Análisis rápido completado!${NC}"
echo -e "${GREEN}📊 Ver: $SONAR_HOST_URL/dashboard?id=$PROJECT_KEY${NC}"

# Limpiar
rm -f sonar-project.properties