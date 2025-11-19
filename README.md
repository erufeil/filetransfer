# FileTransfer
endpoint para hacer un CURL POST

# Docker Build
docker build -t file-receiver .

# Docker compose
docker run -d -p 5000:5000 -v /ruta/real/uploads:/uploads file-receiver


# Curl para windows
curl -F "file=@C:\ruta\al\archivo.txt" https://subdominio.dominio.com/upload

# Comprimir
Compress-Archive -Path C:\ruta\carpeta\* -DestinationPath C:\ruta\carpeta.zip

# Subir con curl.exe (usar curl.exe para evitar el alias de PowerShell)
curl.exe -F "file=@C:\ruta\carpeta.zip" https://subdominio.dominio.com/upload

# CMD:
for %f in ("C:\ruta\carpeta\*") do curl -F "file=@%~ff" https://subdominio.dominio.com/upload