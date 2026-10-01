# Critter Extension

You already have a working Critter Caretaker. Twelve exercises that make it more.

The early ones show you every line. The later ones don't.

---

## Before you start

```bash
git clone https://github.com/mrcarle-asb/critter_extension.git
cd critter_extension
python3 critter.py
```

Play until a critter goes from `happy` to `mad`. Quit with `0`.

| File | What it is |
|---|---|
| `critter.py` | The finished program. Your starting point. |
| `README.md` | This file. Twelve exercises. |
| `critter_uml.md` | The class diagram of `critter.py` as it starts. |

**Use `python3 -i critter.py` constantly.** Quit the game with `0` and you are left at the
`>>>` prompt with the `Critter` class loaded. Far faster than restarting the game to find out
whether something worked.

**ADD** — type this in, nothing else changes. **CHANGE** — a line you have becomes a
different line. **DELETE** — take something out.

| Marker | What you get |
|---|---|
| 🔧 **DO THIS** | Every line you need |
| 🧩 **WORK IT OUT** | What it should do, and where to look. No code. |
| 🚀 **ON YOUR OWN** | A description of the finished thing. Nothing else. |

Nothing here is marked automatically. Reading your own output and deciding whether it is
right is the skill. **Compare behaviour, not wording.**

> One difference from the version we built in class: `__init__` assigns the name *through the
> property setter*, so `Critter("")` is refused. Compare the two `__init__` methods.

---

# Part 1 — Let the player decide how much

> **Dawson, challenge 1:** Improve the Critter Caretaker program by allowing the user to
> specify how much food he or she feeds the critter and how long he or she plays with the
> critter. Have these values affect how quickly the critter's hunger and boredom levels drop.

## Stage 1 — 🔧 Find what you already have

**Write no code.** Two lines in `critter.py`:

```python
    def eat(self, food=4):
    def play(self, fun=4):
```

`food=4` is a **default parameter**: use 4 if nobody says otherwise. So somebody *can* say
otherwise. Prove it — neglect a critter, then feed it badly and well:

```
>>> crit = Critter("Fluffy")
A new critter has been born!
>>> for _ in range(6): crit.talk()
...                                   (six lines of talk)
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

`eat(1)` left hunger at 6 — `eat()` took 1 off and `_pass_time()` put 1 back. `eat(10)` on a
hunger of 6 threw 4 food away. Both matter later.

The ability is already in the class. Stage 2 only makes it reachable.

## Stage 2 — 🔧 Reach it from the menu

**CHANGE** both branches in `main()`:

```python
        elif choice == "2":
            amount = int(input("How much food do you give it?: "))
            crit.eat(amount)
        elif choice == "3":
            amount = int(input("How many minutes do you play for?: "))
            crit.play(amount)
```

`input()` returns a **string**; `int()` makes a number of it.

**Run it:**

```
Choice: 2
How much food do you give it?: 8
Fluffy eats and seems happy.
```

## Stage 3 — 🔧 Validate it

Feed your critter `banana`:

```
How much food do you give it?: banana
ValueError: invalid literal for int() with base 10: 'banana'
```

Your critter is gone. `int()` was handed something that is not a number.

Don't convert until you know it will work. **ADD** above `main()`:

```python
def ask_for_amount(question):
    """Ask until the player types a whole number, then hand it back as an int."""
    while True:
        answer = input(question)
        if answer.isdigit():
            return int(answer)
        print("Please type a whole number, like 4.")
```

**CHANGE** both branches to use it:

```python
            amount = ask_for_amount("How much food do you give it?: ")
            amount = ask_for_amount("How many minutes do you play for?: ")
