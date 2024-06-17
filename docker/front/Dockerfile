FROM node:18
# WORKDIR /frontend
# COPY package*.json .
# RUN yarn install
COPY /frontend /frontend
# RUN cd /frontend
RUN cd /frontend && yarn install
RUN cd /frontend && yarn build
CMD cd /frontend && npm run preview --host 0.0.0.0

# FROM node:18
# COPY --from=builder /frontend /frontend
# CMD cd /frontend && vite preview
# FROM nginx:latest
# COPY --from=builder /app/dist /usr/share/nginx/html
# COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf
# EXPOSE 80
# CMD ["nginx", "-g", "daemon off;"]