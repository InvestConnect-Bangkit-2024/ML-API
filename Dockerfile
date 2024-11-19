FROM node:18.16.1

WORKDIR /ml-api

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 80

CMD ["node", "server.js"]