```

**Run it:**

```
How much food do you give it?: banana
Please type a whole number, like 4.
How much food do you give it?: -3
Please type a whole number, like 4.
How much food do you give it?: 8
Fluffy eats and seems happy.
```

Nobody wrote a rule about negatives. Work out why `-3` was rejected, and what `3.5` does.

## Stage 4 — 🧩 Stop the player wasting food

A critter at hunger 6, fed 10, ends at 0 and says nothing about the 4 wasted.

Make `eat()` report wasted food, and `play()` report wasted fun. Something like:

```
How much food do you give it?: 10
Fluffy only needed 6. You wasted 4 food.
Fluffy eats and seems happy.
```

Look at the first two lines of `eat()`. By the time hunger has bottomed out at 0 you have
lost the number it started from.

Then check the two cases that must stay silent: hunger 6 fed exactly 6, and hunger 6 fed 2.

---

# Part 2 — Let critters describe themselves

> **Dawson's challenge 3** wants a secret menu choice that prints the object's raw attributes,
> via `__str__`. We are not doing it: our Critter already prints its raw attributes, through
> `__repr__`, which you have been reading all along. The back door is open.
>
> The better question: **how does an object describe itself to a player rather than to a
> programmer?**

## Stage 5 — 🔧 Print a critter

**Write no code.**

```
>>> crit = Critter("Fluffy")
A new critter has been born!
>>> print(crit)
Critter(name='Fluffy', hunger=0, boredom=0, mood='happy')
>>> print(f"Meet {crit}!")
Meet Critter(name='Fluffy', hunger=0, boredom=0, mood='happy')!
```

`print(crit)` calls `str(crit)`, which calls the object's `__str__`. An f-string does the same.
Our Critter has **no `__str__`** — so Python fell back to `__repr__`, and put debugging output
in the middle of a sentence meant for a player.

Stage 6 does not add a missing feature. It replaces a fallback.

## Stage 6 — 🔧 Add `__str__`

**ADD** above `@property def name`:

```python
    def __str__(self):
        """How the critter describes itself to a player."""
        return f"{self.name} the {self.mood} critter"
```

`return`, not `print`. A phrase, not a sentence — it gets dropped into somebody else's.

**Run it:**

```
>>> print(crit)
Fluffy the happy critter
>>> print(f"Meet {crit}!")
Meet Fluffy the happy critter!
>>> print(repr(crit))
Critter(name='Fluffy', hunger=0, boredom=0, mood='happy')
```

`print(crit)` changed. `repr(crit)` did not. One object, two descriptions, two audiences.

> **For your UML:** this is the operation drawn as `+ toString(): String`. See the note at the
> end of `critter_uml.md` — you now have two Python methods and one UML name.

## Stage 7 — 🔧 Introduce two critters

One critter describing itself is useful. Two critters comparing themselves is a program.

**ADD** above `ask_for_amount`:

```python
def introduce(one, other):
    """Introduce two critters to each other."""
    print(f"{one} meets {other}.")

    if one.mood == other.mood:
        print(f"Both {one.mood}. They get on.")
    else:
        print(f"{one.name} is {one.mood} and {other.name} is {other.mood}. Awkward.")
```

**Run it:**

```
>>> a = Critter("Fluffy")
A new critter has been born!
>>> b = Critter("Spot")
A new critter has been born!
>>> introduce(a, b)
Fluffy the happy critter meets Spot the happy critter.
Both happy. They get on.
>>> for _ in range(7): b.talk()
...                                   (seven lines of talk)
>>> introduce(a, b)
Fluffy the happy critter meets Spot the frustrated critter.
Fluffy is happy and Spot is frustrated. Awkward.
```

Same call, different result, and `introduce` contains no critter names. Your `__str__` was
written once and is doing the work twice in one f-string.

Now try to compare their hunger instead of their mood:

```
>>> a.hunger
AttributeError: 'Critter' object has no attribute 'hunger'
```

`mood` is a property, so `introduce` can reach it. `_hunger` is private, so it cannot. Work out
what you would have to change, and whether you should.

## Stage 8 — 🧩 Put it in the game

`introduce` is unreachable from the menu — the game only ever makes one critter.

Add a second critter and two menu choices: introduce yours to the other one, and listen to the
other one. Both critters must age independently, so playing with one must not change the other.

No code. You have `introduce`, and `main()` already shows you how one critter is built and used.

---

# Part 3 — The Critter Farm

> **Dawson, challenge 4:** Create a Critter Farm program by instantiating several Critter
> objects and keeping track of them through a list. Mimic the Critter Caretaker program, but
> instead of requiring the user to care for a single critter, require them to care for an entire
> farm. Each menu choice should allow the user to perform some action for all of the critters
> (feed all of the critters, play with all of the critters, or listen to all of the critters).
> To make the program interesting, give each critter random starting hunger and boredom levels.

Two critters was Part 2. This is *many*, which needs a list.

**Work in a copy:** `cp critter.py farm.py`, and do Part 3 in `farm.py`.

## Stage 9 — 🔧 Critters that don't all start the same

**ADD** below the docstring:

```python
import random
```

**CHANGE** `__init__`:

```python
    def __init__(self, name, hunger=0, boredom=0):
        """Build a critter. Needs start at zero unless you say otherwise."""
        print("A new critter has been born!")
        self._name = "Critter"
        self.name = name
        self._hunger = hunger
        self._boredom = boredom
        Critter.total += 1
