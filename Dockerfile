FROM node:18-alpine

WORKDIR /usr/src/app

ENV NODE_ENV=production

# Copy package files first to leverage Docker cache
COPY package*.json ./

RUN npm ci --only=production

# Copy app sources
COPY . .

EXPOSE 3000

USER node

CMD ["npm", "start"]
