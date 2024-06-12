# views.py
#from django.shortcuts import render, redirect  # 중복 패키지 삭제
import pandas as pd
import random
import string
import requests
from django.shortcuts import render, redirect

#word_list = ['tough', 'print', 'pilot', 'spend', 'board', 'count', 'march', 'topic', 'slice', 'above']

# #@! 20240612
# 1. 단어 리스트 준비
file_path = r'C:\Users\user\Downloads\11sucsucwordsmaster1.xlsx'

# 엑셀 파일을 데이터프레임으로 읽어오기
df = pd.read_excel(file_path, engine='openpyxl', header=None)

# DataFrame을 리스트로 변환 후 평탄화
data_list = df.values.flatten().tolist()

word_list = data_list

# 리스트 단어 중 제일 긴 WORD
dl_max = len(max(data_list, key=len))

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
    global remaining_letters, answer, attempts, guesses, game_over, letter_status, dl_max

    #initial_guess = 1  # guess의 초기 값 설정  #@!

    if request.method == 'POST':  # POST 요청일 때  guess 사용자가 입력하는 갯수
        if 'guess' in request.POST and not game_over:
            guess = request.POST['guess'].lower()  # 입력된 단어를 소문자로 변환
            

            # 14글자가 아니면 message
            if len(guess) != dl_max:  # 액셀파일 중 제일 긴 단어기준 # << 바꿈 단어 길이가 5자가 아니면 에러 메시지 반환 
                return render(request, 'wordle/index.html', {
                    'message': '글자수가 아닙니다. 밀크T 리스트 중의 사용하는 영어 단어를 입력해주세요.',
                    'remaining_letters': remaining_letters,
                    'attempts': attempts,
                    'guesses': guesses,
                    'game_over': game_over,
                    'letter_status': letter_status
                })
            
            # 'message': '밀크T 리스트 중의 사용하는 영어 단어를 입력해주세요.',
            
            # # 14글자가 아니면 안됨.
            # if len(guess) <= dl_max:  # 액셀파일 중 제일 긴 단어기준 # << 바꿈 단어 길이가 5자가 아니면 에러 메시지 반환 
            #     return render(request, 'wordle/index.html', {
            #         'message': '글자수가 맞지 않습니다.',
            #         'remaining_letters': remaining_letters,
            #         'attempts': attempts,
            #         'guesses': guesses,
            #         'game_over': game_over,
            #         'letter_status': letter_status
            #     })
            
            # if len(answer) == dl_max:  # 14 = 14 액셀파일 중 제일 긴 단어기준 # << 바꿈 단어 길이가 5자가 아니면 에러 메시지 반환 
            #     return render(request, 'wordle/index.html', {
            #         'message': '글자수는 맞습니다.',
            #         'remaining_letters': remaining_letters,
            #         'attempts': attempts,
            #         'guesses': guesses,
            #         'game_over': game_over,
            #         'letter_status': letter_status
            #     })

            if not is_valid_word(guess):  # 단어가 유효하지 않으면 에러 메시지 반환
                return render(request, 'wordle/index.html', {
                    'message': '존재하지 않는 단어입니다.',
                    'remaining_letters': remaining_letters,
                    'attempts': attempts,
                    'guesses': guesses,
                    'game_over': game_over,
                    'letter_status': letter_status,
                })

            if guess == answer:  # 사용자가 정답을 맞춘 경우
                feedback = ''.join([f'<span class="correct">{guess[i]}</span>' for i in range(dl_max)])  # #@! range(5) dl_max
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
                for i in range(14):                   # #@! dl_max
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
            #initial_guess = 1     #@! 추가
            letter_status = {letter: 'unused' for letter in remaining_letters}
            game_over = False  # 게임 종료 상태 해제
            return redirect('index')
    
    return render(request, 'wordle/index.html', {  # GET 요청일 때
        'remaining_letters': remaining_letters,
        'attempts': attempts,
        'guesses': guesses,
        # 'initial_guess': initial_guess,     #@! 추가
        'letter_status': letter_status,
        'game_over': game_over
    })
