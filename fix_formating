.PHONY check
check:
	black --check ./ && flake8 ./ && isort --check-only ./

.PHONY fix
fix:
	black ./ && flake8 ./ && isort ./