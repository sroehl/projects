from notebook import Notebook
from note import Note
import argparse

def load_args():
    parser = argparse.ArgumentParser(description='Python Note Logger')
    parser.add_argument()


if __name__ == '__main__':
    load_args()
    notebook = Notebook()
    test_note = Note('Books I have read', '2019 Books', 'Books', ['read', 'books', '2019'])
    notebook.add_note(test_note)
    notebook.save_to_file('test.dat')

    notebook2 = Notebook()
    notebook2.load_from_file('test.dat')
    for note in notebook2:
        note.print()
