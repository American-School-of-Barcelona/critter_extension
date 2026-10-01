# Critter Extension

You already have a working Critter Caretaker. This is how you make it more.

Fifteen stages, each adding one thing. The early ones show you every line you need to
change. The later ones describe what the program should do and leave the code to you.
That shift is deliberate — the point of the first half is to get you fluent enough that
the second half is possible.

---

## Before you start

Get the program and run it.

```bash
git clone https://github.com/mrcarle-asb/critter_extension.git
cd critter_extension
python3 critter.py
```

Play it until you have seen a critter go from `happy` to `mad`. Then quit with `0`.

### What's in here

| File | What it is |
|---|---|
| `critter.py` | The finished program. Your starting point. Run it, then change it. |
| `README.md` | This file. Fifteen stages of changes to make. |
| `critter_uml.md` | The class diagram of `critter.py` as it starts, and how to read Python types into UML. |

Now open `critter.py` and read it. You are looking for three things:

1. **The class** — `class Critter`, everything indented under it. The template.
2. **`main()`** — the menu loop. This is the *game*, not the critter.
3. **The line at the bottom** — `if __name__ == "__main__":` — which starts the game when
   you run the file, and does *not* start it when you import the file.

That last point is what makes this possible:

```bash
python3 -i critter.py
```

`-i` means "run it, then leave me at the prompt". Quit the game with `0` and you are still
in Python, with the `Critter` class loaded:

```
>>> crit = Critter("Fluffy")
A new critter has been born!
>>> crit
Critter(name='Fluffy', hunger=0, boredom=0, mood='happy')
>>> crit.talk()
Fluffy says: I feel happy right now.
>>> crit
Critter(name='Fluffy', hunger=1, boredom=1, mood='happy')
```

**Use this constantly.** It is much faster than restarting the game every time you want to
know whether something worked.

### How to read the stages

Three kinds of instruction, same as the build guide:

- **ADD** — type this in; nothing else changes
- **CHANGE** — a line you already have becomes a different line
- **DELETE** — take something out

And three levels of help, which decrease as you go:

| Marker | What you get |
|---|---|
| 🔧 **DO THIS** | Every line you need, written out |
| 🧩 **WORK IT OUT** | What it should do, and where to look. No code. |
| 🚀 **ON YOUR OWN** | A description of the finished thing. Nothing else. |

### About the sample output

Every stage ends with output from a real run. **Compare behaviour, not wording.** If your
critter says "Fluffy is munching" where ours says "Fluffy eats", you have not made a
mistake — you have made a choice. What has to match is *what happens*: the right numbers
moving the right way at the right time.

Nothing here is marked automatically. Reading your own output and deciding whether it is
right is the skill.

> **One difference from the version we built in class.** In this copy, `__init__` assigns
> the name *through the property setter*, so `Critter("")` is refused instead of quietly
> producing a nameless critter. Compare the two `__init__` methods and you will see why.

---

# Part 1 — Let the player decide how much

> **Dawson, challenge 1:** Improve the Critter Caretaker program by allowing the user to
> specify how much food he or she feeds the critter and how long he or she plays with the
> critter. Have these values affect how quickly the critter's hunger and boredom levels
> drop.

Half of this is already done. Finding that out is stage 1.

## Stage 1 — 🔧 Find out what you already have

**Write no code.** Look at these two lines in `critter.py`:

```python
    def eat(self, food=4):
    def play(self, fun=4):
```

`food=4` is a **default parameter**. It means: if nobody says how much, use 4. Which also
means — if somebody *does* say, use that instead. The ability Dawson is asking for is
already in the class. It just isn't reachable from the menu.

Prove it. `python3 -i critter.py`, quit with `0`, then neglect a critter and feed it badly:

```
>>> crit = Critter("Fluffy")
A new critter has been born!
>>> for _ in range(6):
...     crit.talk()
...
Fluffy says: I feel happy right now.
Fluffy says: I feel happy right now.
Fluffy says: I feel happy right now.
Fluffy says: I feel okay right now.
Fluffy says: I feel okay right now.
Fluffy says: I feel okay right now.
>>> crit
Critter(name='Fluffy', hunger=6, boredom=6, mood='frustrated')
>>> crit.eat(1)
Fluffy eats.
>>> crit
Critter(name='Fluffy', hunger=6, boredom=7, mood='frustrated')
>>> crit.eat(10)
Fluffy eats.
>>> crit
Critter(name='Fluffy', hunger=1, boredom=8, mood='okay')
```

