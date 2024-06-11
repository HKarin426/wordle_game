import random
import string
import requests
from django.shortcuts import render, redirect

# 1. 단어 리스트 준비
word_list = ["apple", "grape", "berry", "melon", "lemon", "mango", "watch", "crane", "blush", "flint", "glove", "jumpy", "knack", "plumb", "quash", "sword", "zesty"]

# 남은 알파벳 초기화
remaining_letters = list(string.ascii_lowercase)  # 알파벳 소문자 리스트
answer = random.choice(word_list)  # 정답 단어를 랜덤으로 선택
attempts = 6  # 사용자에게 주어진 시도 횟수
guesses = []  # 사용자가 입력한 단어들과 피드백을 저장하는 리스트
game_over = False  # 게임 종료 상태를 나타내는 변수

# 단어가 유효한지 검사하는 함수
def is_valid_word(word):
    api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(api_url)
    return response.status_code == 200

def index(request):
    global remaining_letters, answer, attempts, guesses, game_over

    if request.method == 'POST':  # POST 요청일 때
        if 'guess' in request.POST and not game_over:
            guess = request.POST['guess'].lower()  # 입력된 단어를 소문자로 변환
            
            if len(guess) != 5:  # 단어 길이가 5자가 아니면 에러 메시지 반환
                return render(request, 'wordle/index.html', {
                    'message': '5개의 알파벳을 사용하는 단어를 입력해주세요.',
                    'remaining_letters': ''.join(remaining_letters),
                    'attempts': attempts,
                    'guesses': guesses,
                    'game_over': game_over
                })

            if not is_valid_word(guess):  # 단어가 유효하지 않으면 에러 메시지 반환
                return render(request, 'wordle/index.html', {
                    'message': '존재하지 않는 단어입니다.',
                    'remaining_letters': ''.join(remaining_letters),
                    'attempts': attempts,
                    'guesses': guesses,
                    'game_over': game_over
                })

            if guess == answer:  # 사용자가 정답을 맞춘 경우
                feedback = ''.join([f'<span class="correct">{guess[i]}</span>' for i in range(5)])
                guesses.append({'guess': guess, 'feedback': feedback})
                game_over = True  # 게임 종료 상태로 설정
                return render(request, 'wordle/index.html', {
                    'message': f'축하합니다! 정답을 맞추셨습니다. 정답은 {guess} 입니다.',
                    'remaining_letters': ''.join(remaining_letters),
                    'attempts': attempts,
                    'guesses': guesses,
                    'game_over': game_over
                })
            else:
                feedback = []
                correct_letters = set()
                for i in range(5):
                    if guess[i] == answer[i]:
                        feedback.append(f'<span class="correct">{guess[i]}</span>')  # 🟢: 위치와 문자가 모두 일치
                        correct_letters.add(guess[i])
                    elif guess[i] in answer:
                        feedback.append(f'<span class="partial">{guess[i]}</span>')  # 🟡: 문자는 일치하나 위치가 다름
                        correct_letters.add(guess[i])
                    else:
                        feedback.append(f'<span class="wrong">{guess[i]}</span>')  # 🔴: 문자가 일치하지 않음

                # 사용된 문자를 남은 알파벳에서 제거 (단, 정답에 들어가는 알파벳은 제거하지 않음)
                for letter in guess:
                    if letter not in correct_letters and letter in remaining_letters:
                        remaining_letters.remove(letter)
                
                attempts -= 1  # 시도 횟수 감소
                guesses.append({'guess': guess, 'feedback': ''.join(feedback)})  # 사용자의 입력과 피드백을 리스트에 추가
                if attempts == 0:  # 시도 횟수가 모두 소진된 경우
                    message = f"아쉽지만 모든 시도 횟수를 소진하셨습니다. 정답은 {answer} 입니다."
                    game_over = True  # 게임 종료 상태로 설정
                else:
                    message = ""

                return render(request, 'wordle/index.html', {
                    'message': message,
                    'remaining_letters': ''.join(remaining_letters),
                    'attempts': attempts,
                    'guesses': guesses,
                    'game_over': game_over
                })

        elif 'reset' in request.POST:  # 게임을 다시 시작할 때
            answer = random.choice(word_list)
            attempts = 6
            remaining_letters = list(string.ascii_lowercase)
            guesses = []
            game_over = False  # 게임 종료 상태 해제
            return redirect('index')
    
    return render(request, 'wordle/index.html', {  # GET 요청일 때
        'remaining_letters': ''.join(remaining_letters),
        'attempts': attempts,
        'guesses': guesses,
        'game_over': game_over
    })
