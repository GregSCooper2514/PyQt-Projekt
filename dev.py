from mingus.containers import Bar
import mingus.extra.lilypond as LilyPond
import os
os.chdir("C:\\Users\\Greg\\Downloads")
b = Bar()
b + "C-0"
b + "C#-0"
b + "D-0"
b + "E-20"
bar = LilyPond.from_Bar(b)
LilyPond.to_png(bar, "my_first_bar")