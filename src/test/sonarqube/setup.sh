#!/bin/bash
# Setup inicial del Scanner SonarQube
# ==================================

echo "🛠️  Configuración SonarQube Scanner"
echo "=================================="

# Crear .env si no existe
if [ ! -f ".env" ]; then
    echo "📝 Creando archivo .env..."
    
    cat > .env << 'EOF'
# Configuración SonarQube Scanner
# ===============================

# URL del servidor SonarQube (CAMBIAR por la IP de tu VPS)
SONAR_HOST_URL=http://TU_VPS_IP:9000

# Token de autenticación (generar en SonarQube: Administration > Security > Users)
SONAR_TOKEN=TU_TOKEN_AQUI

# Configuraciones del proyecto
SONAR_PROJECT_VERSION=1.0
SONAR_SOURCES=.
SONAR_SOURCE_ENCODING=UTF-8

# Exclusiones comunes
SONAR_EXCLUSIONS=**/node_modules/**,**/vendor/**,**/*.min.js,**/dist/**,**/build/**,**/.git/**,**/.vscode/**,**/.idea/**
SONAR_COVERAGE_EXCLUSIONS=**/*.test.js,**/*.spec.js,**/tests/**,**/test/**,**/__tests__/**

# Git provider
SONAR_SCM_PROVIDER=git
EOF

    echo "✅ Archivo .env creado"
    echo ""
    echo "🔧 EDITA .env con:"
    echo "   - La IP real de tu VPS"
    echo "   - Tu token de SonarQube"
else
    echo "✅ .env ya existe"
fi

# Hacer ejecutables los scripts
chmod +x *.sh 2>/dev/null || true

# Crear .gitignore
if [ ! -f ".gitignore" ]; then
    echo "sonar-project.properties" >> .gitignore
    echo ".scannerwork/" >> .gitignore
fi

echo ""
echo "📋 Comandos disponibles:"
echo "   ./quick-scan.sh                    - Análisis rápido"
echo "   ./sonar-scan.sh                    - Análisis completo"
echo "   ./sonar-scan.sh mi-app \"Mi App\"    - Con nombre específico"
echo ""
echo "🎯 ¡Listo! Edita .env y ejecuta los scanners"