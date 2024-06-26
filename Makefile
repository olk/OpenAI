#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = OpenAI
PYTHON_INTERPRETER = python3

#################################################################################
# COMMANDS                                                                      #
#################################################################################

# Make helper

test-api:
	$(PYTHON_INTERPRETER) src/test_api.py

app:
	$(PYTHON_INTERPRETER) src/app.py

max-tokens:
	$(PYTHON_INTERPRETER) src/max_tokens.py

stop-tokens:
	$(PYTHON_INTERPRETER) src/stop_tokens.py

temperature:
	$(PYTHON_INTERPRETER) src/temperature.py

generated-knowledge-prompt:
	$(PYTHON_INTERPRETER) src/generated_knowledge_prompting.py

context-stuffing:
	$(PYTHON_INTERPRETER) src/context_stuffing.py

dyn-max-tokens:
	$(PYTHON_INTERPRETER) src/dyn_max_tokens.py 3

embedding:
	$(PYTHON_INTERPRETER) src/embedding.py 3

zero-shot-classifier:
	$(PYTHON_INTERPRETER) src/zero_shot_classifier.py

zero-shot-class-acc:
	$(PYTHON_INTERPRETER) src/zero_shot_class_acc.py

## Delete all compiled Python files
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Lint using flake8
lint:
	flake8 src

.PHONY: clean data features lint


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
#
help:
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

.PHONY: help
