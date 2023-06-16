FROM node:lts

WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH

COPY . /app

RUN npm ci

EXPOSE 4300

CMD npm start