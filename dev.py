from mingus.containers import Bar
from mingus.containers import Track
import mingus.extra.lilypond as LilyPond
from mingus.containers.instrument import Instrument, Piano, Guitar
i = Instrument()
i.name = "Lol"
i.clef = "bass"
import os
os.chdir("C:\\Users\\Greg\\Downloads")
b1 = Bar()
b1 + "C-4"
b2 = Bar()
b2 + "E-4"
b3 = Bar()
b3 + "C-4"
b4 = Bar()
b4 + "E-4"
b5 = Bar()
b5 + "C-4"
b6 = Bar()
b6 + "E-4"
b7 = Bar()
b7 + "C-4"
b8 = Bar()
b8 + "E-4"
b9 = Bar()
b9 + "C-4"
b10 = Bar()
b10 + "E-4"
t = Track(instrument="Lol")
t.add_bar(b1)
t.add_bar(b2)
t.add_bar(b3)
t.add_bar(b4)
t.add_bar(b5)
t.add_bar(b6)
t.add_bar(b7)
t.add_bar(b8)
t.add_bar(b9)
t.add_bar(b10)
bar = LilyPond.from_Track(t)
LilyPond.to_png(bar, "my_first_bar")