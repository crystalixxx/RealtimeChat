# Dockerfile.dev
FROM node:20-alpine3.20

WORKDIR /app

# Установка зависимостей
COPY package*.json ./
RUN npm install

# Копируем исходный код
COPY . .

# Открываем порты для разработки
EXPOSE 5173 35729

# Запускаем Vite в режиме разработки
CMD ["npm", "run", "dev"]
