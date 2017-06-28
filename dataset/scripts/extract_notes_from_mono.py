from mido import Message, MidiFile, MidiTrack
import sys

mid = MidiFile(sys.argv[1])
notes = []
for msg in mid.tracks[0]:
    if msg.type == 'note_on':
        notes.append(str(msg.note))
print(', '.join(notes))
