# SonarQube Scanner - Cigarra Teammates

## 📋 Descripción

Este directorio contiene la configuración completa para ejecutar análisis de código con SonarQube en el proyecto Cigarra-Teammates. Incluye scripts automatizados para Linux y Windows, configuración mediante variables de entorno y opción de ejecutar SonarQube Server localmente con Docker.

## 📁 Estructura del Directorio

```
src/test/sonarqube/
├── scanner/                    # SonarScanner CLI (ver README en scanner/)
│   ├── bin/
│   ├── conf/
│   ├── jre/
│   └── lib/
├── .env                        # Variables de configuración
├── docker-compose.yml          # SonarQube Server local
├── sonar-linux.sh             # Script para Linux/macOS
├── sonar-win.sh               # Script para Windows
└── README.md                  # Este archivo
```

## 🚀 Inicio Rápido

### Opción 1: Usar SonarQube Server Remoto
```bash
# Linux/macOS
./sonar-linux.sh

# Windows
./sonar-win.sh
```

### Opción 2: Ejecutar SonarQube Server Local
```bash
# Iniciar SonarQube Server
docker-compose up -d

# Esperar a que esté disponible (http://localhost:9000)
# Configurar proyecto y obtener token

# Actualizar .env con URL local
# SONAR_HOST_URL=http://localhost:9000

# Ejecutar análisis
./sonar-linux.sh  # o ./sonar-win.sh
```

## ⚙️ Configuración (.env)

El archivo `.env` contiene todas las variables necesarias para el análisis:

### Variables Obligatorias
```bash
# Identificador único del proyecto en SonarQube
SONAR_PROJECT_KEY=cigarra-teammates

# Nombre descriptivo del proyecto
SONAR_PROJECT_NAME=Cigarra-Teammates

# URL del servidor SonarQube (remoto o local)
SONAR_HOST_URL=http://34.95.154.160:9000

# Token de autenticación (generar en SonarQube)
SONAR_TOKEN=squ_f20ff50256ee3b562745fd549c236c2139259a31
```

### Variables de Proyecto
```bash
# Versión del proyecto
SONAR_PROJECT_VERSION=1.0

# Directorio del código fuente (relativo a esta carpeta)
SONAR_SOURCES=../../../

# Codificación de archivos
SONAR_SOURCE_ENCODING=UTF-8
```

### Exclusiones y Filtros
```bash
# Archivos/carpetas a excluir del análisis
SONAR_EXCLUSIONS=**/node_modules/**,**/.vscode/**,**/.idea/**,**/.angular/**,**/.gradle/**,**/bin/**,**/dist/**,**/build/**,**/target/**,**/*.min.js,**/*.bundle.js

# Exclusiones para cobertura de código (opcional)
# SONAR_COVERAGE_EXCLUSIONS=**/*test*/**,**/*spec*/**,**/*mock*/**

# Exclusiones para detección de duplicados (opcional)
# SONAR_DUPLICATION_EXCLUSIONS=**/*test*/**,**/*spec*/**
```

### Variables Específicas del Lenguaje
```bash
# Rutas de archivos compilados Java (opcional)
# SONAR_JAVA_BINARIES=../../../build/classes

# Reportes de cobertura JavaScript (opcional)
# SONAR_JAVASCRIPT_LCOV_REPORT_PATHS=../../../coverage/lcov.info
```

### Configuración de Rendimiento
```bash
# Memoria asignada al scanner (opcional)
# SONAR_SCANNER_JAVA_OPTS=-Xmx2048m -XX:MaxPermSize=256m

# Nivel de logging
SONAR_LOG_LEVEL=INFO

# Activar logs detallados
SONAR_VERBOSE=false
```

## 🔧 Cómo Modificar la Configuración

### 1. Cambiar Servidor SonarQube
```bash
# Para servidor local
SONAR_HOST_URL=http://localhost:9000

# Para servidor remoto
SONAR_HOST_URL=http://tu-servidor:9000
```

