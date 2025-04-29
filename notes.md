1. Tokenize base text to evaluate needed context window size
2. List different models ranking context window size
3. Try example-based prompt instead of format description

Alternative
1. Tokenize page-by-page
2. Store in vector Db
3. Select N most relevant pages based on relevance
4. Relevance can be evaluated by cosine distance
5. Distance can be computed on a variable by variable basis with a different prompt for each

gemma3 doesn't support embedding
qwen3:14b has a 128k context window

TODO: Add different tables for embedding lengths