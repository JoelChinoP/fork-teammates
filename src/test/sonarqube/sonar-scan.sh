#!/bin/bash
# SonarQube Scanner - Análisis completo
# ====================================

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🔍 SonarQube Scanner - Análisis Completo${NC}"
echo "========================================"

# Verificar Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker no está instalado${NC}"
    exit 1
fi

# Cargar configuración
if [ ! -f ".env" ]; then
    echo -e "${RED}❌ Archivo .env no encontrado${NC}"
    echo -e "${YELLOW}💡 Ejecuta ./setup.sh primero${NC}"
    exit 1
fi

source .env

# Validar configuración
if [[ "$SONAR_HOST_URL" == *"TU_VPS_IP"* ]] || [[ "$SONAR_TOKEN" == *"TU_TOKEN"* ]]; then
    echo -e "${RED}❌ Configura primero tu IP y token en .env${NC}"
    exit 1
fi

# Obtener información del proyecto
PROJECT_DIR=$(basename "$(pwd)")
PROJECT_KEY="${1:-$(echo "$PROJECT_DIR" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g')}"
PROJECT_NAME="${2:-$PROJECT_DIR}"

# Crear sonar-project.properties
echo -e "${YELLOW}📝 Configurando proyecto...${NC}"
cat > sonar-project.properties << EOF
# Configuración SonarQube - $(date)
sonar.projectKey=$PROJECT_KEY
sonar.projectName=$PROJECT_NAME
sonar.projectVersion=$SONAR_PROJECT_VERSION
sonar.sources=$SONAR_SOURCES
sonar.sourceEncoding=$SONAR_SOURCE_ENCODING
sonar.exclusions=$SONAR_EXCLUSIONS
sonar.coverage.exclusions=$SONAR_COVERAGE_EXCLUSIONS
sonar.scm.provider=$SONAR_SCM_PROVIDER
EOF

# Mostrar configuración
echo -e "${BLUE}📋 Configuración:${NC}"
echo "  🏷️  Proyecto: $PROJECT_NAME"
echo "  🔑 Clave: $PROJECT_KEY"
echo "  🌐 Servidor: $SONAR_HOST_URL"
echo "  📁 Directorio: $(pwd)"

# Verificar conectividad
echo -e "${YELLOW}🔗 Verificando servidor...${NC}"
if ! timeout 10 curl -s "$SONAR_HOST_URL/api/system/status" &>/dev/null; then
    echo -e "${RED}❌ No se puede conectar con SonarQube${NC}"
    echo -e "${YELLOW}💡 Verifica que SonarQube esté ejecutándose en $SONAR_HOST_URL${NC}"
    exit 1
fi

# Ejecutar análisis
echo -e "${GREEN}🚀 Iniciando análisis completo...${NC}"
echo "⏱️  Este proceso puede tomar varios minutos..."

docker run \
    --rm \
    -e SONAR_HOST_URL="$SONAR_HOST_URL" \
    -e SONAR_TOKEN="$SONAR_TOKEN" \
    -v "$(pwd):/usr/src" \
    --user "$(id -u):$(id -g)" \
    sonarsource/sonar-scanner-cli

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ Análisis completado exitosamente!${NC}"
    echo -e "${GREEN}📊 Ver resultados: $SONAR_HOST_URL/dashboard?id=$PROJECT_KEY${NC}"
    
    # Limpiar archivo temporal
    rm -f sonar-project.properties
else
    echo -e "${RED}❌ El análisis falló${NC}"
    exit 1
fi