import random

class Banana:
    def __init__(self):
        self.mood = random.choice(["confused", "horizontal", "legendary"])

    def calculate_gravity(self):
        return 0 if self.mood == "horizontal" else 9.81

if __name__ == "__main__":
    banana = Banana()
    print(f"Banana mood: {banana.mood}")
    print(f"Gravity: {banana.calculate_gravity()}")
