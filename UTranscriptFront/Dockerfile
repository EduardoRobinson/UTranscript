FROM node:18-alpine

WORKDIR /app

# Copia apenas os arquivos de dependências primeiro (otimiza cache)
COPY package*.json ./
RUN npm install

# Copia o restante do código
COPY . .

# Expõe as portas do Angular e do Ionic
EXPOSE 4200
EXPOSE 8100

# Comando para rodar com Hot Reload no Docker
CMD ["npm", "start", "--", "--host", "0.0.0.0", "--poll", "2000"]