#!/usr/bin/env bash
set -e

# All notebook chapters are now standalone HTML files (<chapter>/index.html)
# with shared assets (assets/lbi.css, assets/lbi.js).
# No jupyter nbconvert needed for these chapters.

# Convert learning_to_count markdown to HTML
# (the .md source is not in the repo — only the exported .html is committed —
#  so skip with a warning instead of failing the whole build)
if [ -f learning_to_count/learning_to_count.md ]; then
  pandoc learning_to_count/learning_to_count.md \
    -o learning_to_count/learning_to_count.html \
    --standalone --metadata title="Learning to Count"
else
  echo "WARNING: learning_to_count/learning_to_count.md not found — keeping existing HTML."
fi

# Convert RAG & Agentic AI markdown chapter to HTML
pandoc rag_and_agents/rag_and_agents.md \
  -o rag_and_agents/rag_and_agents.html \
  --standalone --metadata title="RAG & Agentic AI"
pandoc rag_and_agents/provider_setup.md \
  -o rag_and_agents/provider_setup.html \
  --standalone --metadata title="Provider Setup"

# Convert Capstone Projects markdown chapter to HTML
pandoc projects/projects.md \
  -o projects/projects.html \
  --standalone --metadata title="Capstone Projects"

# Convert Practice Problems index to HTML
pandoc practice_problems/practice_problems.md \
  -o practice_problems/practice_problems.html \
  --standalone --metadata title="Practice Problems"

echo "Build complete. Open index.html to preview."
