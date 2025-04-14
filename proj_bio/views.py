"""Functions views"""
import csv
import os
from django.shortcuts import render, redirect
from django import forms

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

def load_quiz_questions():
    """load quiz from file"""
    quiz_questions = []
    file_path = os.path.join(DATA_DIR, 'quiz_data.csv')
    try:
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                question = {
                    "id": int(row['id']),
                    "question": row['question'],
                    "options": [row['option1'], row['option2'], row['option3'], row['option4']],
                    "correct": int(row['correct']) - 1  
                }
                quiz_questions.append(question)
    except FileNotFoundError:
        print(f"[!] Файл {file_path} не найден!")
    return quiz_questions

def load_theory_data():
    """load of theory page from file"""
    theory_pages = []
    file_path = os.path.join(DATA_DIR, 'theory_data.csv')
    try:
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                theory_pages.append({
                    "id": int(row['id']),
                    "title": row['title'],
                    "content": row['content'].replace('\\n', '\n')  
                })
    except FileNotFoundError:
        print(f"[!] Файл {file_path} не найден!")
    return theory_pages

THEORY_PAGES = load_theory_data()


class QuizForm(forms.Form):
    """class form quizs"""
    def __init__(self, *args, **kwargs):
        quiz_questions = load_quiz_questions()
        super().__init__(*args, **kwargs)
        for i, q in enumerate(quiz_questions):
            self.fields[f'question_{i}'] = forms.ChoiceField(
                label=q['question'],
                choices=[(str(j), opt) for j, opt in enumerate(q['options'])],
                widget=forms.RadioSelect
            )

def index(request):
    """main page"""
    context = {
        "title": "Добро пожаловать в мир биологии!",
        "message": "Здесь вы можете изучать удивительный мир живых организмов, клеток и экосистем."
    }
    return render(request, "index.html", context)

def theory(request):
    """theory page"""
    context = {
        "theory_pages": THEORY_PAGES
    }
    return render(request, 'theory.html', context)

def quiz(request):
    """quiz page"""
    quiz_questions = load_quiz_questions()
    if request.method == "POST":
        form = QuizForm(request.POST)
        if form.is_valid():
            score = 0
            for i, question in enumerate(quiz_questions):
                user_answer = int(form.cleaned_data[f'question_{i}'])
                if user_answer == question['correct']:
                    score += 1
            return redirect('quiz_result', score=score)
    else:
        form = QuizForm()
    return render(request, "quiz/quiz_form.html", {"form": form})

def quiz_result(request, score):
    """page result of quiz"""
    quiz_questions = load_quiz_questions()
    total = len(quiz_questions)
    context = {
        "score": score,
        "total": total,
        "percent": int((score / total) * 100),
        "comment": "Отлично!" if score >= 4 else "Хорошо!" if score >= 3 else "Попробуй ещё раз!"
    }
    return render(request, "quiz/quiz_result.html", context)


class AddQuestionForm(forms.Form):
    """form to add question"""
    question_text = forms.CharField(
        label="Текст вопроса",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )
    option1 = forms.CharField(
        label="Вариант 1",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )
    option2 = forms.CharField(
        label="Вариант 2",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )
    option3 = forms.CharField(
        label="Вариант 3",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )
    option4 = forms.CharField(
        label="Вариант 4",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )
    correct_answer = forms.ChoiceField(
        label="Номер правильного ответа",
        choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )

def add_question(request):
    """add question in quiz"""
    if request.method == "POST":
        form = AddQuestionForm(request.POST)
        if form.is_valid():
            question_text = form.cleaned_data['question_text']
            options = [
                form.cleaned_data['option1'],
                form.cleaned_data['option2'],
                form.cleaned_data['option3'],
                form.cleaned_data['option4']
            ]
            correct_answer = int(form.cleaned_data['correct_answer'])

            quiz_questions = load_quiz_questions()
            new_id = max((q['id'] for q in quiz_questions), default=0) + 1

            file_path = os.path.join(DATA_DIR, 'quiz_data.csv')
            with open(file_path, mode='a', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    new_id,
                    question_text,
                    options[0],
                    options[1],
                    options[2],
                    options[3],
                    correct_answer
                ])

            return redirect('quiz')
    else:
        form = AddQuestionForm()

    return render(request, 'quiz/add_question.html', {'form': form})
