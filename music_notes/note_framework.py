
# If 4/4, create one list per quarter note. 
# Based on how many lists there are in the composition determines how many quarter notes are in the composition
# How many notes in the quarter note list dertermine the speed of notes
# - one: 1/4
# - two: 1/8
# - three: triplets 
# - four: 1/16

# drawbacks: doesn't account for swing / timing that combines quarternotes
# - halfnotes
# - store scale type and scale degrees or notes
# - store octave?
# - store string / location?



# |----1----|--2---2--|-3--3--3-|-4-4-4-4-|
# |----1----|--2---2--|-3--3--3-|-4-4-4-4-|
# |----1----|--2---2--|-3--3--3-|-4-4-4-4-|
# |----1----|--2---2--|-3--3--3-|-4-4-4-4-|
#      1       1   &    1  e  &   1 e & a

composition = [[1],[2],[3],[4],[5,6,7],[8,9,10]] 

# Step 1: make a webpage with a guitar neck
# - shows values in divs. Values are either fret number, scale degree or note

# Step 2: make a metronome with bpm settings
# - add a few different midi files for the beat patterns, with at least one swing.