import json
from difflib import get_close_matches
import os
from typing import List, Union

current_directory = os.getcwd()

def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question: str, questions: List[str]) -> Union[str, None]:
    matches = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> Union[str, None]:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]
    return None

def chat_bot():
    knowledge_base: dict = load_knowledge_base(f"{current_directory}/node_express.json")
    
    while True:
        user_input: str = input("User: ")
        if user_input.lower() == "exit":
            break

        questions_list = [q["question"] for q in knowledge_base["questions"]]
        best_match: Union[str, None] = find_best_match(user_input, questions_list)

        if best_match:
            answer: Union[str, None] = get_answer_for_question(best_match, knowledge_base)
            print(f"Bot: {answer}")
        else:
            print("Bot: Sorry, I don't understand that. Can you please teach me?")
            new_answer: str = input("Type the answer or 'skip' to skip: ")

            if new_answer.lower() == "skip":
                continue
            else:
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                save_knowledge_base(f"{current_directory}/node_express.json", knowledge_base)
                print("Bot: Thanks, the new data has been added!")

if __name__ == "__main__":
    chat_bot()
