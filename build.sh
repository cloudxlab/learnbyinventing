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
jupyter nbconvert --to html encoder_decoder/encoder_decoder.ipynb
jupyter nbconvert --to html gradient_descent/linear_regression_gradient_descent.ipynb
jupyter nbconvert --to html decision_tree/decision_tree.ipynb
jupyter nbconvert --to html convolutions/convolutions.ipynb
jupyter nbconvert --to html information_theory/information_theory.ipynb

# Convert learning_to_count markdown to HTML
pandoc learning_to_count/learning_to_count.md \
  -o learning_to_count/learning_to_count.html \
  --standalone --metadata title="Learning to Count"

echo "Build complete. Open index.html to preview."
