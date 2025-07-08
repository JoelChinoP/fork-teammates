#!/bin/bash
# SonarQube Scanner - Versión Optimizada con Cache
# ===============================================
# Autor: JoelChinoP
# Fecha: 2025-01-13 23:01:29

set -e

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🔍 SonarQube Scanner - Optimizado${NC}"
echo -e "${BLUE}==================================${NC}"
echo "Autor: JoelChinoP"
echo "Fecha: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# Función para verificar Docker
check_docker() {
    echo -e "${YELLOW}🐳 Verificando Docker...${NC}"
    
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}❌ Docker no está instalado${NC}"
        exit 1
    fi
    
    if ! docker ps &> /dev/null; then
        echo -e "${RED}❌ Docker Desktop no está ejecutándose${NC}"
        echo -e "${YELLOW}💡 Inicia Docker Desktop y vuelve a intentar${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Docker funcionando correctamente${NC}"
}

# Función para crear .env
create_env_file() {
    echo -e "${YELLOW}📝 Configuración inicial...${NC}"
    echo ""
    read -p "🌐 IP de tu VPS SonarQube: " VPS_IP
    read -p "🔑 Token de SonarQube: " TOKEN
    
    cat > .env << EOF
# SonarQube Scanner Config - $(date '+%Y-%m-%d %H:%M:%S')
SONAR_HOST_URL=http://$VPS_IP:9000
SONAR_TOKEN=$TOKEN
SONAR_PROJECT_VERSION=1.0
SONAR_SOURCES=.
SONAR_SOURCE_ENCODING=UTF-8
SONAR_EXCLUSIONS=**/node_modules/**,**/vendor/**,**/*.min.js,**/dist/**,**/build/**,**/.git/**,**/.vscode/**,**/.idea/**
SONAR_COVERAGE_EXCLUSIONS=**/*.test.js,**/*.spec.js,**/tests/**,**/test/**,**/__tests__/**
SONAR_SCM_PROVIDER=git
EOF

    echo -e "${GREEN}✅ Configuración guardada${NC}"
}

# Crear directorio de cache
setup_cache() {
    CACHE_DIR="$HOME/.sonar-scanner-cache"
    
    if [ ! -d "$CACHE_DIR" ]; then
        echo -e "${YELLOW}📦 Creando directorio de cache...${NC}"
        mkdir -p "$CACHE_DIR"
        echo -e "${GREEN}✅ Cache creado: $CACHE_DIR${NC}"
    else
        echo -e "${GREEN}✅ Usando cache existente: $CACHE_DIR${NC}"
    fi
}

# Verificaciones iniciales
check_docker
setup_cache

# Cargar configuración
if [ ! -f ".env" ]; then
    create_env_file
fi

source .env

# Validar configuración
if [ -z "$SONAR_HOST_URL" ] || [ -z "$SONAR_TOKEN" ]; then
    echo -e "${RED}❌ Configuración incompleta${NC}"
    create_env_file
    source .env
fi

# Configurar proyecto
PROJECT_DIR=$(basename "$(pwd)")
PROJECT_KEY="${1:-$(echo "$PROJECT_DIR" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-\|-$//g')}"
PROJECT_NAME="${2:-$PROJECT_DIR}"

# Crear sonar-project.properties
cat > sonar-project.properties << EOF
# SonarQube Project Config - $(date '+%Y-%m-%d %H:%M:%S')
sonar.projectKey=$PROJECT_KEY
sonar.projectName=$PROJECT_NAME
sonar.projectVersion=$SONAR_PROJECT_VERSION
sonar.sources=$SONAR_SOURCES
sonar.sourceEncoding=$SONAR_SOURCE_ENCODING
sonar.exclusions=$SONAR_EXCLUSIONS
sonar.coverage.exclusions=$SONAR_COVERAGE_EXCLUSIONS
sonar.scm.provider=$SONAR_SCM_PROVIDER
EOF

# Mostrar información
echo -e "${BLUE}📋 Configuración:${NC}"
echo "  🏷️  Proyecto: $PROJECT_NAME"
echo "  🔑 Clave: $PROJECT_KEY"
echo "  🌐 Servidor: $SONAR_HOST_URL"
echo "  📁 Código: $(pwd)"
echo "  📦 Cache: $CACHE_DIR"
echo ""

# Verificar servidor
echo -e "${YELLOW}🔗 Verificando SonarQube...${NC}"
if ! timeout 10 curl -s "$SONAR_HOST_URL/api/system/status" &>/dev/null; then
    echo -e "${RED}❌ No se puede conectar con SonarQube${NC}"
    exit 1
fi

# Verificar token
if ! curl -s -u "$SONAR_TOKEN:" "$SONAR_HOST_URL/api/authentication/validate" | grep -q '"valid":true'; then
    echo -e "${RED}❌ Token inválido${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Servidor y token válidos${NC}"

# Ejecutar análisis con cache
echo ""
echo -e "${GREEN}🚀 Iniciando análisis (con cache optimizado)...${NC}"
echo ""

docker run \
    --rm \
    -e SONAR_HOST_URL="$SONAR_HOST_URL" \
    -e SONAR_TOKEN="$SONAR_TOKEN" \
    -v "$CACHE_DIR:/opt/sonar-scanner/.sonar/cache" \
    -v "$(pwd):/usr/src" \
    --user "$(id -u):$(id -g)" \
    sonarsource/sonar-scanner-cli

# Resultado
if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ Análisis completado!${NC}"
    echo -e "${GREEN}📊 Resultados: $SONAR_HOST_URL/dashboard?id=$PROJECT_KEY${NC}"
    
    # Mostrar estadísticas de cache
    if [ -d "$CACHE_DIR" ]; then
        CACHE_SIZE=$(du -sh "$CACHE_DIR" 2>/dev/null | cut -f1 || echo "N/A")
        echo -e "${BLUE}📦 Cache utilizado: $CACHE_SIZE${NC}"
    fi
    
    rm -f sonar-project.properties
else
    echo -e "${RED}❌ Análisis falló${NC}"
    exit 1
fi