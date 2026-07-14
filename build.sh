#!/usr/bin/env bash
set -e

# Export all notebooks to HTML in-place (next to the .ipynb file)
jupyter nbconvert --to html dictionaries/dictionaries.ipynb
jupyter nbconvert --to html binary_search/binary_search.ipynb
jupyter nbconvert --to html loops_and_array/loops_and_array.ipynb
jupyter nbconvert --to html expressions_and_functions/expressions_and_functions.ipynb
jupyter nbconvert --to html if_else/if_else.ipynb
jupyter nbconvert --to html recursion/recursion.ipynb
jupyter nbconvert --to html sorting/sorting.ipynb
jupyter nbconvert --to html trees_and_heaps/trees_and_heaps.ipynb
jupyter nbconvert --to html pattern_matching/pattern_matching.ipynb
jupyter nbconvert --to html backtracking/backtracking.ipynb
jupyter nbconvert --to html encoder_decoder/encoder_decoder.ipynb
jupyter nbconvert --to html classes_and_objects/classes_and_objects.ipynb
jupyter nbconvert --to html secrets_of_prediction/secrets_of_prediction.ipynb
jupyter nbconvert --to html gradient_descent/linear_regression_gradient_descent.ipynb
jupyter nbconvert --to html decision_tree/decision_tree.ipynb
jupyter nbconvert --to html random_forest/random_forest.ipynb
jupyter nbconvert --to html recommender/recommender.ipynb
jupyter nbconvert --to html neural_networks/neural_networks.ipynb
jupyter nbconvert --to html convolutions/convolutions.ipynb
jupyter nbconvert --to html information_theory/information_theory.ipynb

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

echo "Build complete. Open index.html to preview."
