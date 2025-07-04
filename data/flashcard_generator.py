import uuid
import json
import os
from datetime import datetime

class FlashcardManager:
    def __init__(self, filepath="flashcards.json"):
        self.filepath = filepath
        self.flashcards = self.load_flashcards()

    def load_flashcards(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r") as f:
                    data = json.load(f)
                    # Ensure all flashcards have an ID
                    for card in data:
                        if "id" not in card:
                            card["id"] = str(uuid.uuid4())
                    return data
            except Exception as e:
                print("Error loading flashcards:", e)
                return []
        return []

    def save_flashcards(self):
        try:
            with open(self.filepath, "w") as f:
                json.dump(self.flashcards, f, indent=2)
        except Exception as e:
            print("Error saving flashcards:", e)

    def add_flashcard(self, question, answer):
        new_card = {
            "id": str(uuid.uuid4()),                       # ✅ Unique ID
            "question": question.strip(),
            "answer": answer.strip(),
            "created": datetime.utcnow().isoformat(),
            "last_reviewed": None,
            "next_review": datetime.utcnow().isoformat(),  # Start now
            "attempts": 0,
            "correct": 0
        }
        self.flashcards.append(new_card)
        self.save_flashcards()

    def get_flashcard_by_id(self, card_id):
        return next((c for c in self.flashcards if c["id"] == card_id), None)

    def delete_flashcard(self, card_id):
        self.flashcards = [c for c in self.flashcards if c["id"] != card_id]
        self.save_flashcards()

    def update_flashcard(self, updated_card):
        for i, card in enumerate(self.flashcards):
            if card["id"] == updated_card["id"]:
                self.flashcards[i] = updated_card
                break
        self.save_flashcards()
