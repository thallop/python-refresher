"""
Tutorial: Geography quiz
This script reads a CSV file of countries and capitals and quizzes the user on either 'country >> capital' or 'capital >> country'.
"""

import sys
import random

n = int(sys.argv[1])

reverse_mode = len(sys.argv) > 2 and sys.argv[2].lower() == "inv"

countries = []
capitals = []

with open("capitals.csv", "r", encoding="utf-8") as f:
    for line in f:
        data = line.strip().split(",")
        if len(data) == 2:
            country = data[0].split("(")[0].strip()
            capital = data[1].strip()
            countries.append(country)
            capitals.append(capital)

questions = list(zip(countries, capitals))
random.shuffle(questions)

score = 0

for i, (country, capital) in enumerate(questions[:n], 1):
    if not reverse_mode:
        answer = input(f"Question {i}: What is the capital of {country}? ")
        correct_answer = capital
    else:
        answer = input(f"Question {i}: Which country has {capital} as its capital? ")
        correct_answer = country

    if answer.strip().lower() == correct_answer.strip().lower():
        print("Correct!\n")
        score += 1
    else:
        print(f"Wrong. The correct answer was {correct_answer}.\n")

print(f"Final score: {score}/{n} ({score / n * 100:.0f}%)")