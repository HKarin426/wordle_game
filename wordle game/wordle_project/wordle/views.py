import random
import string
import requests
from django.shortcuts import render, redirect
from urllib.parse import urlencode

# 1. 단어 리스트 준비
word_list = ["apple", "grape", "berry", "melon", "lemon", "mango", "watch", "crane", "blush", "flint", "glove", "jumpy", "knack", "plumb", "quash", "sword", "zesty"]

def is_valid_word(word):
    api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(api_url)
    return response.status_code == 200

def index(request):
    answer = request.GET.get('answer')
    remaining_letters = request.GET.get('remaining_letters')
    attempts = int(request.GET.get('attempts', 6))
    guesses = request.GET.getlist('guesses')
    feedbacks = request.GET.getlist('feedbacks')

    if not answer:
        answer = random.choice(word_list)
        remaining_letters = list(string.ascii_lowercase)
        attempts = 6
        guesses = []
        feedbacks = []

    if request.method == 'POST':
        guess = request.POST['guess'].lower()
        
        if len(guess) != 5:
            message = 'Please enter a 5-letter word.'
        elif not is_valid_word(guess):
            message = 'This is not a valid word.'
        else:
            feedback = []
            for i in range(5):
                if guess[i] == answer[i]:
                    feedback.append('🟢')  # 🟢: 위치와 문자가 모두 일치
                elif guess[i] in answer:
                    feedback.append('🟡')  # 🟡: 문자는 일치하나 위치가 다름
                else:
                    feedback.append('🔴')  # 🔴: 문자가 일치하지 않음

            guesses.append(guess)
            feedbacks.append(''.join(feedback))

            # 알파벳 제거 로직 수정: 단어에 없는 알파벳만 제거
            remaining_letters = list(remaining_letters)
            for letter in guess:
                if letter not in answer and letter in remaining_letters:
                    remaining_letters.remove(letter)

            attempts -= 1

            if guess == answer:
                message = 'Congratulations! You\'ve guessed the word correctly.'
            elif attempts == 0:
                message = f"Sorry, you've run out of attempts. The word was: {answer}"
            else:
                message = "Feedback: " + ''.join(feedback)

        query_params = {
            'answer': answer,
            'remaining_letters': ''.join(remaining_letters),
            'attempts': attempts,
            'guesses': guesses,
            'feedbacks': feedbacks,
            'message': message
        }
        return redirect(f'/?{urlencode(query_params, doseq=True)}')

    return render(request, 'wordle/index.html', {
        'remaining_letters': ''.join(remaining_letters),
        'attempts': attempts,
        'guesses': zip(guesses, feedbacks),
        'message': request.GET.get('message', '')
    })
