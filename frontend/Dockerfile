ARG NODE_VERSION=22

FROM node:${NODE_VERSION}-slim

ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PATH="/app/node_modules/.bin:$PATH"

RUN set -ex && \
    sed -i 's/deb.debian.org/mirrors.cloud.tencent.com/g' /etc/apt/sources.list.d/debian.sources && \
    apt update && \
    apt install -y --no-install-recommends \
    git \
    ca-certificates

RUN npm config set registry https://mirrors.cloud.tencent.com/npm/

WORKDIR /app

COPY package.json ./

RUN npm install

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
