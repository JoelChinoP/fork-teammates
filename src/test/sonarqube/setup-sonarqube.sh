#!/bin/bash

# ==============================================
# Autor: JoelChinoP
# Fecha: 2025-07-08 23:08:20
# Script para ejecutar docker-compose para SonarQube
# ==============================================

echo "🚀 Configurando SonarQube + CNES Plugin..."

# Crear directorio plugins
mkdir -p ./plugins

# Descargar plugin CNES
echo "⬇️ Descargando CNES plugin..."
curl -L -o ./plugins/sonar-cnes-report-5.0.2.jar \
    "https://github.com/cnescatlab/sonar-cnes-report/releases/download/5.0.2/sonar-cnes-report-5.0.2.jar"

# Verificar descarga
if [ -f "./plugins/sonar-cnes-report-5.0.2.jar" ]; then
    echo "✅ Plugin descargado: $(ls -lh ./plugins/sonar-cnes-report-5.0.2.jar)"
else
    echo "❌ Error al descargar plugin"
    # exit 1
fi

# Iniciar SonarQube
#echo "🐳 Iniciando SonarQube..."
#docker-compose up -d

echo "🎉 ¡Listo!"
#echo "📍 SonarQube: http://localhost:9000"
#echo "👤 Login: admin / admin"