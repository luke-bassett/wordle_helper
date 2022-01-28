# Wordle Helper
Helps you cheat at wordle.

## Usage
If you have taken two guesses, "rusty", and "about" and these were your results:  
⬜🟨⬜🟨⬜  
⬜⬜🟨🟨🟩  

then you would type this to see the top five most frequently used valid words:

**Input**
```
python wordle_helper.py -n 5 rusty/gygyg about/ggyyn
```

**Output**
```
most frequent valid words
mount
count
moult
fount
hoult
```

## Word frequency list from here
https://github.com/IlyaSemenov/wikipedia-word-frequency/blob/master/results/enwiki-20190320-words-frequency.txt
