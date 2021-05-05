from abc import ABC, abstractmethod
from typing import Union


class Document:
    def __init__(self, init_text: str = ''):
        self.content = init_text
        self.copy_buffer = None

    def __repr__(self):
        return self.content

    def __str__(self):
        return self.__repr__()


class Editor:

    def get_selection(self, doc: Document, snippet: str):
        # in sake of simplicity lets make an assumption that this snippet is unique for this document
        if snippet in doc.content:
            return snippet
        else:
            raise ValueError(f'No "{snippet}" snippet in this text')

    def del_selection(self, doc: Document, snippet: str):
        snip = self.get_selection(doc, snippet)
        doc.content = doc.content.replace(snip, '')

    @staticmethod
    def paste_selection(doc: Document, highlighted: tuple, new: str):
        highlighted = sorted(highlighted)
        if highlighted[0] == -1:
            doc.content += new
        elif highlighted[1] == -1:
            doc.content = doc.content[:highlighted[0]] + new
        else:
            doc.content = doc.content[:highlighted[0]] + new + doc.content[highlighted[1]:]


class CommandHistory:
    def __init__(self):
        self.memory = []

    def push(self, command):
        self.memory.append(command)

    def pop(self, command):
        return self.memory.pop(self.memory.index(command))


class Command(ABC):
    history = CommandHistory()

    def __init__(self, editor: Editor, document: Document):
        self.editor = editor
        self.doc = document
        self.backup = document.content

    @abstractmethod
    def execute(self, *args, **kwargs):
        pass

    @abstractmethod
    def undo(self, *args, **kwargs):
        pass

    def save(self):
        self.backup = self.doc.content


class CopyCommand(Command):
    def __init__(self, editor: Editor, document: Document):
        super().__init__(editor, document)

    def execute(self, snippet):
        self.doc.copy_buffer = snippet
        self.history.push(self)

    def undo(self):
        self.doc.copy_buffer = None
        self.history.pop(self)


class PasteCommand(Command):
    def __init__(self, editor: Editor, document: Document):
        super().__init__(editor, document)

    def execute(self, highlighted):
        self.save()
        self.editor.paste_selection(self.doc, highlighted, self.doc.copy_buffer)
        self.history.push(self)

    def undo(self, *args, **kwargs):
        self.doc.content = self.backup
        self.history.pop(self)


class DeleteCommand(Command):
    def __init__(self, editor: Editor, document: Document):
        super().__init__(editor, document)

    def execute(self, snippet):
        self.save()
        self.editor.del_selection(self.doc, snippet)

    def undo(self):
        self.doc.content = self.backup


if __name__ == '__main__':
    doc1 = Document('Chapter 1')
    editor = Editor()
    hist = Command

    copy = CopyCommand(editor, doc1)
    copy.execute(' New path')
    print(copy.history.memory)
    print(doc1)

    paste = PasteCommand(editor, doc1)
    paste.execute(highlighted=(-1, -1))
    print(copy.history.memory)
    print(doc1)

    delete = DeleteCommand(editor, doc1)
    delete.execute('New')
    print(copy.history.memory)
    print(doc1)
