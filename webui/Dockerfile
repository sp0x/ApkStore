FROM node:12.2.0-alpine as NODE
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
COPY package.json ./package.json
COPY package-lock.json ./package-log.json

RUN yarn
COPY ./package.json .
RUN yarn install
COPY ./ /app
#COPY ./scripts /app/
RUN yarn build


FROM nginx:alpine
COPY --from=NODE /app/build /usr/share/nginx/html
EXPOSE 80


