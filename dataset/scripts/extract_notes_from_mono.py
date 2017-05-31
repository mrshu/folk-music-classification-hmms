from mido import Message, MidiFile, MidiTrack
import sys

mid = MidiFile(sys.argv[1])
for msg in mid.tracks[0]:
    if msg.type == 'note_on':
        print(msg.note)