```

**Run it:**

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

Every call you already wrote still works, because the defaults catch what you didn't pass. Same
trick `eat(food=4)` played on you in stage 1.

## Stage 10 — 🔧 A list of critters

**ADD** above `ask_for_amount`:

```python
def make_farm():
    """Build a list of three critters with random starting needs."""
    farm = []
    for name in ["Fluffy", "Spot", "Bruiser"]:
        critter = Critter(name, random.randint(0, 5), random.randint(0, 5))
        farm.append(critter)
    return farm


def introduce_all(farm):
    """Have every critter on the farm introduce itself."""
    for critter in farm:
        print(f"This is {critter}.")


def feed_all(farm, food):
    """Feed every critter on the farm the same amount."""
    for critter in farm:
        critter.eat(food)
```

**Run it** (your numbers will differ — that is `random` working):

```
>>> farm = make_farm()
A new critter has been born!
A new critter has been born!
A new critter has been born!
>>> farm
[Critter(name='Fluffy', hunger=2, boredom=1, mood='happy'), Critter(name='Spot', hunger=3, boredom=5, mood='okay'), Critter(name='Bruiser', hunger=0, boredom=0, mood='happy')]
>>> introduce_all(farm)
This is Fluffy the happy critter.
This is Spot the okay critter.
This is Bruiser the happy critter.
>>> feed_all(farm, 5)
Fluffy eats and seems happy.
Spot eats.
Bruiser eats and seems happy.
```

Three things to account for:

1. `feed_all` gave each critter the same food and they did not all say the same thing.
2. `introduce_all` is `introduce` with the pair replaced by a loop, and you changed nothing in
   the class to get it.
3. `print(farm)` shows `__repr__` for every critter, not the `__str__` you wrote. Lists always
   use `repr` on their contents. Why would that be the right default?

## Stage 11 — 🧩 The rest of the farm

**Write `play_all` and `listen_all`.** Same shape as `feed_all`. One of them needs no amount —
work out which before you write either.

**Then rebuild `main()`** so the game is about the farm:

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

        # one branch per choice

    Critter.status()
```

Choices 2 and 3 still ask how much, through `ask_for_amount`, once for the farm. `Critter.status()`
should report 3.

The hard line is the first comment. `crit.mood` was one critter; a farm has three. Decide what one
line says about three critters — "the farm is happy" when one of them is `mad` is a program lying
to its player.

## Stage 12 — 🚀 On your own

Specification only.

1. **The player sets the farm size** and names each critter. An empty name must not produce a
   nameless critter — the class refuses one, so find out what your farm code does on a bare Enter.
2. **Feed one critter by name**, chosen from a list, as well as feeding everybody.
3. **Report honestly.** Before the menu, show how many critters are hungry, bored, or `mad`.
4. **A critter left `mad` for too long leaves the farm.** Decide what "too long" means, add
   whatever state that needs, and tell the player.

Item 4 is the only one that makes you change the Critter class rather than the farm code. Notice
how different that feels.

---

## What each stage was for

| Stage | The one new idea |
|---|---|
| 1 | a default parameter is an ability already present, not yet reachable |
| 2 | `input()` returns a string; a number has to be made from it |
| 3 | validate before you convert |
| 4 | a program that silently throws work away is not finished |
| 5 | with no `__str__`, `print()` falls back to `__repr__` |
| 6 | one object, two descriptions, two audiences |
| 7 | a function comparing two objects needs no names of its own |
| 8 | two objects of the same class, ageing independently |
| 9 | defaults let you add an ability without breaking old calls |
| 10 | a list of objects; containers print their contents with `repr` |
| 11 | reading a pattern well enough to write the next one |
| 12 | a specification, and no help |

## Check yourself

1. You fed a critter 1 food and its hunger did not move. Where did the food go?
2. Stage 3 rejects `-3` and nobody wrote a rule about negatives. Why? What about `3.5`?
3. Before stage 6, `print(crit)` already worked. What was it calling, and why is that a fallback
   rather than the answer?
4. `introduce` compares `mood` but cannot compare hunger. What does that tell you about which of
   a critter's state is part of its public interface?
5. `introduce_all` works on a farm of 3 and a farm of 300, and contains no number. Which line is
   responsible?

---

## Where this came from

The Critter Caretaker program is adapted from Mike Dawson's *Python Programming for the Absolute
Beginner*, 3rd Edition, Chapter 8. Parts 1 and 3 follow his challenges 1 and 4. Part 2 replaces
his challenge 3 for the reason given there.

Two deliberate divergences from the book: single-underscore privacy (`_mood`) rather than double,
because this class has no inheritance and so no need for name mangling; and a `__repr__` from the
start, so a critter can always describe its state in the REPL.
