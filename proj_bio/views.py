#from django.shortcuts import render
#from django.core.cache import cache
#from . import quiz_work
from django.shortcuts import render, redirect
from django.urls import reverse
import random

"""
QUESTIONS = [
    {
        "id": 1,
        "text": "Как называется единица наследственности?",
        "variants": [
            {"id": 1, "text": "Клетка"},
            {"id": 2, "text": "Ген"},
            {"id": 3, "text": "Хромосома"},
            {"id": 4, "text": "Молекула"},
        ],
        "correct": 2
    },
    {
        "id": 2,
        "text": "Что такое фотосинтез?",
        "variants": [
            {"id": 1, "text": "Процесс дыхания растений"},
            {"id": 2, "text": "Превращение солнечной энергии в химическую"},
            {"id": 3, "text": "Размножение клеток"},
            {"id": 4, "text": "Испарение воды листьями"},
        ],
        "correct": 2
    },
    {
        "id": 3,
        "text": "Какой ученый открыл законы наследования признаков?",
        "variants": [
            {"id": 1, "text": "Чарльз Дарвин"},
            {"id": 2, "text": "Грегор Мендель"},
            {"id": 3, "text": "Луи Пастер"},
            {"id": 4, "text": "Иван Павлов"},
        ],
        "correct": 2
    },
    {
        "id": 4,
        "text": "Как называют «строительные кирпичи» всех живых организмов?",
        "variants": [
            {"id": 1, "text": "Молекулы"},
            {"id": 2, "text": "Ткани"},
            {"id": 3, "text": "Клетки"},
            {"id": 4, "text": "Органы"},
        ],
        "correct": 3
    }
    ]
"""

def index(request):
    context = {
        "title": "Добро пожаловать в мир биологии!",
        "message": "Здесь вы можете изучать удивительный мир живых организмов, клеток, генов и экосистем."
    }
    return render(request, "index.html", context)



"""
def theory(request):
    pass
    return render(request, 'theory.html')

def start_test(request):
    pass
    request.session.flush()  # Очищение
    random.shuffle(QUESTIONS)  # Перемешивание
    request.session['questions'] = QUESTIONS
    request.session['answers'] = {}  # {question_id: user_answer_id}
    request.session['current_question'] = 1  # Счётчик
    return redirect(reverse('test_page', args=[1]))

def test_page(request, question_id):
    pass
    questions = request.session.get('questions')
    if not questions or question_id > len(questions) or question_id < 1:
        return redirect(reverse('index'))

    question = questions[question_id - 1]
    question['number'] = question_id
    question['progress'] = int((question_id / len(questions)) * 100)

    return render(request, 'test_page.html', {'question': question})
    

def submit_answer(request):
    pass
    
    if request.method != "POST":
        return redirect(reverse('index'))

    question_id = int(request.POST.get('question_id'))
    user_answer = int(request.POST.get('answer'))
    questions = request.session.get('questions')

    if not questions or question_id < 1 or question_id > len(questions):
        return redirect(reverse('index'))

    # Сохраняем ответ пользователя
    request.session['answers'][str(question_id)] = user_answer

    # Переходим к следующему вопросу или к результатам
    next_question = question_id + 1
    if next_question > len(questions):
        return redirect(reverse('result'))
    else:
        return redirect(reverse('test_page', args=[next_question]))
    


def result(request):
    return render(request, 'result.html')
    pass
    questions = request.session.get('questions')
    user_answers = request.session.get('answers', {})

    if not questions or not user_answers:
        return redirect(reverse('index'))

    correct_count = 0
    mistakes = []

    for q in questions:
        user_ans = user_answers.get(str(q['id']))
        correct_ans = q['correct']

        if user_ans == correct_ans:
            correct_count += 1
        else:
            mistakes.append({
                "question": q['text'],
                "user_answer": next((v['text'] for v in q['variants'] if v['id'] == user_ans), "Не выбрано"),
                "correct": next((v['text'] for v in q['variants'] if v['id'] == correct_ans), "Ошибка")
            })

    score = int((correct_count / len(questions)) * 100)

    context = {
        "score": score,
        "correct_answers": correct_count,
        "mistakes": mistakes,
    }
    return render(request, 'result.html', context)

"""