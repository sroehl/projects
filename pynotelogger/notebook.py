import json

from note import Note


class Notebook:

    def load_from_file(self, file):
        with open(file, 'r') as json_file:
            notes_to_load = json.load(json_file)
        for id in notes_to_load:
            json_note = notes_to_load[id]
            note = Note(json_note['text'], json_note['title'], json_note['group'], json_note['tags'])
            note.date = json_note['date']
            note.update_date = json_note['update']
            note.id = json_note['id']
            self.notes[id] = note

    def save_to_file(self, file):
        notes_to_save = {}
        for note in self.notes:
            notes_to_save[note] = self.notes[note].save()
        with open(file, 'w') as json_file:
            json.dump(notes_to_save, json_file)

    def add_note(self, note):
        self.notes[note.id] = note

    def __iter__(self):
        return (self.notes[note] for note in self.notes.__iter__())

    def __init__(self):
        self.notes = {}
