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

.PHONY: docker-image
docker-image:
	@for module in $(MODULES) ; do \
  		echo "[docker-image] start to build $(PROJECT_NAME)-$$module."; \
  		cd $(ROOT_DIR)/$$module/; \
  		docker build -t $(PROJECT_NAME)-$$module:$(IMAGE_VERSION) .; \
  	done

	@echo "当前服务配置如下：";
	@cat $(ROOT_DIR)/variables.env;
	@echo "📣 为确保程序正常运行，请检查：";
	@echo "1️⃣ 请按指引（https://github.com/hanshuaikang/AI-Media2Doc/blob/main/backend/README.md）了解如何获取上述配置项。";
	@echo "2️⃣ 在项目根目录的 variables.env 文件中填写相应的配置项。";
	@echo "3️⃣ 运行 make run 启动项目。";

.PHONY: run
run:
	docker compose up -d

	@echo "🚀 项目已启动，访问地址：http://127.0.0.1:5173/";
	@echo "💤 停止运行：make stop";

.PHONY: stop
stop:
	docker compose down

	@echo "👋";
