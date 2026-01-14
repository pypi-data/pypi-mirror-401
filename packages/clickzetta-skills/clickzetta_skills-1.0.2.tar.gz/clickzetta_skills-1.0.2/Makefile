.PHONY: help build install install-dev clean test uninstall list-skills

help:
	@echo "Clickzetta Skills - Makefile"
	@echo ""
	@echo "Available targets:"
	@echo "  make build        - Build the distribution package"
	@echo "  make install      - Install the package locally"
	@echo "  make install-dev  - Install in development mode (editable)"
	@echo "  make clean        - Remove build artifacts"
	@echo "  make test         - Run tests"
	@echo "  make uninstall    - Uninstall the package"
	@echo "  make list-skills  - List all available skills"
	@echo ""
	@echo "Quick start:"
	@echo "  1. make install      # Install the package"
	@echo "  2. cz-analyze-job plan.json job_profile.json output_dir"
	@echo ""
	@echo "Available skills:"
	@echo "  - Job Performance Analyzer: cz-analyze-job"

build: clean
	@echo "Building clickzetta-skills package..."
	python3 -m build
	@echo "✅ Build complete! Package files in dist/"

install: build
	@echo "Installing clickzetta-skills..."
	pip3 install dist/*.whl --force-reinstall
	@echo "✅ Installation complete!"
	@echo ""
	@echo "Available commands:"
	@echo "  cz-analyze-job <plan.json> <job_profile.json> [output_dir]"

install-dev:
	@echo "Installing in development mode..."
	pip3 install -e .
	@echo "✅ Development installation complete!"
	@echo ""
	@echo "Changes to code will take effect immediately without reinstalling."

clean:
	@echo "Cleaning build artifacts..."
	rm -rf build/ dist/ *.egg-info cz_skills.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	@echo "✅ Clean complete!"

uninstall:
	@echo "Uninstalling clickzetta-skills..."
	pip3 uninstall -y clickzetta-skills
	@echo "✅ Uninstall complete!"

# Development helpers
dev-check:
	@echo "Checking installation..."
	@echo ""
	@pip3 show clickzetta-skills || echo "❌ Package not installed"
	@echo ""
	@echo "Checking available commands:"
	@which cz-analyze-job && echo "✅ cz-analyze-job found" || echo "❌ cz-analyze-job not found"

list-skills:
	@echo "Available skills in clickzetta-skills:"
	@echo ""
	@echo "1. Job Performance Analyzer"
	@echo "   Command: cz-analyze-job"
	@echo "   Description: 分析 plan.json 和 job_profile.json，识别性能瓶颈"
	@echo ""
	@echo "To add more skills, see scripts/README.md"

rebuild: clean build
	@echo "✅ Rebuild complete!"

upload:
	@echo "Uploading package to PyPI..."
	@echo "Package: clickzetta-skills"
	twine upload dist/*
	@echo "✅ Upload complete!"