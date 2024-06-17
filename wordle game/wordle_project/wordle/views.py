<<<<<<< HEAD
import random
import string
import requests
import re
import pdfplumber
from django.shortcuts import render, redirect
import pandas as pd

# 1. 단어 리스트 준비
    
# 엑셀 파일 경로
file_path = r'C:\Users\user\Documents\bigdata\wordle_game-1\wordle game\wordle_project\word\master_1.xlsx'
# 엑셀 파일을 데이터프레임으로 읽어오기
df = pd.read_excel(file_path, engine='openpyxl', header=None)
# DataFrame을 리스트로 변환 후 평탄화
word_list = df.values.flatten().tolist()

# 남은 알파벳 초기화
qwerty = ['q','w','e','r','t','y','u','i','o','p','a','s','d','f','g','h','j','k','l','z','x','c','v','b','n','m']  # qwerty 배열
remaining_letters = qwerty
answer = random.choice(word_list)  # 정답 단어를 랜덤으로 선택
attempts = 6  # 사용자에게 주어진 시도 횟수
guesses = []  # 사용자가 입력한 단어들과 피드백을 저장하는 리스트
game_over = False  # 게임 종료 상태를 나타내는 변수
letter_status = {letter: 'unused' for letter in remaining_letters}

# 단어가 유효한지 검사하는 함수
def is_valid_word(word):
    api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(api_url)
    return response.status_code == 200

