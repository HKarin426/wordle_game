# views.py
from django.shortcuts import render
import random
import string
import requests

word_list = ["apple", "grape", "berry", "melon", "lemon", "mango", "watch", "crane", "blush", "flint", "glove", "jumpy", "knack", "plumb", "quash", "sword", "zesty"]

remaining_letters = list(string.ascii_lowercase)
answer = random.choice(word_list)
attempts = 6
guesses = []

letter_status = {letter: 'unused' for letter in remaining_letters}

def is_valid_word(word):
    api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(api_url)
    return response.status_code == 200

def index(request):
    global remaining_letters, answer, attempts, guesses, letter_status

    if request.method == 'POST':
        if 'guess' in request.POST:
            guess = request.POST['guess'].lower()
            
            if len(guess) != 5:
                return render(request, 'wordle/index.html', {
                    'message': 'Please enter a 5-letter word.',
                    'remaining_letters': remaining_letters,
                    'attempts': attempts,
                    'guesses': guesses,
                    'letter_status': letter_status,
                })

            if not is_valid_word(guess):
                return render(request, 'wordle/index.html', {
                    'message': 'This is not a valid word.',
                    'remaining_letters': remaining_letters,
                    'attempts': attempts,
                    'guesses': guesses,
                    'letter_status': letter_status,
                })

            if guess == answer:
                feedback = ''.join([f'<span class="correct">{guess[i]}</span>' for i in range(5)])
                guesses.append({'guess': guess, 'feedback': feedback})
                return render(request, 'wordle/index.html', {
                    'message': f'Congratulations! You\'ve guessed the word correctly: {guess}',
                    'remaining_letters': remaining_letters,
                    'attempts': attempts,
                    'guesses': guesses,
                    'letter_status': letter_status,
                })
            else:
                feedback = []
                correct_letters = set()
                for i in range(5):
                    if guess[i] == answer[i]:
                        feedback.append(f'<span class="correct">{guess[i]}</span>')  # 🟢: 위치와 문자가 모두 일치
                        correct_letters.add(guess[i])
                        letter_status[guess[i]] = 'correct'
                    elif guess[i] in answer:
                        feedback.append(f'<span class="partial">{guess[i]}</span>')  # 🟡: 문자는 일치하나 위치가 다름
                        correct_letters.add(guess[i])
                        if letter_status[guess[i]] != 'correct':
                            letter_status[guess[i]] = 'partial'
                    else:
                        feedback.append(f'<span class="wrong">{guess[i]}</span>')  # ⚫: 문자가 일치하지 않음
                        letter_status[guess[i]] = 'wrong'

                attempts -= 1
                guesses.append({'guess': guess, 'feedback': ''.join(feedback)})
                if attempts == 0:
                    message = f"Sorry, you've run out of attempts. The word was: {answer}"
                    answer = random.choice(word_list)  # 새로운 게임을 위해 단어 재설정
                    attempts = 6  # 시도 횟수 재설정
                    remaining_letters = list(string.ascii_lowercase)  # 남은 알파벳 재설정
                    guesses = []  # 입력 내역 초기화
                    letter_status = {letter: 'unused' for letter in remaining_letters}  # 알파벳 상태 재설정
                else:
                    message = ""

                return render(request, 'wordle/index.html', {
                    'message': message,
                    'remaining_letters': remaining_letters,
                    'attempts': attempts,
                    'guesses': guesses,
                    'letter_status': letter_status,
                })

        elif 'reset' in request.POST:
            answer = random.choice(word_list)
            attempts = 6
            remaining_letters = list(string.ascii_lowercase)
            guesses = []
            letter_status = {letter: 'unused' for letter in remaining_letters}
            return redirect('index')
    
    return render(request, 'wordle/index.html', {
        'remaining_letters': remaining_letters,
        'attempts': attempts,
        'guesses': guesses,
        'letter_status': letter_status,
    })