# FileTransfer
endpoint para hacer un CURL POST

# Docker Build
docker build -t file-receiver:latest .

# docker-compose: file-transfer
services:
  file-receiver:
    container_name: file-transfer
    image: file-receiver:latest
    networks: 
      front-net:
        ipv4_address: 172.21.0.
    ports:
      - 9000:5000
    volumes:
      - /mnt/hdd-erf/config/file-transfer:/uploads
    restart: unless-stopped
    environment:
      - ENV=production

networks:
  front-net:
    external: true


# Curl para windows
curl -F "file=@C:\ruta\al\archivo.txt" https://subdominio.dominio.com/upload

# Comprimir
Compress-Archive -Path C:\ruta\carpeta\* -DestinationPath C:\ruta\carpeta.zip

# Subir con curl.exe (usar curl.exe para evitar el alias de PowerShell)
curl.exe -F "file=@C:\ruta\carpeta.zip" https://subdominio.dominio.com/upload

# CMD:
for %f in ("C:\ruta\carpeta\*") do curl -F "file=@%~ff" https://subdominio.dominio.com/upload