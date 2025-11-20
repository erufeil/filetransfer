# FileTransfer
aplicacion completa para tener un endpoint para hacer un CURL POST y una pagina web que me permita descargarlo facilmente desde cualquier navegador y que permita borrar el archivo con un solo boton.

arquitectura:
lenguaje: python
programacion: muy simple
landing page: index.html
Sistema operativo: ubuntu server 22.04.5 LTS
Contenedores: Docker


descripcion:
- el python sirve el endpoint y el index.html en el mismo contenedor
- todo lo que necesite el html sera simple sin librerias extra ni servicio de node.js
- usare una carpeta en servidor creada con git pull
- construire la imagen en servidor con docker build
- creare el contenedor con el docker compose

# Instalación en Servidor Ubuntu

## 1. Clonar el repositorio
```bash
git clone <tu-repositorio>
cd filetransfer
```

## 2. Crear el directorio para volumen persistente
```bash
sudo mkdir -p /mnt/hdd-erf/config/file-transfer
sudo chmod 777 /mnt/hdd-erf/config/file-transfer
```

## 3. Construir la imagen Docker
```bash
docker build -t file-receiver:latest .
```

## 4. Crear la red (si no existe)
```bash
docker network create --subnet=172.21.0.0/16 front-net
```

## 5. Iniciar el contenedor
```bash
docker-compose up -d
```

## 6. Verificar que está corriendo
```bash
docker ps
docker logs file-transfer
```

El servidor estará disponible en `http://IP-SERVIDOR:9000`

**NOTA:** Edita `docker-compose.yml` línea 7 para cambiar la IP: `172.21.0.10` por la que necesites.


# Uso

## Interfaz Web
Abre en tu navegador: `http://IP-SERVIDOR:9000`

Desde allí podrás:
- Subir archivos
- Descargar archivos
- Eliminar archivos

## Subir archivos con cURL

### Windows PowerShell
```powershell
# Archivo único
curl.exe -F "file=@C:\ruta\al\archivo.txt" http://IP-SERVIDOR:9000/upload

# Comprimir carpeta y subir
Compress-Archive -Path C:\ruta\carpeta\* -DestinationPath C:\ruta\carpeta.zip
curl.exe -F "file=@C:\ruta\carpeta.zip" http://IP-SERVIDOR:9000/upload
```

### Windows CMD
```cmd
REM Archivo único
curl -F "file=@C:\ruta\al\archivo.txt" http://IP-SERVIDOR:9000/upload

REM Múltiples archivos
for %f in ("C:\ruta\carpeta\*") do curl -F "file=@%~ff" http://IP-SERVIDOR:9000/upload
```

### Linux / Mac
```bash
# Archivo único
curl -F "file=@/ruta/al/archivo.txt" http://IP-SERVIDOR:9000/upload

# Múltiples archivos
for file in /ruta/carpeta/*; do
  curl -F "file=@$file" http://IP-SERVIDOR:9000/upload
done
```

**NOTA:** Si usas HTTPS con dominio, reemplaza `http://IP-SERVIDOR:9000` por `https://subdominio.dominio.com`