Look hard at `crit.eat(1)`. Hunger went in at 6 and came out at 6. **A one-food meal does
not keep up with time passing** — `eat()` took 1 off, and then `_pass_time()` put 1 back on.
The critter ate and got no further forward.

Now look at `crit.eat(10)`. Hunger was 6, and 10 food took it to 0 — but only 6 of that
food did anything. The other 4 vanished. Remember that; it is stage 5.

**Your job in stages 2 and 3** is only to let the player reach the parameter that is
already there.

## Stage 2 — 🔧 Ask how much food

**CHANGE** the `choice == "2"` branch in `main()`:

```python
        elif choice == "2":
            amount = int(input("How much food do you give it?: "))
            crit.eat(amount)
```

Two things happen on that first line. `input()` always hands back a **string** — if the
player types `8` you get `"8"`, and `self._hunger -= "8"` is not a thing. `int()` converts
it to a number. Then that number is passed to `eat()`, landing in `food`.

**Run it:**

```
Fluffy is happy.

0 - Quit
1 - Listen to your critter
2 - Feed your critter
3 - Play with your critter

Choice: 2
How much food do you give it?: 8
Fluffy eats and seems happy.
```

## Stage 3 — 🔧 Ask how long they play

Same shape, other branch. **CHANGE** the `choice == "3"` branch:

```python
        elif choice == "3":
            amount = int(input("How many minutes do you play for?: "))
            crit.play(amount)
```

`play()` calls its parameter `fun`, not `food`, but you do not need to care — you are passing
a number in by position, and `play` can call it whatever it likes.

**Run it:**

```
Choice: 3
How many minutes do you play for?: 2
Fluffy plays and laughs!
```

Notice you now have the same two lines twice, with one word different. Hold that thought.

## Stage 4 — 🔧 What happens when they type "banana"

Run the program and feed your critter `banana`:

```
Choice: 2
How much food do you give it?: banana
Traceback (most recent call last):
  File "critter.py", line 147, in <module>
    main()
  File "critter.py", line 135, in main
    amount = int(input("How much food do you give it?: "))
ValueError: invalid literal for int() with base 10: 'banana'
```

The game is dead. Your critter is gone. `int()` was handed something that is not a number
and it had nowhere to go.

Read that error, because you will see it a thousand more times. `ValueError` means *the
right kind of thing, the wrong value* — `int()` does take strings, just not that one. The
file and line number tell you where to look.

The fix: don't convert until you know it will work. **ADD** this function above `main()`:

```python
def ask_for_amount(question):
    """Ask until the player types a whole number, then hand it back as an int."""
    while True:
        answer = input(question)
        if answer.isdigit():
            return int(answer)
        print("Please type a whole number, like 4.")
```

`while True` loops forever. The only way out is `return`, which happens only once
`.isdigit()` agrees that every character is a digit. Anything else falls through to the
`print` and goes round again.

**CHANGE** both branches to use it — this is where that doubled line pays off:

```python
        elif choice == "2":
            amount = ask_for_amount("How much food do you give it?: ")
            crit.eat(amount)
        elif choice == "3":
            amount = ask_for_amount("How many minutes do you play for?: ")
            crit.play(amount)
```

**Run it:**

```
Choice: 2
How much food do you give it?: banana
Please type a whole number, like 4.
How much food do you give it?: -3
Please type a whole number, like 4.
How much food do you give it?: 8
Fluffy eats and seems happy.
```

`-3` was rejected too, and nobody wrote a rule about negatives. `"-3".isdigit()` is `False`
because `-` is not a digit. You got that for free — but check you understand *why*, because
free things you don't understand break later.

## Stage 5 — 🧩 Stop the player wasting food

Back to the end of stage 1: a critter with hunger 6, fed 10 food, ends at hunger 0. Four
food did nothing at all, and the program never said so.

