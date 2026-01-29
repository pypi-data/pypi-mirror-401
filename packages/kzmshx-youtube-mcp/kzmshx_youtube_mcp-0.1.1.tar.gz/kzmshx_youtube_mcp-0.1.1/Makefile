.PHONY: help
help: ## Show help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: lint
lint: ## Run linter
	uv run ruff check src tests
	uv run ruff format --check src tests

.PHONY: fix
fix: ## Auto-fix lint issues
	uv run ruff check --fix src tests
	uv run ruff format src tests

.PHONY: test
test: ## Run all tests
	uv run pytest -v

.PHONY: typecheck
typecheck: ## Run type checker
	uv run mypy src

.PHONY: dev
dev: ## Launch MCP Inspector for interactive debugging
	npx @modelcontextprotocol/inspector uv run kzmshx-youtube-mcp
