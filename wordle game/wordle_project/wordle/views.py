pip install request

import random
import string
import requests
from django.shortcuts import render, redirect

# 1. 단어 리스트 준비
word_list = ["apple", "grape", "berry", "melon", "lemon", "mango", "watch", "crane", "blush", "flint", "glove", "jumpy", "knack", "plumb", "quash", "sword", "zesty"]

def is_valid_word(word):
    # Dictionary API를 통해 단어의 유효성을 확인합니다.
    api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(api_url)
    return response.status_code == 200

def index(request):
    if 'remaining_letters' not in request.session:
        request.session['remaining_letters'] = list(string.ascii_lowercase)
        request.session['answer'] = random.choice(word_list)
        request.session['attempts'] = 6
        request.session['guesses'] = []

    remaining_letters = request.session['remaining_letters']
    answer = request.session['answer']
    attempts = request.session['attempts']
    guesses = request.session['guesses']

    if request.method == 'POST':
        guess = request.POST['guess'].lower()

        if len(guess) != 5:
            return render(request, 'wordle/index.html', {
                'message': 'Please enter a 5-letter word.',
                'remaining_letters': ''.join(remaining_letters),
                'attempts': attempts,
                'guesses': guesses,
            })
        
        if not is_valid_word(guess):
            return render(request, 'wordle/index.html', {
                'message': 'This is not a valid word.',
                'remaining_letters': ''.join(remaining_letters),
                'attempts': attempts,
                'guesses': guesses,
            })

        feedback = []
        for i in range(5):
            if guess[i] == answer[i]:
                feedback.append('🟢')  # 🟢: 위치와 문자가 모두 일치
            elif guess[i] in answer:
                feedback.append('🟡')  # 🟡: 문자는 일치하나 위치가 다름
            else:
                feedback.append('🔴')  # 🔴: 문자가 일치하지 않음

        guesses.append({'guess': guess, 'feedback': ''.join(feedback)})

        # 알파벳 제거 로직 수정: 단어에 없는 알파벳만 제거
        for letter in guess:
            if letter not in answer and letter in remaining_letters:
                remaining_letters.remove(letter)

        attempts -= 1
        request.session['remaining_letters'] = remaining_letters
        request.session['attempts'] = attempts
        request.session['guesses'] = guesses

        if guess == answer:
            message = 'Congratulations! You\'ve guessed the word correctly.'
            request.session.flush()  # 게임 상태 초기화
        elif attempts == 0:
            message = f"Sorry, you've run out of attempts. The word was: {answer}"
            request.session.flush()  # 게임 상태 초기화
        else:
            message = "Feedback: " + ''.join(feedback)

        return render(request, 'wordle/index.html', {
            'message': message,
            'remaining_letters': ''.join(remaining_letters),
            'attempts': attempts,
            'guesses': guesses,
        })

    return render(request, 'wordle/index.html', {
        'remaining_letters': ''.join(remaining_letters),
        'attempts': attempts,
        'guesses': guesses,
    })