**Make `eat()` tell the player when food was wasted**, and make `play()` do the same for fun.

Where to look: the first two lines of `eat()`. The problem is that by the time you know
hunger has bottomed out at 0, you have already lost the number it started from. You will
need that number before you change it.

Your output should do something along these lines (your wording will differ):

```
Choice: 2
How much food do you give it?: 10
Fluffy only needed 6. You wasted 4 food.
Fluffy eats and seems happy.
```

Then check the case that must still be silent: a critter with hunger 6 fed exactly 6, and
a critter with hunger 6 fed 2. Neither of those wasted anything, and neither should say so.

---

# Part 2 — Let the critter introduce itself

> **Dawson's challenge 3** asks you to build a secret "back door" menu choice that prints
> the object's raw attribute values, using `__str__`.
>
> **We are not doing that one**, for a reason worth knowing: our Critter *already* has a
> method that prints its raw attribute values. It is called `__repr__` and you have been
> reading its output since page one of this file. The back door is already open.
>
> So this part asks a better question. Not *how do I see inside the object* — you can — but
> **how does an object describe itself to a player rather than to a programmer?**

## Stage 6 — 🔧 Print a critter and watch what you get

**Write no code.** `python3 -i critter.py`, quit the game, and print a critter:

```
>>> crit = Critter("Fluffy")
A new critter has been born!
>>> print(crit)
Critter(name='Fluffy', hunger=0, boredom=0, mood='happy')
>>> print(f"Meet {crit}!")
Meet Critter(name='Fluffy', hunger=0, boredom=0, mood='happy')!
```

That second line is the whole lesson. You can put a critter in an f-string and Python will
put *something* there — but what it put there is debugging output with brackets and quote
marks in the middle of a sentence you were trying to show a player.

Here is the machinery. When Python needs a string for an object, it asks the object:

- `print(crit)` calls `str(crit)`, which calls the object's `__str__` method
- `f"{crit}"` does the same thing
- `f"{crit!r}"` calls `__repr__` instead — that is what `!r` means, and it is why our
  `__repr__` has `{self.name!r}` in it, to get the quote marks around `'Fluffy'`

Our Critter **has no `__str__`**. When there is no `__str__`, Python falls back to
`__repr__` rather than giving up. That fallback is why `print(crit)` worked at all, and
why it printed the wrong thing.

So you are not adding a missing feature in stage 7. You are **replacing a fallback** —
behaviour you already have is about to change.

## Stage 7 — 🔧 Add `__str__`

**ADD** this method, just above `@property def name`:

```python
    def __str__(self):
        """How the critter describes itself to the player.

        Returns a string. Prints nothing, changes nothing, takes no time.
        """
        return f"{self.name}, who is feeling {self.mood}"
```

Read the body. `return`, not `print`. A phrase, not a sentence — no capital letter, no full
stop — because it is going to be dropped *into* somebody else's sentence.

**Run it** — same commands as stage 6:

```
>>> crit = Critter("Fluffy")
A new critter has been born!
>>> print(crit)
Fluffy, who is feeling happy
>>> print(f"Meet {crit}!")
Meet Fluffy, who is feeling happy!
>>> print(repr(crit))
Critter(name='Fluffy', hunger=0, boredom=0, mood='happy')
```

Three things to see:

1. `print(crit)` **changed**. It used to show the repr. It stopped falling back the moment
   there was something to fall forward to.
2. `Meet Fluffy, who is feeling happy!` reads like English.
3. `repr(crit)` is **untouched**. You did not lose the programmer's view by gaining the
   player's. The object now has two ways of describing itself, for two audiences.

> **For your UML:** `__str__` is the method your class diagram draws as
> `+ toString(): String` — a public operation that takes nothing and returns a String. The
> syllabus calls it `toString()`; Python spells it `__str__` and wires `print()` to it for
> you. Same operation, two names.

## Stage 8 — 🔧 Give the player a way to use it

A method nobody calls is not a feature. **CHANGE** the menu text in `main()` to add a
fourth line:

