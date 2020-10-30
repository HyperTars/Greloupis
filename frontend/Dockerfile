FROM node:latest as build
RUN mkdir -p /usr/src/app
COPY . /usr/src/app
WORKDIR /usr/src/app
RUN npm install
RUN npm run build
CMD ["npm", "start"]

#FROM nginx:alpine
#COPY --from=build /usr/src/app/build /usr/share/nginx/html
#COPY nginx.conf /etc/nginx/nginx.conf
#EXPOSE 80
#CMD ["nginx", "-g", "daemon off;"]
