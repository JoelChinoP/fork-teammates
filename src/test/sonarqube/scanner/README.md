# SonarScanner CLI

## 📋 Descripción

Este directorio contiene la instalación de SonarScanner CLI descargada y descomprimida desde la página oficial de SonarQube. Este scanner se utiliza para analizar el código fuente y enviar los resultados al servidor SonarQube.

## 📁 Estructura Requerida

Para que el scanner funcione correctamente, esta carpeta debe contener las siguientes subcarpetas:

```
scanner/
├── bin/                        # Ejecutables del scanner
│   ├── sonar-scanner          # Script para Linux/macOS  
│   ├── sonar-scanner.bat      # Script para Windows
│   └── sonar-scanner-debug    # Script de debug
├── conf/                       # Archivos de configuración
│   └── sonar-scanner.properties  # Configuración principal (MODIFICADO AUTOMÁTICAMENTE)
├── jre/                        # Java Runtime Environment incluido
│   └── [archivos JRE]         # Runtime Java embebido
└── lib/                        # Librerías del scanner
    └── [archivos .jar]        # Dependencias y librerías
```

## ⚙️ Archivo de Configuración Principal

### conf/sonar-scanner.properties

Este archivo es **modificado automáticamente** por los scripts de ejecución (`sonar-linux.sh` y `sonar-win.sh`) ubicados en el directorio padre.

#### Contenido Típico:
```properties
# Configuración generada automáticamente - 2025-07-09 17:02:43
sonar.host.url=http://34.95.154.160:9000
sonar.log.level=INFO
```

#### Variables Configuradas Automáticamente:
- `sonar.host.url`: URL del servidor SonarQube (desde `SONAR_HOST_URL`)
- `sonar.log.level`: Nivel de logging (desde `SONAR_LOG_LEVEL`)

> ⚠️ **Importante:** No editar manualmente este archivo, ya que será sobrescrito en cada ejecución.

## 🔧 Verificación de Instalación

### Estructura de Carpetas
Verificar que existan todas las carpetas requeridas:
```bash
# Linux/macOS
ls -la scanner/
# Debe mostrar: bin/ conf/ jre/ lib/

# Windows
dir scanner\
# Debe mostrar: bin\ conf\ jre\ lib\
```

### Ejecutables
Verificar que los ejecutables tengan permisos correctos:
```bash
# Linux/macOS - hacer ejecutable si es necesario
chmod +x scanner/bin/sonar-scanner
chmod +x scanner/bin/sonar-scanner-debug

# Verificar funcionamiento
scanner/bin/sonar-scanner -h
```

```cmd
REM Windows - verificar funcionamiento
scanner\bin\sonar-scanner.bat -h
```

### Salida Esperada
```
usage: sonar-scanner [options]

Options:
-D,--define <arg>     Define property
-h,--help             Display help information  
-v,--version          Display version information
-X,--debug            Produce execution debug output
```

## 📋 Requisitos del Sistema

### Java Runtime
- **Incluido:** JRE embebido en la carpeta `jre/`
- **Versión:** Java 17 o superior
- **Memoria recomendada:** Mínimo 2GB RAM disponible

### Espacio en Disco
- **Scanner:** ~200MB
- **Cache temporal:** ~100MB durante análisis
- **Logs:** Variable según proyecto

### Conectividad
- Acceso HTTP/HTTPS al servidor SonarQube
- Puerto por defecto: 9000
- Verificar firewall y proxy si aplica

## 🔍 Archivos Importantes

### bin/sonar-scanner
Ejecutable principal para Linux/macOS
```bash
# Uso directo (no recomendado, usar scripts automatizados)
./scanner/bin/sonar-scanner -Dsonar.token=TOKEN
```

### bin/sonar-scanner.bat  
Ejecutable principal para Windows
```cmd
REM Uso directo (no recomendado, usar scripts automatizados)
scanner\bin\sonar-scanner.bat -Dsonar.token=TOKEN
```

### conf/sonar-scanner.properties
Configuración global que se aplica a todos los análisis. Modificado automáticamente por los scripts.

## 🚨 Troubleshooting

### Scanner No Encontrado
```
Error: sonar-scanner command not found
```
**Solución:** Verificar que existe `scanner/bin/sonar-scanner` y tiene permisos de ejecución.

### Permisos en Linux/macOS
```bash
# Dar permisos de ejecución
chmod +x scanner/bin/*
```

### Error de Java
```
Error: Java not found
```
**Solución:** El JRE debería estar incluido en `scanner/jre/`. Si falta, descargar nuevamente el scanner.

### Memoria Insuficiente
```
java.lang.OutOfMemoryError
```
**Solución:** Configurar `SONAR_SCANNER_JAVA_OPTS` en el archivo `.env`:
```bash
SONAR_SCANNER_JAVA_OPTS=-Xmx4096m
```

### Configuración Corrupta
Si `conf/sonar-scanner.properties` está corrupto:
1. Eliminar el archivo
2. Ejecutar script automatizado para regenerarlo

## 📥 Reinstalación

Si necesitas reinstalar el scanner:

1. **Eliminar carpeta actual:**
   ```bash
   rm -rf scanner/  # Linux/macOS
   rmdir /s scanner\  # Windows
   ```

2. **Descargar nueva versión:**
   - Ir a [https://docs.sonarqube.org/latest/analysis/scan/sonarscanner/](https://docs.sonarqube.org/latest/analysis/scan/sonarscanner/)
   - Descargar la versión apropiada para tu OS
   - Descomprimir en esta ubicación como `scanner/`

3. **Verificar instalación:**
   ```bash
   ./scanner/bin/sonar-scanner -v
   ```

---
**Nota:** Este directorio contiene solo el SonarScanner CLI. La configuración y ejecución se maneja desde el directorio padre mediante los scripts automatizados.
