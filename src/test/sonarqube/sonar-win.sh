#!/bin/bash
# ==============================================
# Autor: JoelChinoP
# Fecha: 2025-07-08 23:08:20

# Script para ejecutar SonarQube Scanner en Linux
# Autor: JoelChinoP
# Fecha: 2025-07-09

set -e  # Salir si hay error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="$SCRIPT_DIR/.env"
SCANNER_DIR="$SCRIPT_DIR/scanner"
CONF_FILE="$SCANNER_DIR/conf/sonar-scanner.properties"

# Verificar archivos necesarios
[[ ! -f "$ENV_FILE" ]] && { echo "Error: .env no encontrado en $ENV_FILE"; exit 1; }
[[ ! -d "$SCANNER_DIR" ]] && { echo "Error: carpeta scanner no encontrada"; exit 1; }
[[ ! -f "$CONF_FILE" ]] && { echo "Error: sonar-scanner.properties no encontrado"; exit 1; }

echo "🔧 Configurando SonarQube Scanner..."

# Cargar variables del .env
export $(grep -v '^#' "$ENV_FILE" | grep -v '^$' | xargs)

# Actualizar sonar-scanner.properties
cat > "$CONF_FILE" << EOF
# Configuración generada automáticamente - $(date)
sonar.host.url=$SONAR_HOST_URL
sonar.log.level=$SONAR_LOG_LEVEL
EOF

# Crear sonar-project.properties temporal
PROJECT_PROPS="$SCRIPT_DIR/sonar-project.properties"
cat > "$PROJECT_PROPS" << EOF
# Configuración del proyecto generada automáticamente
sonar.projectKey=$SONAR_PROJECT_KEY
sonar.projectName=$SONAR_PROJECT_NAME
sonar.projectVersion=$SONAR_PROJECT_VERSION
sonar.sources=$SONAR_SOURCES
sonar.sourceEncoding=$SONAR_SOURCE_ENCODING
sonar.exclusions=$SONAR_EXCLUSIONS
sonar.coverage.exclusions=$SONAR_COVERAGE_EXCLUSIONS
sonar.cpd.exclusions=$SONAR_DUPLICATION_EXCLUSIONS
sonar.java.binaries=$SONAR_JAVA_BINARIES
sonar.javascript.lcov.reportPaths=$SONAR_JAVASCRIPT_LCOV_REPORT_PATHS
EOF

# Configurar variables de entorno para el scanner
export SONAR_SCANNER_JAVA_OPTS="$SONAR_SCANNER_JAVA_OPTS"
export SONAR_TOKEN="$SONAR_TOKEN"

echo "📊 Iniciando análisis de SonarQube..."
echo "Proyecto: $SONAR_PROJECT_NAME ($SONAR_PROJECT_KEY)"
echo "Servidor: $SONAR_HOST_URL"

# Ejecutar scanner
"$SCANNER_DIR/bin/sonar-scanner.bat" \
    -Dproject.settings="$PROJECT_PROPS" \
    -Dsonar.verbose="$SONAR_VERBOSE"

# Limpiar archivo temporal
rm -f "$PROJECT_PROPS"

echo "✅ Análisis completado. Revisa los resultados en: $SONAR_HOST_URL"