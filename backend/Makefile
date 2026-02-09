# Переменные
AL = uv run alembic
m = "migration_message"

.PHONY: gen-mig up downgrade

gen-mig:
	$(AL) revision -m $(m) --autogenerate --rev-id $(id)

up:
	$(AL) upgrade head

downgrade:
	$(AL) downgrade -1

	