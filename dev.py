from mingus.containers import Bar
from mingus.containers import Track
import mingus.extra.lilypond as LilyPond
import os
os.chdir("C:\\Users\\Greg\\Downloads")
b = Bar()
b1 = Bar()
b.place_notes("Bb-4", 4)
b.place_notes("E-4", 16)
b1.place_notes("C-2", 1)
t = Track()
t.add_bar(b)
t.add_bar(b1)
bar = LilyPond.from_Track(t)
LilyPond.to_png(bar, "my_first_barr")