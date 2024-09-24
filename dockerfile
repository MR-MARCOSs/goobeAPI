FROM python:3.12.6-slim

# Instalar FFmpeg
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Definir diretório de trabalho
WORKDIR /app

# Copiar arquivos de requisitos e instalá-los
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código
COPY . .

# Comando para iniciar a aplicação
CMD ["gunicorn", "goobe_api:app"]
