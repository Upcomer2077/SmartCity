# Переменные
AL = uv run alembic
m = "migration_message"

.PHONY: gen-mig up downgrade help
.DEFAULT_GOAL := help


help:
	@echo. & \
	echo Available commands: & \
	echo --------------------------------------------------------------------------- & \
	echo make gen-mig  			- Generate new migration (params: m="msg", id="id") & \
	echo make up                - Apply all migrations (upgrade head) & \
	echo make downgrade         - Rollback last migration (downgrade -1) & \
	echo make help              - Show this help message & \
	echo --------------------------------------------------------------------------- & \
	echo.



gen-mig:
	$(AL) revision -m $(m) --autogenerate --rev-id $(id)

up:
	$(AL) upgrade head

downgrade:
	$(AL) downgrade -1
