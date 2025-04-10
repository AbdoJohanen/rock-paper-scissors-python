from flask import Flask, render_template, request, redirect, url_for, session
import random

# Set up Flask app and configure static folder (which holds your SVGs)
app = Flask(__name__, static_folder='assets')
app.secret_key = 'my_simple_development_key'

@app.route('/', methods=['GET', 'POST'])
def index():
    # Initialize scores in the session if they are not present
    if 'player_score' not in session:
        session['player_score'] = 0
    if 'computer_score' not in session:
        session['computer_score'] = 0

    last_round = False
    round_result = ''
    player_move = ''
    computer_move = ''
    player_move_image = ''
    computer_move_image = ''
    game_over = session.get('player_score') == 2 or session.get('computer_score') == 2
    winner = ''

    if request.method == 'POST' and not game_over:
        player_move = request.form.get('move')
        moves = ['rock', 'paper', 'scissors']
        computer_move = random.choice(moves)

        # Determine the outcome of the round
        if player_move == computer_move:
            round_result = "It's a tie!"
        elif (player_move == 'rock' and computer_move == 'scissors') or \
             (player_move == 'scissors' and computer_move == 'paper') or \
             (player_move == 'paper' and computer_move == 'rock'):
            round_result = "Player wins the round!"
            session['player_score'] = session.get('player_score') + 1
        else:
            round_result = "Computer wins the round!"
            session['computer_score'] = session.get('computer_score') + 1

        last_round = True

        # Map moves to their corresponding SVG file paths
        image_map = {
            "rock": url_for('static', filename='rock.svg'),
            "paper": url_for('static', filename='paper.svg'),
            "scissors": url_for('static', filename='scissors.svg')
        }
        player_move_image = image_map.get(player_move, '')
        computer_move_image = image_map.get(computer_move, '')

        game_over = session.get('player_score') == 2 or session.get('computer_score') == 2
        if game_over:
            winner = "Player" if session.get('player_score') == 2 else "Computer"

    if game_over and not winner:
        winner = "Player" if session.get('player_score') == 2 else "Computer"

    return render_template(
        'index.html', 
        player_score=session.get('player_score'),
        computer_score=session.get('computer_score'),
        round_result=round_result,
        player_move=player_move,
        computer_move=computer_move,
        last_round=last_round,
        game_over=game_over,
        winner=winner,
        player_move_image=player_move_image,
        computer_move_image=computer_move_image
    )

@app.route('/reset', methods=['POST'])
def reset():
    session.pop('player_score', None)
    session.pop('computer_score', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
