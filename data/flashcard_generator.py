import json
import os
from datetime import datetime

FLASHCARD_FILE = "flashcards.json"


class FlashcardManager:
    def __init__(self, autosave=True):
        self.flashcards = []
        self.autosave = autosave
        self.load_flashcards()

    def add_flashcard(self, question, answer):
        card = {
            "question": question.strip(),
            "answer": answer.strip(),
            "created_at": datetime.now().isoformat(),
            "attempts": 0,
            "correct": 0,
            "last_reviewed": None,
            "memory_score": 0.0,
        }
        self.flashcards.append(card)
        if self.autosave:
            self.save_flashcards()

    def get_all_flashcards(self):
        return self.flashcards

    def save_flashcards(self):
        try:
            with open(FLASHCARD_FILE, "w", encoding="utf-8") as f:
                json.dump(self.flashcards, f, indent=4)
        except Exception as e:
            print(f"Error saving flashcards: {e}")

    def load_flashcards(self):
        if os.path.exists(FLASHCARD_FILE):
            try:
                with open(FLASHCARD_FILE, "r", encoding="utf-8") as f:
                    self.flashcards = json.load(f)
            except Exception as e:
                print(f"Error loading flashcards: {e}")
                self.flashcards = []

    def update_flashcard(self, index, update_data):
        """Update any flashcard fields such as memory_score, attempts, last_reviewed"""
        if 0 <= index < len(self.flashcards):
            self.flashcards[index].update(update_data)
            if self.autosave:
                self.save_flashcards()

    def clear_flashcards(self):
        self.flashcards = []
        if self.autosave:
            self.save_flashcards()
