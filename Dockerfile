FROM python:3.12.6-slim

RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /goobe_api

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY package.json ./
COPY package-lock.json ./
RUN npm install --production

COPY . .

EXPOSE 3000

CMD ["gunicorn", "-b", "0.0.0.0:3000", "app:app"]
