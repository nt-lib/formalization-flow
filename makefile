.PHONY: clean test verify copy_remote copy_logs test_remote verify_remote
REMOTE_DIR := /tmp/$(shell basename $(CURDIR))

clean:
	find . -type f -name "*.sig" -delete

test:
	@echo "No tests configured yet - override this target"

verify:
	bash verify_all.sh

copy_remote:
	rsync -avz --delete ./ $(ssh):$(REMOTE_DIR)

copy_logs:
	rsync -avz $(ssh):$(REMOTE_DIR)/logs/ logs/

# Usage: make test_remote ssh="user@hostname"
test_remote: copy_remote
	ssh $(ssh) "cd $(REMOTE_DIR) && make test"

# Usage: make verify_remote ssh="user@hostname"
verify_remote: copy_remote
	ssh $(ssh) "cd $(REMOTE_DIR) && make verify"