def index(request):
    global remaining_letters, answer, attempts, guesses, game_over, letter_status

    if request.method == 'POST':  # POST 요청일 때
        if 'guess' in request.POST and not game_over:
            guess = request.POST['guess'].lower()  # 입력된 단어를 소문자로 변환
            
            if len(guess) != 5:  # 단어 길이가 5자가 아니면 에러 메시지 반환
                return render(request, 'wordle/index.html', {
                    'message': '5개의 알파벳을 사용하는 단어를 입력해주세요.',
                    'remaining_letters': remaining_letters,
                    'attempts': attempts,
                    'guesses': guesses,
                    'game_over': game_over,
                    'letter_status': letter_status
                })

            if not is_valid_word(guess) and guess not in word_list: # 단어가 유효하지 않으면 에러 메시지 반환
                return render(request, 'wordle/index.html', {
                    'message': '존재하지 않는 단어입니다.',
                    'remaining_letters': remaining_letters,
                    'attempts': attempts,
                    'guesses': guesses,
                    'game_over': game_over,
                    'letter_status': letter_status,
                })

            if guess == answer:  # 사용자가 정답을 맞춘 경우
                feedback = ''.join([f'<span class="correct">{guess[i]}</span>' for i in range(5)])
                guesses.append({'guess': guess, 'feedback': feedback})
                game_over = True  # 게임 종료 상태로 설정
                return render(request, 'wordle/index.html', {
                    'message': f'축하합니다! 정답을 맞추셨습니다. 정답은 {guess} 입니다.',
                    'remaining_letters': remaining_letters,
                    'attempts': attempts,
                    'guesses': guesses,
                    'game_over': game_over,
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
                 
                attempts -= 1  # 시도 횟수 감소
                guesses.append({'guess': guess, 'feedback': ''.join(feedback)})  # 사용자의 입력과 피드백을 리스트에 추가
                if attempts == 0:  # 시도 횟수가 모두 소진된 경우
                    message = f"아쉽지만 모든 시도 횟수를 소진하셨습니다. 정답은 {answer} 입니다."
                    answer = random.choice(word_list)  # 새로운 게임을 위해 단어 재설정
                    attempts = 6  # 시도 횟수 재설정
                    remaining_letters = qwerty  # 남은 알파벳 재설정
                    guesses = []  # 입력 내역 초기화
                    letter_status = {letter: 'unused' for letter in remaining_letters}  # 알파벳 상태 재설정
                    game_over = True  # 게임 종료 상태로 설정
                else:
                    message = ""

                return render(request, 'wordle/index.html', {
                    'message': message,
                    'remaining_letters': remaining_letters,
                    'attempts': attempts,
                    'guesses': guesses,
                    'letter_status': letter_status,
                    'game_over': game_over
                })

        elif 'reset' in request.POST:  # 게임을 다시 시작할 때
            answer = random.choice(word_list)
            attempts = 6
            remaining_letters = qwerty
            guesses = []
            letter_status = {letter: 'unused' for letter in remaining_letters}
            game_over = False  # 게임 종료 상태 해제
            return redirect('index')
    
    return render(request, 'wordle/index.html', {  # GET 요청일 때
        'remaining_letters': remaining_letters,
        'attempts': attempts,
        'guesses': guesses,
        'letter_status': letter_status,
        'game_over': game_over
    })
=======
import random
import string
import requests
import pandas as pd
from django.shortcuts import render, redirect

# 1. 단어 리스트 준비

# 엑셀 파일에서 단어 리스트를 로드하는 함수에 대한 설명
def load_excel(file_name):
    file_path = r'C:\Users\USER\Documents\wordle_game-1\wordle game\wordle_project\word\{}.xlsx'.format(file_name)
    
    try:
        df = pd.read_excel(file_path, engine='openpyxl', header=None)
        data_list = df.values.flatten().tolist()
        return data_list
    except Exception as e:
        return str(e)

# 단어가 유효한지 검사하는 함수
def is_valid_word(word):
    api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(api_url)
    return response.status_code == 200

# 글로벌 변수 설정
qwerty = ['q','w','e','r','t','y','u','i','o','p','a','s','d','f','g','h','j','k','l','z','x','c','v','b','n','m']
remaining_letters = qwerty
word_list = []
answer = ""
attempts = 6
guesses = []
game_over = False
letter_status = {letter: 'unused' for letter in remaining_letters}

def index(request):
    global remaining_letters, answer, attempts, guesses, game_over, letter_status, word_list

    if request.method == 'POST':
        if 'load_file' in request.POST:
            file_name = request.POST['file_name']
            word_list = load_excel(file_name)
            message : f'밀크T 초등 {file_name} 단어장을 선택 하셨습니다.'
            
            if isinstance(word_list, str):  # Error message returned
                return render(request, 'wordle/index.html', {
                    'error_message': word_list,
                })
                
            if not word_list:
                return render(request, 'wordle/index.html', {'error_message': '파일이 비어있거나 잘못된 형식입니다.'})
            
            answer = random.choice(word_list)
            attempts = 6
            remaining_letters = qwerty
            guesses = []
            letter_status = {letter: 'unused' for letter in remaining_letters}
            game_over = False
            message = f'밀크T 초등 {file_name} 단어장을 선택 하셨습니다.'
            return render(request, 'wordle/index.html', {
                'message': message,
                'remaining_letters': remaining_letters,
                'attempts': attempts,
                'guesses': guesses,
                'letter_status': letter_status,
                'game_over': game_over
            })
        
        if 'guess' in request.POST and not game_over:
            guess = request.POST['guess'].lower()
            
            if len(guess) != 5:
                return render(request, 'wordle/index.html', {
                    'message': '5개의 알파벳을 사용하는 단어를 입력해주세요.',
                    'remaining_letters': remaining_letters,
                    'attempts': attempts,
                    'guesses': guesses,
                    'game_over': game_over,
                    'letter_status': letter_status
                })

            if not is_valid_word(guess):
                return render(request, 'wordle/index.html', {
                    'message': '존재하지 않는 단어입니다.',
                    'remaining_letters': remaining_letters,
                    'attempts': attempts,
                    'guesses': guesses,
                    'game_over': game_over,
                    'letter_status': letter_status,
                })

            if guess == answer:
                feedback = ''.join([f'<span class="correct">{guess[i]}</span>' for i in range(5)])
                guesses.append({'guess': guess, 'feedback': feedback})
                game_over = True
                return render(request, 'wordle/index.html', {
                    'message': f'축하합니다! 정답을 맞추셨습니다. 정답은 {guess} 입니다.',
                    'remaining_letters': remaining_letters,
                    'attempts': attempts,
                    'guesses': guesses,
                    'game_over': game_over,
                    'letter_status': letter_status,
                })
            else:
                feedback = []
                correct_letters = set()
                for i in range(5):
                    if guess[i] == answer[i]:
                        feedback.append(f'<span class="correct">{guess[i]}</span>')
                        correct_letters.add(guess[i])
                        letter_status[guess[i]] = 'correct'
                    elif guess[i] in answer:
                        feedback.append(f'<span class="partial">{guess[i]}</span>')
                        correct_letters.add(guess[i])
                        if letter_status[guess[i]] != 'correct':
                            letter_status[guess[i]] = 'partial'
                    else:
                        feedback.append(f'<span class="wrong">{guess[i]}</span>')
                        letter_status[guess[i]] = 'wrong'
                
                attempts -= 1
                guesses.append({'guess': guess, 'feedback': ''.join(feedback)})
                if attempts == 0:
                    message = f"아쉽지만 모든 시도 횟수를 소진하셨습니다. 정답은 {answer} 입니다."
                    answer = random.choice(word_list)
                    attempts = 6
                    remaining_letters = qwerty
                    guesses = []
                    letter_status = {letter: 'unused' for letter in remaining_letters}
                    game_over = True
                else:
                    message = ""

                return render(request, 'wordle/index.html', {
                    'message': message,
                    'remaining_letters': remaining_letters,
                    'attempts': attempts,
                    'guesses': guesses,
                    'letter_status': letter_status,
                    'game_over': game_over
                })

        elif 'reset' in request.POST:
            answer = random.choice(word_list)
            attempts = 6
            remaining_letters = qwerty
            guesses = []
            letter_status = {letter: 'unused' for letter in remaining_letters}
            game_over = False
            return redirect('index')
    else:
        if not answer and word_list:  # #@! and word_list: 추가
            answer = random.choice(word_list)

        return render(request, 'wordle/index.html', {
            'message': '난이도 Milk T 단어장을 선택해 주세요.',
            'remaining_letters': remaining_letters,
            'attempts': attempts,
            'guesses': guesses,
            'letter_status': letter_status,
            'game_over': game_over
        })
    return render(request, 'wordle/index.html', {
        'message': '난이도 Milk T 단어장을 선택해 주세요.',
        'remaining_letters': remaining_letters,
        'attempts': attempts,
        'guesses': guesses,
        'letter_status': letter_status,
        'game_over': game_over
    })
>>>>>>> origin/ks
