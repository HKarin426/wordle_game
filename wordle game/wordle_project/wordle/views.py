import random
import string
from django.shortcuts import render

# 1. 단어 리스트 준비
word_list = ["apple", "grape", "berry", "melon", "lemon", "mango"]

# 남은 알파벳 초기화
remaining_letters = list(string.ascii_lowercase)
answer = random.choice(word_list)
attempts = 6

def index(request):
    global remaining_letters, answer, attempts

    if request.method == 'POST':
        guess = request.POST['guess'].lower()
        
        if len(guess) != 5:
            return render(request, 'wordle/index.html', {
                'message': 'Please enter a 5-letter word.',
                'remaining_letters': ''.join(remaining_letters),
                'attempts': attempts,
            })

        if guess == answer:
            return render(request, 'wordle/index.html', {
                'message': 'Congratulations! You\'ve guessed the word correctly.',
                'remaining_letters': ''.join(remaining_letters),
                'attempts': attempts,
            })
        else:
            feedback = []
            for i in range(5):
                if guess[i] == answer[i]:
                    feedback.append('G')  # G는 Green: 위치와 문자가 모두 일치
                elif guess[i] in answer:
                    feedback.append('Y')  # Y는 Yellow: 문자는 일치하나 위치가 다름
                else:
                    feedback.append('B')  # B는 Black: 문자가 일치하지 않음

            # 사용된 문자를 남은 알파벳에서 제거
            for letter in guess:
                if letter in remaining_letters:
                    remaining_letters.remove(letter)
            
            attempts -= 1
            if attempts == 0:
                message = f"Sorry, you've run out of attempts. The word was: {answer}"
                answer = random.choice(word_list)  # 새로운 게임을 위해 단어 재설정
                attempts = 6  # 시도 횟수 재설정
                remaining_letters = list(string.ascii_lowercase)  # 남은 알파벳 재설정
            else:
                message = "Feedback: " + ''.join(feedback)

            return render(request, 'wordle/index.html', {
                'message': message,
                'remaining_letters': ''.join(remaining_letters),
                'attempts': attempts,
            })
    
    return render(request, 'wordle/index.html', {
        'remaining_letters': ''.join(remaining_letters),
        'attempts': attempts,
    })
