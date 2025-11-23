ARG NODE_VERSION=22

FROM node:${NODE_VERSION}-slim

ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PATH="/app/node_modules/.bin:$PATH"


RUN set -ex && \
    apt-get update -o Acquire::Retries=3 && \
    apt-get install -y --no-install-recommends git ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN npm config set registry https://mirrors.cloud.tencent.com/npm/

WORKDIR /app

COPY package.json ./

RUN npm install

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
