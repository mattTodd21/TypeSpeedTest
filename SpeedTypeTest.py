import sys
import time
import random
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit

class TypingTest(QWidget):
    def __init__(self):
        super().__init__()
        self.levelSentences = {
            1: ["apple", "truth", "world", "happy", "light", "butterfly", 
                "laughter", "ocean", "guitar", "dream", "mountain", "laughter", 
                "adventure", "wonder", "sunset", "whisper", "blossom", "freedom", 
                "serenity", "chocolate", "journey", "sapphire", "carousel", "laughter", 
                "reflection", "tranquil", "silhouette", "harmony", "garden", "infinity",
                "imagination", "moonlight", "melody", "inspiration", "sunset", "twilight", 
                "waterfall", "embrace", "enchanted", "firefly", "silence", "wanderlust"],
            2: ["The quick fox.", "Jump high above.", "Rain falls softly.", 
                "Birds sing sweetly.", "Green grass grows.", "The sun shines.", 
                "Music soothes souls.", "Laughter brings joy.", "Time heals everything.", 
                "Birds chirp loudly.", "Rainbows appear magically.", "Whispers carry secrets.",
                "Snowflakes fall silently.", "Winds howl fiercely.", "Fireflies dance gracefully.",
                "Stars twinkle brightly.", "Ocean waves crash.", "Autumn leaves fall.", 
                "Children laugh gleefully.", "Mountains stand tall.", "Night descends slowly.", 
                "Flowers bloom beautifully.", "Breezes whisper softly.", "Rivers flow calmly.", 
                "Dreams inspire creativity."],
            3: ["Life is a beautiful journey.", "The sun rises in the east.", 
                "Never stop dreaming big.", "Hard work pays off always.", 
                "Nature is a great teacher.", "Dreams shape the future's reality.", 
                "Laughter is the best medicine.", "Change starts with a single step.", 
                "Courage leads to the stars.", "Art reflects life's true colors.", 
                "Music heals the deepest wounds.", "Kindness creates an endless ripple.", 
                "Books are gateways to worlds.", "Adventure awaits the brave soul.", 
                "Hope shines brightest in darkness."],
            4: ["The early bird catches the worm every day.", 
                "A journey of a thousand miles begins with a single step.", 
                "Every moment is a fresh beginning.", 
                "Believe you can and you're halfway there.", 
                "Act as if what you do makes a difference."]
        }
        self.usedSentences = {level: set() for level in self.levelSentences}
        self.currentLevel = 1
        self.successfulTests = 0
        self.initUI()

    def initUI(self):
        self.currentTestSentence = self.getNextSentence()
        self.startTime = 0

        self.layout = QVBoxLayout()

        self.levelLabel = QLabel(f"Level: {self.currentLevel}", self)
        self.layout.addWidget(self.levelLabel)

        self.instructionsLabel = QLabel("Press ENTER to start the timer, then type the setence and press ENTER to check your score!", self)
        self.layout.addWidget(self.instructionsLabel)

        self.textLabel = QLabel(self.currentTestSentence, self)
        self.layout.addWidget(self.textLabel)

        self.entry = QLineEdit(self)
        self.entry.setReadOnly(True)
        self.layout.addWidget(self.entry)

        self.entry.returnPressed.connect(self.endTest)

        self.resultLabel = QLabel('', self)
        self.layout.addWidget(self.resultLabel)

        self.setLayout(self.layout)
        self.setWindowTitle('Typing Speed Test')
        self.show()

    def getNextSentence(self):
        availableSentences = set(self.levelSentences[self.currentLevel]) - self.usedSentences[self.currentLevel]
        if not availableSentences:
            self.usedSentences[self.currentLevel] = set()  # Reset used sentences for the level
            availableSentences = set(self.levelSentences[self.currentLevel])
        
        sentence = random.choice(list(availableSentences))
        self.usedSentences[self.currentLevel].add(sentence)
        return sentence

    def startTest(self):
        self.startTime = time.time()
        self.entry.setReadOnly(False)

    def endTest(self):
        if self.startTime == 0:
            self.startTest()
            return

        endTime = time.time()
        userInput = self.entry.text()
        if userInput != self.currentTestSentence:
            self.resultLabel.setText("Incorrect sentence. Starting over at Level 1.")
            self.currentLevel = 1
            self.successfulTests = 0
            self.usedSentences = {level: set() for level in self.levelSentences}  # Reset all used sentences
        else:
            self.successfulTests += 1
            if self.successfulTests >= 5:
                if self.currentLevel < 4:
                    self.currentLevel += 1
                    self.successfulTests = 0
                    self.resultLabel.setText(f"Congratulations! You've advanced to Level {self.currentLevel}!")
                    # Reset used sentences for the new level
                    self.usedSentences[self.currentLevel] = set()
                else:
                    self.resultLabel.setText("You have completed the highest level. Well done!")
            else:
                charCount = len(userInput.replace(" ", ""))
                timeElapsed = endTime - self.startTime
                wpm = (charCount / 5) / (timeElapsed / 60)
                self.resultLabel.setText(f"Your typing speed: {wpm:.2f} WPM. Successful tests at this level: {self.successfulTests}")

        # Reset for a new test
        self.currentTestSentence = self.getNextSentence()
        self.textLabel.setText(self.currentTestSentence)
        self.levelLabel.setText(f"Level: {self.currentLevel}")
        self.entry.clear()
        self.startTime = 0
        self.entry.setReadOnly(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TypingTest()
    sys.exit(app.exec_())
