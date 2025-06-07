ARG PYTHON_VERSION=3.11

FROM python:${PYTHON_VERSION}-slim AS base

ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PATH="/.venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN set -ex && \
    sed -i 's/deb.debian.org/mirrors.cloud.tencent.com/g' /etc/apt/sources.list.d/debian.sources && \
    apt update

# ------------------- Stage 1: Build Stage ------------------------------
FROM base AS builder

WORKDIR /

COPY requirements.txt .

RUN set -ex && \
    mkdir ~/.pip && \
    echo "[global]" >> ~/.pip/pip.conf && \
    echo "index-url=https://mirrors.tencent.com/pypi/simple/" >> ~/.pip/pip.conf

RUN set -ex && \
    python -m venv .venv && \
    pip install --upgrade pip && \
    pip install -r ./requirements.txt

# ------------------- Stage 2: Final Stage ------------------------------
FROM base

WORKDIR /app

COPY --from=builder /.venv /.venv
ADD ./ ./

ENV MODEL_ID="xxx" \
    ARK_API_KEY="xxx" \
    TOS_ACCESS_KEY="xxx" \
    TOS_SECRET_KEY="xxx" \
    TOS_ENDPOINT="xxx" \
    TOS_REGION="xxx" \
    TOS_BUCKET="xxx" \
    AUC_APP_ID="xxx" \
    AUC_ACCESS_TOKEN="xxx" \
    AUC_CLUSTER_ID="xxx"

EXPOSE 8080

CMD ["python", "/app/main.py"]
