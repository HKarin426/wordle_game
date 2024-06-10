from django.shortcuts import render

# Create your views here.
from Flask import Flask, request, jsonify, render_template_string
import random

app = Flask(__name__)

word_list = ["apple", "berry", "charm", "delta", "eagle"]
answer = random.choice(word_list)

def check_guess(guess, answer):
    result = ['_'] * len(answer)
    for i in range(len(guess)):
        if guess[i] == answer[i]:
            result[i] = guess[i].upper()
        elif guess[i] in answer:
            result[i] = guess[i].lower()
    return ''.join(result)

@app.route('/', methods=['GET', 'POST'])
def index():
    global answer
    if request.method == 'POST':
        guess = request.form['input_text'].lower()
        if guess == answer:
            response = f"Congratulations! You've guessed the word: {answer.upper()}"
            answer = random.choice(word_list)  # 새 게임 시작
        else:
            response = check_guess(guess, answer)
        return jsonify(response)
    return render_template_string(open('template.html').read())

if __name__ == '__main__':
    app.run(debug=True)

# 게임 시작
#wordle()

# output 값 : 1. 6번의 기회가 있다. 못 맞추면 sorry ~~~ 문구가 쳐진다.
            #2. index(순번)이 틀리면 소문자로 보여지고, 순번이 맞으면 대문자로 보여진다
            #3. 6번 input 값내로 성공하면 Congratulations! You've guessed the word: 문구가 뜬다.