```python
        print(
            "\n0 - Quit"
            "\n1 - Listen to your critter"
            "\n2 - Feed your critter"
            "\n3 - Play with your critter"
            "\n4 - Introduce your critter"
        )
```

**ADD** a branch for it, after the `choice == "3"` branch:

```python
        elif choice == "4":
            print(f"\nThis is {crit}.")
```

**Run it:**

```
Fluffy is happy.

0 - Quit
1 - Listen to your critter
2 - Feed your critter
3 - Play with your critter
4 - Introduce your critter

Choice: 4

This is Fluffy, who is feeling happy.
```

Now compare choice `4` with choice `1`. Press `1`, then `4`, then `1`, then `4`, and watch
hunger in the repr. **Choice 4 does not make the critter hungrier.** Choice 1 does. You
wrote no `_pass_time()` in `__str__`, and that was not an oversight — *describing* a critter
is not *doing something to* a critter.

## Stage 9 — 🧩 `talk()` and `__str__` are not the same kind of thing

Both of them produce the words "Fluffy" and "happy". They are still completely different.
In the REPL:

```
>>> label = str(crit)
>>> label
'Fluffy, who is feeling happy'
>>> result = crit.talk()
Fluffy says: I feel happy right now.
>>> result
>>> print(result)
None
```

`str(crit)` **gave you a value you could keep.** `crit.talk()` printed something and handed
back `None` — the nothing you get when a function has no `return`. That is the difference
between a **function** (returns a value) and a **procedure** (does something). `talk()` is a
procedure with a side effect: time passes.

Answer these before you write anything:

1. Why can you write `f"Meet {crit}!"` but not `f"Meet {crit.talk()}!"`? Try it. Explain the
   output.
2. `__str__` has no `_pass_time()`. If you added one, what would go wrong the next time you
   printed a list of critters?
3. Which of the two could you call a hundred times without changing the critter at all?

**Then one change.** Numbers are a programmer's way of saying things. **Make `__str__`
describe the critter's hunger in words rather than leaving it out** — so a well-fed critter
and a starving one introduce themselves differently, without a digit anywhere in the
output. Keep it to one short phrase; it still has to fit inside `This is ___.`

---

# Part 3 — The Critter Farm

> **Dawson, challenge 4:** Create a Critter Farm program by instantiating several Critter
> objects and keeping track of them through a list. Mimic the Critter Caretaker program, but
> instead of requiring the user to care for a single critter, require them to care for an
> entire farm. Each menu choice should allow the user to perform some action for all of the
> critters (feed all of the critters, play with all of the critters, or listen to all of the
> critters). To make the program interesting, give each critter random starting hunger and
> boredom levels.

That paragraph is four new ideas stacked on top of each other: optional parameters, random
numbers, a list of objects, and a rebuilt `main()`. Stages 10 to 12 hand you the first three.
Then the help stops.

**Work in a copy.** `cp critter.py farm.py` and do Part 3 in `farm.py`, so you still have a
working one-critter game to go back to.

## Stage 10 — 🔧 Critters that don't all start the same

Right now every critter is born at hunger 0, boredom 0. A farm of identical critters is a
boring farm. The fix is not to make `__init__` random — it is to let the *caller* decide,
the same way `eat(food=4)` does.

**CHANGE** the first line of `__init__` and the two lines that set the needs:

```python
    def __init__(self, name, hunger=0, boredom=0):
        """Build a critter. Needs start at zero unless you say otherwise."""
        print("A new critter has been born!")
        self._name = "Critter"  # a fallback, so the setter below has something to keep
        self.name = name        # assigning through the property means it gets checked
        self._hunger = hunger
        self._boredom = boredom
        Critter.total += 1
```

**ADD** this at the top of the file, just below the docstring:

```python
import random
```

**Run it** — `python3 -i farm.py`, quit, then:

```
>>> a = Critter("Fluffy")
A new critter has been born!
>>> a
Critter(name='Fluffy', hunger=0, boredom=0, mood='happy')
>>> b = Critter("Bruiser", 7, 9)
A new critter has been born!
>>> b
Critter(name='Bruiser', hunger=7, boredom=9, mood='mad')
```

