class Chore:

    def __init__(self, desc, explanation, frequency, locked_day):
        self.desc = desc
        self.explanation = explanation
        self.frequency = frequency
        if locked_day.lower() == "any":
            self.locked_day = None
        else:
            self.locked_day = locked_day

    def __repr__(self):
        if self.locked_day is None:
            return self.desc + ": " + self.explanation + " on a " + str(self.frequency) + " basis, priority "
        else:
            return self.desc + ": " + self.explanation + " on a " + str(self.frequency) + " basis, priority " + " on " + str(self.locked_day)