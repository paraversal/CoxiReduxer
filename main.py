import json
from llama_cpp import Llama
from src.prompt_library import system_prompt, prompt
from src.models import ConversationClassificationCompletion, ConversationClassification, ConversationContext
import dataclasses
from tqdm import tqdm

class EnhancedJSONEncoder(json.JSONEncoder):
        def default(self, o):
            if dataclasses.is_dataclass(o):
                return dataclasses.asdict(o)
            return super().default(o)

def main():
    llm = Llama(
        model_path="./models/Qwen3-4B.Q3_K_M.gguf",
        n_gpu_layers=-1, # Uncomment to use GPU acceleration
        n_ctx=4096, # Uncomment to increase the context window
    )
    output_schema = ConversationClassificationCompletion.model_json_schema()

    with open("./data/preprocessed_messages.json", "r") as f:
        messages = json.load(f)

    classifications: list[ConversationClassification] = []

    # main loop
    for idx, message in tqdm(enumerate(messages[:50])):
        try:
            output = llm.create_chat_completion(
            messages = [
                {"role": "system", "content": f'{system_prompt}\n{prompt(message, [], [])}'},
                {
                    "role": "user",
                    "content": "Summarise the 'focus message' please."
                }
            ],
            response_format={
                "type": "json_object",
                "schema": output_schema
            }
            )
            completion = output["choices"][0]["message"]["content"]
            
            completion_validated = ConversationClassificationCompletion.model_validate_json(completion)
            context = ConversationContext(message, [], [])
            classification = ConversationClassification(context, completion_validated)
            classifications.append(classification)
        except:
            print("failed classification!")
            continue
    
    with open("./data/classifications.json", "w") as f:
        json.dump({"classifications": classifications}, f, cls=EnhancedJSONEncoder, ensure_ascii=False)


if __name__ == "__main__":
    main()
