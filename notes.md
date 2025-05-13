
1. Distance can be computed on a variable by variable basis with a different prompt for each

gemma3 doesn't support embedding
qwen3:14b has a 128k context window

Hyperparametros: Max tokens x RAG Pages x Modelo

Usar num_ctx maior q o do modelo gera lixo : ex ">4"

Investigar influência da temperatura no resultado
Investigar usar docling -> possivelmente extração melhor de tabelas
Investigar langchain para RAG -> automatizar a quantidade de páginas usadas