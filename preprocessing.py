import argparse
import json
from typing import Any
from src.models import Message
import dataclasses


class EnhancedJSONEncoder(json.JSONEncoder):
        def default(self, o):
            if dataclasses.is_dataclass(o):
                return dataclasses.asdict(o)
            return super().default(o)

def parse_message(message_json: dict[str, Any]) -> None | Message:
    try:
        # extract and reassemble origin text
        text_entities: list[dict[str, str]] = message_json["text_entities"]
        parsed_message_text = "".join([entity["text"] for entity in text_entities])

        reactions = message_json.get("reactions", None)
        reactions_count = 0 if not reactions else sum([reaction["count"] for reaction in reactions])

        message = Message(message_json["from"], message_json["date"], parsed_message_text, reactions_count)
        return message
    except KeyError as e:
        print(f"Unable to parse message: {message_json}. ({e})")
        return None

def main():
    parser = argparse.ArgumentParser()  
    parser.add_argument("--input")
    args = parser.parse_args()
    if not args.input:
        raise Exception("Must pass input file")
    
    # load json file
    with open(args.input, "r") as f:
        input_contents: dict[str, Any] = json.load(f)["messages"]
    
    non_empty_messages = list(filter(lambda x: x["text"] != "", input_contents))

    stripped_messages: list[Message] = []

    for message in non_empty_messages:
        parsed_message: Message | None = parse_message(message)
        if not parsed_message:
            continue
        stripped_messages.append(parsed_message)
    
    with open("./data/preprocessed_messages.json", "w") as f:
        json.dump(stripped_messages, f, cls=EnhancedJSONEncoder, ensure_ascii=False)


if __name__ == "__main__":
    main()