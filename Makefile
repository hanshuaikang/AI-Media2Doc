IMAGE_VERSION ?= latest

PROJECT_NAME := ai-media2doc
MODULES := backend frontend
ROOT_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

.PHONY: help
help:
	@echo "Make Targets: "
	@echo " docker-image: Build image"
	@echo " run: Run project"
	@echo " stop: Stop project"

.PHONY: run
run:
	docker compose up -d

	@echo "🚀 项目已启动，访问地址：http://127.0.0.1:5173/";
	@echo "💤 停止运行：make stop";

.PHONY: stop
stop:
	docker compose down

	@echo "👋";
