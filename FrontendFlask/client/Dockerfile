# build step / Quelle: https://medium.com/@johnidouglasmarangon/how-to-dockerize-a-frontend-app-using-react-js-1d193b4d151b
FROM node:16.13.2-alpine as build

WORKDIR /app

COPY package.json ./

RUN npm install

COPY .. ./

RUN npm run build

# release step
FROM nginx:1.21.5-alpine as release

COPY --from=build /app/build /usr/share/nginx/html/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]