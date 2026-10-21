from database.repository import get_notes

notes = get_notes(1)

for note in notes:
    print(note.timestamp, note.content)