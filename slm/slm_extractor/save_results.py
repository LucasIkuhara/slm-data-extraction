from pathlib import Path
from datetime import datetime


def save_result(case_study: str, model: str, rag_prompt: str, extraction_prompt: str, result: str):
    """
    Saves the relevant information about a case study run.
    
    Args:
        case_study: The name of the case study used.
        model: The language model used.
        rag_prompt: The RAG prompt used to fetch context.
        extraction_prompt: The prompt used to generate the final response.
    """
    today = datetime.now()
    model_name = model.replace(":", "-")
    dir_name = f"results/{today.strftime('%Y-%m-%d')}/{case_study}/{model_name}/"
    
    print(f"Saving results to: {dir_name}")
    Path(dir_name).mkdir(parents=True, exist_ok=True)

    with open(dir_name + "rag_prompt.txt", "w") as f:
        f.write(rag_prompt)

    with open(dir_name + "extraction_prompt.txt", "w") as f:
        f.write(extraction_prompt)

    with open(dir_name + "result.txt", "w") as f:
        f.write(result)
