#!/usr/bin/env bash
set -e

# Build all YAML-based chapters (index.html + slides.html)
python3 build.py

# Convert learning_to_count markdown to HTML
if [ -f learning_to_count/learning_to_count.md ]; then
  pandoc learning_to_count/learning_to_count.md \
    -o learning_to_count/learning_to_count.html \
    --standalone --metadata title="Learning to Count" \
    -H templates/blocks/ga.html
else
  echo "WARNING: learning_to_count/learning_to_count.md not found — keeping existing HTML."
fi

# Convert markdown-only chapters to HTML
pandoc rag_and_agents/rag_and_agents.md \
  -o rag_and_agents/rag_and_agents.html \
  --standalone --metadata title="RAG & Agentic AI" \
  -H templates/blocks/ga.html
pandoc rag_and_agents/provider_setup.md \
  -o rag_and_agents/provider_setup.html \
  --standalone --metadata title="Provider Setup" \
  -H templates/blocks/ga.html
pandoc projects/projects.md \
  -o projects/projects.html \
  --standalone --metadata title="Capstone Projects" \
  -H templates/blocks/ga.html
pandoc practice_problems/practice_problems.md \
  -o practice_problems/practice_problems.html \
  --standalone --metadata title="Practice Problems" \
  -H templates/blocks/ga.html

echo "Build complete. Open index.html to preview."
