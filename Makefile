# Re-execute the tutorial notebooks in order, saving outputs in place.
# Run inside the floodnet_env conda environment.
#   make notebooks  re-run 01-07 on the data already in data/
#   make refresh    download new data (notebook 00), then re-run 01-07

NOTEBOOKS := $(sort $(wildcard [0-9][0-9]-*.ipynb))
ANALYSIS  := $(filter-out 00-%,$(NOTEBOOKS))
JUPYTER   ?= jupyter
EXECUTE    = $(JUPYTER) nbconvert --to notebook --execute --inplace

.PHONY: notebooks refresh

# nbconvert leaves a notebook unchanged if any cell fails; stop there.
notebooks:
	@test -n "$(ANALYSIS)" || { echo "No notebooks found."; exit 1; }
	@for nb in $(ANALYSIS); do \
		echo "== $$nb"; \
		$(EXECUTE) "$$nb" || exit 1; \
	done

# Start from a clean data/ so a failed download can be undone with git.
refresh:
	@test -z "$$(git status --porcelain -- data/)" || { \
		echo "data/ has uncommitted changes. Commit or restore them before refreshing."; \
		exit 1; }
	@echo "== 00-download-data.ipynb"
	@$(EXECUTE) 00-download-data.ipynb || { \
		echo "Download failed; data/ may be partly updated. Undo with:"; \
		echo "  git restore data/ && git clean -fd data/"; \
		exit 1; }
	@$(MAKE) --no-print-directory notebooks