Nothing broke. `Critter("Fluffy")` still works exactly as before, because the defaults catch
the arguments you didn't pass. **This is what default parameters are for** — adding an
ability without breaking every existing call. It is the same trick `eat(food=4)` played on
you in stage 1.

## Stage 11 — 🔧 A list of critters

**ADD** these two functions above `ask_for_amount`:

```python
def make_farm():
    """Build a list of three critters, each with random starting needs."""
    farm = []
    for name in ["Fluffy", "Spot", "Bruiser"]:
        critter = Critter(name, random.randint(0, 5), random.randint(0, 5))
        farm.append(critter)
    return farm


def introduce_all(farm):
    """Have every critter on the farm introduce itself."""
    for critter in farm:
        print(f"This is {critter}.")
```

`random.randint(0, 5)` gives a whole number from 0 to 5, 5 included. It is called twice per
critter, so hunger and boredom are rolled separately.

`farm` is an ordinary list. The only new thing is **what is in it** — not numbers or strings,
but Critter objects, each carrying its own name, hunger, and boredom.

**Run it:**

```
>>> farm = make_farm()
A new critter has been born!
A new critter has been born!
A new critter has been born!
>>> farm
[Critter(name='Fluffy', hunger=2, boredom=1, mood='happy'), Critter(name='Spot', hunger=3, boredom=5, mood='okay'), Critter(name='Bruiser', hunger=0, boredom=0, mood='happy')]
>>> introduce_all(farm)
This is Fluffy, who is feeling happy.
This is Spot, who is feeling okay.
This is Bruiser, who is feeling happy.
```

**Your numbers will not match ours.** That is `random` doing its job. What must match is the
shape: three critters, each with its own two numbers, each mood agreeing with those numbers.

Two things worth stopping on.

**First:** `introduce_all` is three lines and you did not touch the Critter class to write it.
The `__str__` from stage 7 did all the work. That is the payoff for having built it — one
critter describing itself scaled to a farm for free.

**Second, and sharper:** look at what `farm` printed on its own. Those are `__repr__` strings,
not `__str__` strings — `Critter(name='Fluffy', ...)`, not `Fluffy, who is feeling happy`. The
list did not use the `__str__` you just wrote. **A container always uses `repr` on the things
inside it,** because when you print a list you are a programmer inspecting data, not a player
meeting a pet. Python guessed your audience from the context, and it guessed right.

## Stage 12 — 🔧 Do one thing to all of them

**ADD** this, next to the other two:

```python
def feed_all(farm, food):
    """Feed every critter on the farm the same amount."""
    for critter in farm:
        critter.eat(food)
```

Three lines, and two of them are the loop. `critter.eat(food)` is the method you have had
since the start; the only new idea is calling it once per item in a list.

**Run it:**

```
>>> farm = make_farm()
A new critter has been born!
A new critter has been born!
A new critter has been born!
>>> introduce_all(farm)
This is Fluffy, who is feeling happy.
This is Spot, who is feeling okay.
This is Bruiser, who is feeling happy.
>>> feed_all(farm, 5)
Fluffy eats and seems happy.
Spot eats.
Bruiser eats and seems happy.
>>> Critter.status()

The total number of critters is: 3
```

Read the three lines `feed_all` printed. **They are not the same.** Spot said "Spot eats"
while the others "seemed happy", because each critter checked *its own* mood and they were
in different states. One function call, one amount of food, three different answers — every
critter is deciding for itself.

## Stage 13 — 🧩 The other two actions

You have `feed_all`. The farm also needs to **play with all the critters** and **listen to
all the critters**.

No sample code for these. `feed_all` is the pattern and you have read it; these are the same
shape with a different method called inside the loop. One of the two does not need an amount
at all — work out which, and why, before you write either.

Check it the way you checked stage 12: build a farm, call your function, and confirm that
different critters say different things.

## Stage 14 — 🧩 The farm menu

Rebuild `main()` so the game is about the farm instead of one critter.

What has to change:

- One `Critter` becomes a list, from `make_farm()`
- The line above the menu reports on the whole farm rather than `{crit.name} is {crit.mood}`
- Each of choices 1, 2, 3, 4 calls one of your `*_all` functions
- Choices 2 and 3 still ask how much, still through `ask_for_amount` — once for the whole
  farm, not once per critter
