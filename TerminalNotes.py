
import sys
import datetime


class Exceptions:
    class NoNotesError(LookupError):
        def __init__(self):
            super().__init__("Your notes list is empty.")

    class NoNotesFoundError(KeyError):
        def __init__(self):
            super().__init__("No notes for your tags were found.")

    class InvalidOptionError(ValueError):
        def __init__(self, choice):
            super().__init__(f"{choice} is not valid choice.")

    class InvalidIdNote(KeyError):
        def __init__(self):
            super().__init__("Sorry, there is no notebook with this index")

    class InvalidTypeError(TypeError):
        def __init__(self):
            super().__init__("Sorry, it's not an integer")


class Note:
    memo: str
    tag: str
    dateCreate: datetime.date
    lastChange: datetime.date
    id: int

    def __init__(self, _memo="", _tag="", _dateCreate=datetime.date.today(), _lastChange=datetime.date.today(), _id=0):
        self.memo = _memo
        self.tag = _tag
        self.dateCreate = _dateCreate
        self.lastChange = _lastChange
        self.id = _id


class NoteFunctions:
    last_id: int
    notes_info: [Note]
    interaction_function_list: dict

    def __init__(self, last_id=1, notes_info=[]):
        self.last_id = last_id
        self.notes_info = notes_info
        self.interaction_function_list = {
            "1": self.show_all_notes,
            "2": self.search_notes,
            "3": self.add_note,
            "4": self.modification,
            "5": self.quit
        }

    def start(self):
        while True:
            try:
                self.interaction()
            except (Exceptions.NoNotesError, Exceptions.NoNotesFoundError, Exceptions.InvalidOptionError,
                    Exceptions.InvalidIdNote, Exceptions.InvalidTypeError) as e:
                print(e)

    def interaction(self):
        print(''.join(80 * ["="]))
        print(f"""
Notebook Menu:
1. Show all Notes
2. Search Notes
3. Add Note
4. Modify Note
5. Quit
""")
        choice = input("Enter an option: ")
        if choice in ["1", "2", "3", "4", "5"]:
            print(''.join(80 * ["="]))
            self.interaction_function_list[str(choice)]()
        else:
            raise Exceptions.InvalidOptionError(choice)

    def show_all_notes(self, notes=None):
        if len(self.notes_info) == 0:
            raise Exceptions.NoNotesError
        if not notes:
            notes = self.notes_info

        sorted_array = sorted(
            notes,
            key=lambda x: x.lastChange
        )

        for i in sorted_array:
            print(f"""Note id: {i.id}
Note memo: {i.memo}
Note tag: {i.tag}
Last Change: {i.lastChange}
Created: {i.dateCreate}
""")

    def search_notes(self):
        searchtags = input("Search for: ")
        found = []
        for i in self.notes_info:
            if i.tag == searchtags or i.memo == searchtags:
                found.append(i)
        if len(found) == 0:
            raise Exceptions.NoNotesFoundError()
        else:
            self.show_all_notes(found)

    def add_note(self):
        memo = input("Enter a memo: ")
        tag = input("Enter tag: ")

        new_note = Note()
        new_note.id = self.last_id
        new_note.memo = memo
        new_note.tag = tag

        self.last_id += 1
        self.notes_info.append(new_note)

        print("Your note has been added.")

    def modification(self):
        global thing
        note_id = input("Enter a note id: ")
        try:
            note_id = int(note_id)
        except:
            raise Exceptions.InvalidTypeError()
        if note_id > len(self.notes_info) or note_id < 1:
            raise Exceptions.InvalidIdNote
        memo = input("Enter a memo: ")
        tags = input("Enter tags: ")
        if memo:
            thing = None
            for i in self.notes_info:
                x = i
                if x.id == note_id:
                    thing = x
            if thing:
                thing.memo = memo
        if tags:
            for i in self.notes_info:
                thing = i
                if thing.id == note_id:
                    thing.tag = tags
                    break
        thing.lastChange = datetime.date.today()

    def quit(self):
        print("Thank you for using your Notebook today.")
        sys.exit(0)


if __name__ == "__main__":
    NoteFunctions().start()
