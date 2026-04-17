FROM node:20-alpine

WORKDIR /app

COPY app/package.json .
RUN npm install --production

COPY app/ .

ARG APP_VERSION=1.0.0
ARG BUILD_ID=local
ARG DEPLOY_TIME=unknown

ENV APP_VERSION=$APP_VERSION
ENV BUILD_ID=$BUILD_ID
ENV DEPLOY_TIME=$DEPLOY_TIME
ENV NODE_ENV=production
ENV AWS_REGION=ap-south-1

EXPOSE 3000

CMD ["node", "server.js"]