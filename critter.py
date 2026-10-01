"""
Critter Caretaker — the finished program.

A virtual pet. You name it, and then you listen to it, feed it, and play with
it. If you ignore it, it gets hungry and bored, and its mood tells you so.

This is the starting point, not the destination. README.md asks you to extend
it, one stage at a time.

Adapted from the Critter Caretaker program in Mike Dawson's
"Python Programming for the Absolute Beginner" (3rd Edition), Chapter 8.

Run it:        python3 critter.py
Poke at it:    python3 -i critter.py
"""


class Critter(object):
    """A virtual pet with a name, two needs, and a mood that follows from them."""

    total = 0  # CLASS attribute: shared by every critter ever made

    def __init__(self, name):
        """Build a critter: give it a name, and start it off content."""
        print("A new critter has been born!")
        self._name = "Critter"  # a fallback, so the setter below has something to keep
        self.name = name        # assigning through the property means it gets checked
        self._hunger = 0
        self._boredom = 0
        Critter.total += 1

    def __repr__(self):
        """How the critter looks to a programmer: raw state, exact values.

        This is what you see in the REPL when you type a critter's name on its
        own. mood is in here even though nothing stores it, so you can watch a
        computed value sitting next to the numbers it was computed from.
        """
        return (
            f"Critter(name={self.name!r}, hunger={self._hunger}, "
            f"boredom={self._boredom}, mood={self.mood!r})"
        )

    @property
    def name(self):
        """Property getter: hand back the name."""
        return self._name

    @name.setter
    def name(self, new_name):
        """Property setter: refuse an empty name instead of storing one."""
        if new_name == "":
            print(f"A critter's name can't be empty. Staying {self._name!r}.")
        else:
            self._name = new_name

    @property
    def mood(self):
        """Computed property: worked out from hunger and boredom, never stored."""
        unhappiness = self._hunger + self._boredom

        if unhappiness < 5:
            return "happy"
        elif unhappiness <= 10:
            return "okay"
        elif unhappiness <= 15:
            return "frustrated"
        else:
            return "mad"

    def _pass_time(self):
        """Private helper: time passing makes a critter hungrier and more bored."""
        self._hunger += 1
        self._boredom += 1

    def talk(self):
        """Critter tells you how it feels. Time passes."""
        print(f"{self._name} says: I feel {self.mood} right now.")
        self._pass_time()

    def eat(self, food=4):
        """Critter eats, reducing hunger. Time passes."""
        self._hunger -= food
        if self._hunger < 0:
            self._hunger = 0

        if self.mood == "happy":
            print(f"{self._name} eats and seems happy.")
        else:
            print(f"{self._name} eats.")

        self._pass_time()

    def play(self, fun=4):
        """Critter plays, reducing boredom. Time passes."""
        self._boredom -= fun
        if self._boredom < 0:
            self._boredom = 0

        if self.mood == "happy":
            print(f"{self._name} plays and laughs!")
        else:
            print(f"{self._name} plays.")

        self._pass_time()

    @staticmethod
    def status():
        """Static method: called on the class, because it isn't about any one critter."""
        print(f"\nThe total number of critters is: {Critter.total}")


def main():
    """Ask for a name, then run the menu until the player quits."""
    crit_name = input("What do you want to name your critter?: ")
    crit = Critter(crit_name)

    choice = None
    while choice != "0":
        print(f"\n{crit.name} is {crit.mood}.")
        print(
            "\n0 - Quit"
            "\n1 - Listen to your critter"
            "\n2 - Feed your critter"
            "\n3 - Play with your critter"
        )

        choice = input("\nChoice: ")

        if choice == "0":
            print(f"\nGoodbye from {crit.name}!")
        elif choice == "1":
            crit.talk()
        elif choice == "2":
            crit.eat()
        elif choice == "3":
            crit.play()
        else:
            print(f"\nSorry, but {choice} isn't a valid choice.")

    Critter.status()


if __name__ == "__main__":
    main()