- `Critter.status()` still runs at the end, and should now report 3

You already have every piece. This stage is wiring, not invention.

Here is the skeleton, and only the skeleton:

```python
def main():
    farm = make_farm()

    choice = None
    while choice != "0":
        # report on the farm here

        print(
            "\n0 - Quit"
            "\n1 - Listen to all your critters"
            "\n2 - Feed all your critters"
            "\n3 - Play with all your critters"
            "\n4 - Introduce all your critters"
        )

        choice = input("\nChoice: ")

        # one branch per choice, as before

    Critter.status()
```

The deliberately hard part is the first comment. `crit.mood` was one critter's mood; a farm
has three. Decide what one line should say about three critters, then write it. There is no
right answer, but there are wrong ones — "the farm is happy" when one critter is `mad` is a
program lying to its player.

## Stage 15 — 🚀 Make it a real farm

Specification only. How you get there is yours.

1. **The player decides how big the farm is**, instead of always three, and names each
   critter themselves. An empty name must not produce a nameless critter — the class already
   refuses one, so find out what your farm code does when the player just presses Enter, and
   make that sensible.
2. **Feeding the whole farm the same amount is crude.** Let the player feed one named
   critter, chosen from a list, as well as feeding everybody.
3. **The farm reports honestly.** Before the menu, show how many critters are hungry, bored,
   or `mad` — not just a single mood word for all of them.
4. **A critter left `mad` for too long leaves the farm.** Add whatever state this needs,
   decide what "too long" means, and tell the player when it happens.

Item 4 will make you change the Critter class itself, not just the farm code. That is the
first time in this whole document you have had to add state to the class, and you should
notice how different it feels from adding a function outside it.

---

## What each stage was for

| Stage | The one new idea |
|---|---|
| 1 | a default parameter is an ability already present, not yet reachable |
| 2 | `input()` returns a string; a number has to be made from it |
| 3 | the same two lines written twice is a signal, not a problem |
| 4 | validate before you convert; `while True` + `return` as the exit |
| 5 | a program that silently throws work away is not finished |
| 6 | `print()` asks the object for a string; with no `__str__` it falls back to `__repr__` |
| 7 | one object, two descriptions, two audiences |
| 8 | describing a thing is not doing something to it |
| 9 | function returns a value; procedure has an effect |
| 10 | default parameters let you add an ability without breaking old calls |
| 11 | a list can hold objects; containers print their contents with `repr` |
| 12 | one loop, one method call, and every object answers for itself |
| 13 | reading a pattern well enough to write the next one |
| 14 | the game loop is not the class, and changing one need not change the other |
| 15 | a specification, and no help at all |

## Check yourself

1. In stage 1 you fed a critter 1 food and its hunger did not move. Where did the food go?
2. `"-3".isdigit()` is `False` and nobody wrote a rule about negative numbers. Why does
   stage 4 reject `-3` anyway — and what would `"3.5"` do?
3. Before stage 7, `print(crit)` already worked. What was it calling, and why is that a
   fallback rather than the intended answer?
4. In stage 11, `print(farm)` shows `__repr__` for each critter even though you had written
   `__str__`. What does that tell you about who Python thinks is reading a list?
5. `introduce_all` works on a farm of 3 and a farm of 300, and you never wrote a number in
   it. Which line is responsible?
6. Stage 15 item 4 makes you edit the Critter class, while items 1 to 3 do not. What is it
   about "a critter leaves the farm" that the class has to know and the farm cannot?

---

## Where this came from

The Critter Caretaker program is adapted from Mike Dawson's *Python Programming for the
Absolute Beginner*, 3rd Edition, Chapter 8. Parts 1 and 3 follow his end-of-chapter
challenges 1 and 4. Part 2 replaces his challenge 3 (a `__str__`-based "back door") with a
different exercise, for the reason given at the top of that part.

The code here diverges from the book in two deliberate ways: single-underscore privacy
(`_mood`) rather than double (`__mood`), because this class has no inheritance and therefore
no need for name mangling; and a `__repr__` from the start, so a critter can always describe
its own state in the REPL.
