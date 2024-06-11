from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string

# 상수 정의
WORD_LIST = ['apple', 'bread', 'crane', 'dance', 'eagle']  # 단순화된 단어 목록
MAX_ATTEMPTS = 6

def get_random_word():
    return get_random_string(length=5, allowed_chars='abcdefghijklmnopqrstuvwxyz')

def index(request):
    if 'word' not in request.session:
        request.session['word'] = get_random_word()
        request.session['attempts'] = MAX_ATTEMPTS
        request.session['guesses'] = []

    word = request.session['word']
    attempts = request.session['attempts']
    guesses = request.session['guesses']

    if request.method == 'POST':
        if 'reset' in request.POST:
            request.session.flush()
            return redirect('index')
        else:
            guess = request.POST.get('guess').lower()
            feedback = generate_feedback(word, guess)
            guesses.append({'guess': guess, 'feedback': feedback})
            attempts -= 1
            request.session['attempts'] = attempts
            request.session['guesses'] = guesses

            if guess == word or attempts == 0:
                return redirect('result')

    context = {
        'remaining_letters': len(set(word) - set(''.join([g['guess'] for g in guesses]))),
        'attempts': attempts,
        'guesses': guesses
    }

    return render(request, 'index.html', context)

def result(request):
    word = request.session.get('word', '')
    guesses = request.session.get('guesses', [])
    won = any(guess['guess'] == word for guess in guesses)
    
    context = {
        'word': word,
        'guesses': guesses,
        'won': won
    }

    return render(request, 'result.html', context)

def generate_feedback(word, guess):
    feedback = []
    for i, char in enumerate(guess):
        if char == word[i]:
            feedback.append(f'<span class="correct">{char}</span>')
        elif char in word:
            feedback.append(f'<span class="partial">{char}</span>')
        else:
            feedback.append(f'<span class="wrong">{char}</span>')
    return ''.join(feedback)