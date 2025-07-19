import json
from llama_cpp import Llama
from ollama import Message
from sympy import comp
from src.prompt_library import system_prompt, prompt
from src.models import ConversationClassificationCompletion, ConversationClassification, ConversationContext
import dataclasses
from tqdm import tqdm
from bertopic import BERTopic

class EnhancedJSONEncoder(json.JSONEncoder):
        def default(self, o):
            if dataclasses.is_dataclass(o):
                return dataclasses.asdict(o)
            return super().default(o)

def llm_classification(messages: list[Message]) -> None:
    llm = Llama(
        model_path="./models/Qwen3-4B.Q3_K_M.gguf",
        n_gpu_layers=-1, # Uncomment to use GPU acceleration
        n_ctx=4096, # Uncomment to increase the context window
    )

    output_schema = ConversationClassificationCompletion.model_json_schema()

    classifications: list[ConversationClassification] = []

    for idx, message in tqdm(enumerate(messages[-1000:])):
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
            # filter for entries that actually have content
            completion_validated.pointsOfInterest = list(filter(lambda x: x.short_summary != "NONE", completion_validated.pointsOfInterest))
            if len(completion_validated.pointsOfInterest) == 0:
                continue
            context = ConversationContext(message, [], [])
            classification = ConversationClassification(context, completion_validated)
            classifications.append(classification)
        except:
            print("failed classification!")
            continue
    
    with open("./data/classifications_llm_pipeline.json", "w") as f:
        json.dump({"classifications": classifications}, f, cls=EnhancedJSONEncoder, ensure_ascii=False)

def main():
    
    with open("./data/preprocessed_messages.json", "r") as f:
        messages = json.load(f)

    llm_classification(messages)
    # all_messages = [m["text"] for m in messages]

    # topic_model = BERTopic()
    # topics, probs = topic_model.fit_transform(all_messages)
    # print(topic_model.get_topic_info())
    
    # with open("./data/classifications.json", "w") as f:
    #     json.dump({"classifications": classifications}, f, cls=EnhancedJSONEncoder, ensure_ascii=False)


if __name__ == "__main__":
    main()
