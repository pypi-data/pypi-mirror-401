
if __name__ == "__main__":
    from Pythia import Pythia
    from pythia.llm import ollama_backend
    from pythia.core.split import split_csv_folder
    backend = ollama_backend(
        model="llama3.1:8b",
        base_url="http://localhost:11434",
        temperature=0.1,
        max_tokens=2048
    )
    x, y = split_csv_folder("dummy_data/", 0.6)
    Pythia(
        LLMbackend=backend,
        dev_data_path=x,
        val_data_path=y,
        output_dir="output_dir",
        SOP="Look for if the patient having chest pains, shortness of breath, etc",
        initial_prompt="Is the patient showing signs of a cardiology concern?"
    )