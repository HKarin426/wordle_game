import random
import string
import requests
from django.shortcuts import render

# 1. 단어 리스트 준비
word_list = ["apple", "grape", "berry", "melon", "lemon", "mango","watch","crane", "blush", "flint", "glove", "jumpy", "knack", "plumb", "quash", "sword", "zesty"]

# 남은 알파벳 초기화
remaining_letters = list(string.ascii_lowercase)
answer = random.choice(word_list)
attempts = 6
guesses = []

def is_valid_word(word):
    api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(api_url)
    return response.status_code == 200

def index(request):
    global remaining_letters, answer, attempts, guesses

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

        if guess == answer:
            guesses.append({'guess': guess, 'feedback': '🟢🟢🟢🟢🟢'})
            return render(request, 'wordle/index.html', {
                'message': f'Congratulations! You\'ve guessed the word correctly: {guess}',
                'remaining_letters': ''.join(remaining_letters),
                'attempts': attempts,
                'guesses': guesses,
            })
        else:
            feedback = []
            correct_letters = set()
            for i in range(5):
                if guess[i] == answer[i]:
                    feedback.append('🟢')  # 🟢: 위치와 문자가 모두 일치
                    correct_letters.add(guess[i])
                elif guess[i] in answer:
                    feedback.append('🟡')  # 🟡: 문자는 일치하나 위치가 다름
                    correct_letters.add(guess[i])
                else:
                    feedback.append('🔴')  # 🔴: 문자가 일치하지 않음

            # 사용된 문자를 남은 알파벳에서 제거 (단, 정답에 들어가는 알파벳은 제거하지 않음)
            for letter in guess:
                if letter not in correct_letters and letter in remaining_letters:
                    remaining_letters.remove(letter)
            
            attempts -= 1
            guesses.append({'guess': guess, 'feedback': ''.join(feedback)})
            if attempts == 0:
                message = f"Sorry, you've run out of attempts. The word was: {answer}"
                answer = random.choice(word_list)  # 새로운 게임을 위해 단어 재설정
                attempts = 6  # 시도 횟수 재설정
                remaining_letters = list(string.ascii_lowercase)  # 남은 알파벳 재설정
                guesses = []  # 입력 내역 초기화
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
