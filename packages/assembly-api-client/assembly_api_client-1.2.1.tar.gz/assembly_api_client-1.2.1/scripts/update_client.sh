#!/bin/bash
set -e

# 1. Sync Specs (Fetch Master List & Download new specs)
# We use --force to ensure we get the latest master list
echo "Step 1: Synchronizing API Specs..."
# Note: Requires ASSEMBLY_API_KEY to be set
python -m assembly_client.cli sync --force

# 2. Generate Code (Enums & Models)
echo "Step 2: Regenerating Client Code..."
python run_codegen.py

# 3. Generate/Update Fixtures (for new APIs)
echo "Step 3: Checking for new fixtures..."
python scripts/generate_fixtures.py

# 4. Verify with Tests
echo "Step 4: Running Tests..."
pytest tests/test_all_services.py

echo "Update Complete! Please review changes and commit."
