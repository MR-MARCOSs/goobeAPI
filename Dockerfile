FROM python:3.12.6-slim

RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    git \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /goobe_api

COPY requirements.txt ./ 
RUN pip install --no-cache-dir -r requirements.txt

COPY package.json ./ 
COPY package-lock.json ./  # Certifique-se de que o package-lock.json está presente no seu repositório
RUN npm install

COPY . .

EXPOSE 3000

CMD ["gunicorn", "-b", "0.0.0.0:3000", "app:app"]
