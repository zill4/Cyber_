import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Game State
# Player's hit points, at 0 player is dead
player_hp = 10
# Player's name
player_name = 'John'
# Player's class
player_class = 'Warlock'
# Player's Abilities, name of ability, effect, and damage 
Player_abs = [
    {'name': 'Eldritch Blast', 'damage': 3, 'effect': 'Shoots a bolt of dark magic from the users palm.'},
    {'name': 'Mage Hand', 'damage': 1, 'effect': 'The user telepathically controls an ethereal hand for a short time.'}
]
# Enemies
Enemies = [
    {'name': 'Boar', 'abilities': [
        {'name': 'Ram', 'damage': 4, 'effect': 'Rams into target at great speed.'}
    ]}
]

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        animal = request.form["animal"]
        nPrompt = """Given the game state and the player's response what happens next
Game State
turn: 1
Player's hit points, at 0 player is dead
player_hp = 10
Player's name
player_name = 'John'
Player's class
player_class = 'Warlock'
Player's Abilities, name of ability, effect, and damage 
Player_abs = [
    {name: 'Eldritch Blast', damage: 3, effect: 'Shoots a bolt of dark magic from the users palm.'},
    {name: 'Mage Hand', damage: 1, effect: 'The user telepathically controls an ethereal hand for a short time.'}
]
Enemies
Enemies = [
    {name: 'Boar', abilities: [
        {name: 'Ram', damage: 4, effect: 'Rams into target at great speed.'}
    ]}
]
Player Response: """ + animal
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=nPrompt,
            max_tokens=100,
            temperature=0.6,
        )
        print(nPrompt)
        print(response.choices)
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(animal):
    return """Given the game state and the player's response what happens next
Game State
turn: 1
Player's hit points, at 0 player is dead
player_hp = 10
Player's name
player_name = 'John'
Player's class
player_class = 'Warlock'
Player's Abilities, name of ability, effect, and damage 
Player_abs = [
    {name: 'Eldritch Blast', damage: 3, effect: 'Shoots a bolt of dark magic from the users palm.'},
    {name: 'Mage Hand', damage: 1, effect: 'The user telepathically controls an ethereal hand for a short time.'}
]
Enemies
Enemies = [
    {name: 'Boar', abilities: [
        {name: 'Ram', damage: 4, effect: 'Rams into target at great speed.'}
    ]}
]
Player Response: {}""".format(
        animal.capitalize()
    )
