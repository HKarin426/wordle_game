import random
import string
import requests
import pandas as pd
from django.shortcuts import render, redirect

# 엑셀 파일에서 단어 리스트를 로드하는 함수
def load_excel_from_github(file_name):
    url = f'https://github.com/HKarin426/wordle_game/raw/07cfeb6b6d8e09946c5f4c62e065455e1ddacfc1/wordle%20game/wordle_project/word/{file_name}.xlsx'
    
    try:
        df = pd.read_excel(url, engine='openpyxl', header=None)
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
            word_list = load_excel_from_github(file_name)
            message = f'밀크T 초등 {file_name} 단어장을 선택 하셨습니다.'
            
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

            if not is_valid_word(guess) and guess not in word_list:
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
        if not answer and word_list:
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
