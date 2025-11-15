# 构建阶段
FROM node:18-alpine AS build

WORKDIR /app
COPY package*.json ./
RUN npm ci --silent
COPY . .
RUN npm run build

# 复制前端构建产物
COPY --from=build /app/dist /usr/share/nginx/web

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]