.PHONY: major minor patch sync init clean

# Formatting
BOLD := \033[1m
RESET := \033[0m

#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PROJECT_SLUG = {{ cookiecutter.project_slug }}
VIRTUAL_ENV ?= $(PROJECT_DIR)/.venv
PREREQUISITES = pre-commit bump2version

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Initialize development environment
init: .python-version
	@echo "$(BOLD)Installing prerequisites...$(RESET)"
	@$(shell pyenv which python) -m pip install -q -U $(PREREQUISITES)
	@echo "$(BOLD)Creating virtual environment...$(RESET)"
	@$(shell pyenv which python) -m venv --clear --prompt "$(PROJECT_SLUG)" .venv
	@echo "$(BOLD)Upgrading pip and setuptools...$(RESET)"
	@$(VIRTUAL_ENV)/bin/python -m pip install -U pip setuptools
	@echo "$(BOLD)Installing pip-tools...$(RESET)"
	@$(VIRTUAL_ENV)/bin/python -m pip install -U pip-tools

## Compile base requirements
requirements.txt: export CUSTOM_COMPILE_COMMAND="make $@"
requirements.txt: requirements.in
	@echo "$(BOLD)Compiling requirements...$(RESET)"
	@$(VIRTUAL_ENV)/bin/pip-compile -o $@ $<

## Compile development requirements
dev-requirements.txt: export CUSTOM_COMPILE_COMMAND="make $@"
dev-requirements.txt: dev-requirements.in requirements.txt
	@echo "$(BOLD)Compiling development requirements...$(RESET)"
	@$(VIRTUAL_ENV)/bin/pip-compile -o $@ $<

## Synchronize virtual environment with requirements
sync: dev-requirements.txt requirements.txt
	@echo "$(BOLD)Synchronizing virtual environment...$(RESET)"
	@$(VIRTUAL_ENV)/bin/pip-sync $^

## Bump version
major minor patch:
	@bumpversion $@

## Delete all compiled Python files
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Delete all mypy caches
clean-mypy:
	find . -maxdepth 1 -type d -name ".mypy_cache" -print0 | xargs -0 rm -rf

## Build Sphinx HTML documentation, including API reference
docs:
	@echo "$(BOLD)Generating API reference...$(RESET)"
	@rm -f docs/{{ cookiecutter.project_slug }}.rst
	@rm -f docs/modules.rst
	@$(VIRTUAL_ENV)/bin/sphinx-apidoc -o docs/ -H "API reference" {{ cookiecutter.project_slug }}
	@echo "$(BOLD)Building HTML documentation...$(RESET)"
	@$(MAKE) -C docs clean
	@$(MAKE) -C docs html

#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help
# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: help
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')
