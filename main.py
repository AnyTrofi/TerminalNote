import sys
import datetime
import os
import csv
import json


class Exceptions:
    """Custom error class

    Consists of classes of various errors.
    Each error class is inherited from the middle error class with the same value.
    """

    class NoNotesError(LookupError):
        """Class No Note Error"""
        def __init__(self):
            """This function load custom error message"""
            super().__init__("Your notes list is empty.")

    class NoNotesFoundError(KeyError):
        """Class No Notes Found Error"""
        def __init__(self):
            """This function load custom error message"""
            super().__init__("No notes for your tags were found.")

    class InvalidOptionError(ValueError):
        """Class Invalid Option Error"""
        def __init__(self, choice):
            """This function load custom error message"""
            super().__init__(f"{choice} is not valid choice.")

    class InvalidIdNote(KeyError):
        """Class Invalid Id Note Error"""
        def __init__(self):
            """This function load custom error message"""
            super().__init__("Sorry, there is no notebook with this index")

    class InvalidTypeError(TypeError):
        """Class Invalid Type Error"""
        def __init__(self):
            """This function load custom error message"""
            super().__init__("Sorry, it's not an integer")



class Note:
    """Note class

    This class creates a new data type "Notepad"

    Class fields:
        memo: Name
        tag: Meaning
        dataCreate: creation date
        lastChange: last change date
        id: ID

    class method:
        init: sets base, set values to all variables

    """
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
    """NoteFunctions class with all notepad functions

    This class contains all the notepad functions for the user to work with it.

    Class fields:
        last_id: The last ID given to the notebook.
        notes_info: array with variables of type Note, needed to store all notepads
        interaction_function_list: Dictionary with all functions of class NoteFunctions

    Class methods:
        __init__: Sets base values ​​for fields of this class
        start
        interaction
        show_all_notes
        search_notes
        add_note
        modification
        quit
    """
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

    def check_file(self):
        """This function check the file

        The function does not need to be passed anything and it does not return anything."""

        try:
            with open("data.csv", encoding='utf-8') as r_file:
                file_reader = csv.reader(r_file, delimiter=",")
                count = 0
                array = []
                for row in file_reader:
                    if count != 0:
                        array.append(row)
                    count += 1
                for i in array:
                    note = Note()
                    note.id = int(i[0])
                    note.tag = i[1]
                    note.memo = i[2]
                    note.lastChange = i[3]
                    note.dateCreate = i[4]
                    self.notes_info.append(note)
                self.last_id = len(self.notes_info) + 1
        except:
            notes_file = open("data.csv", "w")




    def start(self):
        """This function starts the program and restarts it in case of errors.

        The function does not need to be passed anything and it does not return anything.
        """
        self.check_file()
        while True:
            try:
                self.interaction()
            except (Exceptions.NoNotesError, Exceptions.NoNotesFoundError, Exceptions.InvalidOptionError,
                    Exceptions.InvalidIdNote, Exceptions.InvalidTypeError) as e:
                print(e)

    def interaction(self):
        """This function displays the menu, and starts the desired function depending on the user's choice.

        The function takes nothing and returns nothing.
        """

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
        """This function displays all available notebooks.

        The function input receives notes, it is needed so that if the function is called from search_notes, then display only the necessary functions

        The function returns nothing
        """

        if len(self.notes_info) == 0:
            raise Exceptions.NoNotesError
        if not notes:
            notes = self.notes_info

        for i in notes:
            print(f"""Note id: {i.id}
Note memo: {i.memo}
Note tag: {i.tag}
Last Change: {i.lastChange}
Created: {i.dateCreate}
""")

    def search_notes(self):
        """This function searches for notebooks according to the specified parameters, and if successful, calls show_all_notes, passing the list of found notebooks there, otherwise it raises an error

        The function takes nothing and returns nothing.
        """

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
        """This function adds a new notepad

        The function takes nothing and returns nothing.
        """

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
        """This function modifies the notebook by the given id

        If there is no such id, then an error is raised.

        The function takes nothing and returns nothing.
        """

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
        """This function terminates

        The function takes nothing and returns nothing.
        """

        notes_file = open("data.csv", "w")
        writer = csv.writer(notes_file)
        writer.writerow(["Id", "Tag", "Memo", "lastChange", "dateCreate"])
        array = []
        for i in self.notes_info:
            array.append(str(i.id))
            array.append(str(i.tag))
            array.append(str(i.memo))
            array.append(str(i.lastChange))
            array.append(str(i.dateCreate))
            writer.writerow(array)
            array = []
        print("Thank you for using your Notebook today.")

        sys.exit(0)


if __name__ == "__main__":
    NoteFunctions().start()


