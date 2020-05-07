from notebook import Notebook
from note import Note
from encryption import Encryption
import argparse


def load_args():
    parser = argparse.ArgumentParser(description='Python Note Logger')


if __name__ == '__main__':
    encryption = Encryption('key.key')
    load_args()
    notebook = Notebook(encryption)
    test_note = Note('Books I have read', '2019 Books', 'Books', ['read', 'books', '2019'])
    notebook.add_note(test_note)
    notebook.save_to_file('test.dat')

    notebook2 = Notebook(encryption)
    notebook2.load_from_file('test.dat')
    for note in notebook2:
        note.print()
