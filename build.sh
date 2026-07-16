#!/usr/bin/env bash
set -e

# Build all YAML-based chapters (index.html + slides.html)
python3 build.py

# Convert learning_to_count markdown to HTML
FOOTER="templates/footer-pandoc.html"
TEMPLATE="templates/pandoc-chapter.html"

if [ -f learning_to_count/learning_to_count.md ]; then
  pandoc learning_to_count/learning_to_count.md \
    -o learning_to_count/learning_to_count.html \
    --template="$TEMPLATE" --metadata title="Learning to Count" \
    -H templates/blocks/ga.html \
    --include-after-body="$FOOTER"
else
  echo "WARNING: learning_to_count/learning_to_count.md not found — keeping existing HTML."
fi

# Convert markdown-only chapters to HTML
pandoc rag_and_agents/rag_and_agents.md \
  -o rag_and_agents/rag_and_agents.html \
  --template="$TEMPLATE" --metadata title="RAG & Agentic AI" \
  -H templates/blocks/ga.html \
  --include-after-body="$FOOTER"
pandoc rag_and_agents/provider_setup.md \
  -o rag_and_agents/provider_setup.html \
  --template="$TEMPLATE" --metadata title="Provider Setup" \
  -H templates/blocks/ga.html \
  --include-after-body="$FOOTER"
pandoc projects/projects.md \
  -o projects/projects.html \
  --template="$TEMPLATE" --metadata title="Capstone Projects" \
  -H templates/blocks/ga.html \
  --include-after-body="$FOOTER"
pandoc practice_problems/practice_problems.md \
  -o practice_problems/practice_problems.html \
  --template="$TEMPLATE" --metadata title="Practice Problems" \
  -H templates/blocks/ga.html \
  --include-after-body="$FOOTER"

echo "Build complete. Open index.html to preview."