### 2. Generar Nuevo Token
1. Ir a SonarQube → **My Account** → **Security**
2. Generar nuevo token
3. Actualizar `SONAR_TOKEN` en `.env`

### 3. Ajustar Exclusiones
```bash
# Añadir más exclusiones
SONAR_EXCLUSIONS=...,**/temp/**,**/*.generated.js

# Excluir tests de cobertura
SONAR_COVERAGE_EXCLUSIONS=**/*test*/**,**/*spec*/**,**/cypress/**
```

### 4. Configurar Análisis de Java
```bash
# Habilitar análisis de bytecode Java
SONAR_JAVA_BINARIES=../../../build/classes,../../../target/classes
```

### 5. Configurar Cobertura JavaScript/TypeScript
```bash
# Reportes de cobertura (Jest, Karma, etc.)
SONAR_JAVASCRIPT_LCOV_REPORT_PATHS=../../../coverage/lcov.info,../../../coverage/karma/lcov.info
```

### 6. Optimizar Rendimiento
```bash
# Aumentar memoria para proyectos grandes
SONAR_SCANNER_JAVA_OPTS=-Xmx4096m -XX:MaxMetaspaceSize=512m

# Activar logs detallados para debugging
SONAR_VERBOSE=true
SONAR_LOG_LEVEL=DEBUG
```

## 🐳 Docker Compose - SonarQube Server Local

El `docker-compose.yml` incluido permite ejecutar SonarQube Server localmente:

### Características:
- **Imagen:** `sonarqube:lts-community` (versión gratuita)
- **Puerto:** `9000`
- **Persistencia:** Volúmenes para datos, extensiones y logs
- **Health Check:** Verificación automática de estado
- **Reinicio:** Automático salvo parada manual

### Comandos Útiles:
```bash
# Iniciar SonarQube
docker-compose up -d

# Ver logs
docker-compose logs -f sonarqube

# Parar SonarQube
docker-compose down

# Limpiar datos (CUIDADO: elimina proyectos)
docker-compose down -v
```

### Configuración Inicial:
1. Acceder a `http://localhost:9000`
2. Login inicial: `admin/admin`
3. Cambiar contraseña
4. Crear proyecto manual o usar token existente

## 🔍 Scripts de Ejecución

### sonar-linux.sh
- Valida archivos necesarios
- Carga variables desde `.env`
- Configura `sonar-scanner.properties`
- Ejecuta análisis
- Limpia archivos temporales

### sonar-win.sh  
- Funcionalidad idéntica para Windows
- Sintaxis batch compatible
- Pausa al final para ver resultados

### Características Comunes:
- ✅ Validación de prerrequisitos
- ✅ Configuración automática
- ✅ Manejo de errores
- ✅ Feedback visual
- ✅ Limpieza automática

## 🚨 Troubleshooting

### Error de Memoria
```bash
# En .env, aumentar memoria
SONAR_SCANNER_JAVA_OPTS=-Xmx4096m
```

### Error de Conexión
```bash
# Verificar URL y puerto
curl http://34.95.154.160:9000/api/system/status
```

### Token Inválido
```bash
# Generar nuevo token en SonarQube
# Actualizar SONAR_TOKEN en .env
```

### Archivos No Encontrados
```bash
# Verificar ruta de fuentes
SONAR_SOURCES=../../../src
```

## 📊 Resultados

Después de ejecutar el análisis, los resultados estarán disponibles en:
- **URL:** Definida en `SONAR_HOST_URL`
- **Proyecto:** `SONAR_PROJECT_KEY`

### Métricas Incluidas:
- 🐛 Bugs y vulnerabilidades
- 🎯 Code smells
- 📈 Cobertura de código
- 🔄 Duplicación de código
- 📏 Métricas de complejidad
- 🔒 Hotspots de seguridad

---