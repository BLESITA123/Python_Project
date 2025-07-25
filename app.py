from flask import Flask, render_template, session, request, jsonify
import random

app = Flask(__name__)
app.secret_key = 'simple_game_key'

@app.route('/')
def home():
    session['score'] = {'won': 0, 'lost': 0, 'draw': 0, 'attempts': 0}
    return render_template('index.html')

@app.route('/play', methods=['POST'])
def play():
    data = request.get_json()
    player_choice = data.get("player_choice", "").upper()
    choices = ["ROCK", "PAPER", "SCISSORS"]
    emoji = {"ROCK": "✊", "PAPER": "✋", "SCISSORS": "✌️"}

    if player_choice not in choices:
        return jsonify({"error": "Invalid choice"}), 400

    score = session.get('score', {'won': 0, 'lost': 0, 'draw': 0, 'attempts': 0})

    if score['attempts'] >= 5:
        return jsonify({
            "message": "Game already over.",
            "game_over": True,
            "score": score,
            "winner": decide_winner(score)
        })

    computer_choice = random.choice(choices)

    if player_choice == computer_choice:
        result = "Draw"
        score['draw'] += 1
    elif (player_choice == "ROCK" and computer_choice == "SCISSORS") or \
         (player_choice == "PAPER" and computer_choice == "ROCK") or \
         (player_choice == "SCISSORS" and computer_choice == "PAPER"):
        result = "You Win!"
        score['won'] += 1
    else:
        result = "You Lose!"
        score['lost'] += 1

    score['attempts'] += 1
    session['score'] = score

    return jsonify({
        "player": emoji[player_choice],
        "computer": emoji[computer_choice],
        "result": result,
        "score": score,
        "game_over": score['attempts'] >= 5,
        "winner": decide_winner(score) if score['attempts'] >= 5 else None
    })

@app.route('/restart', methods=['POST'])
def restart():
    session['score'] = {'won': 0, 'lost': 0, 'draw': 0, 'attempts': 0}
    return jsonify({"message": "Game restarted!"})

def decide_winner(score):
    if score['won'] > score['lost']:
        return "🎉 You are the Winner!"
    elif score['won'] < score['lost']:
        return "💻 Computer Wins!"
    else:
        return "🤝 It's a Draw!"

if __name__ == '__main__':
    app.run(debug=True)
