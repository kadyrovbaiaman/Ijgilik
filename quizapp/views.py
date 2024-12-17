from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Quiz, Question, Option, History
from .forms import QuizForm, QuestionForm, OptionForm

def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('homepage')
    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('homepage')
    return render(request, 'signup.html')

@login_required
def homepage(request):
    quizzes = Quiz.objects.all()
    return render(request, 'homepage.html', {'quizzes': quizzes})

@login_required
def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    return render(request, 'quiz_detail.html', {'quiz': quiz})

@login_required
def start_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.question_set.all()
    return render(request, 'quiz_page.html', {'quiz': quiz, 'questions': questions})

@login_required
def submit_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.question_set.all()
    score = 0
    for question in questions:
        selected_option_id = request.POST.get(str(question.id))
        if selected_option_id:
            option = Option.objects.get(id=selected_option_id)
            if option.is_correct:
                score += 1
    History.objects.create(user=request.user, quiz=quiz, score=score)
    return render(request, 'result.html', {'score': score, 'total': questions.count()})

@login_required
def create_quiz(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.creator = request.user  # Associate the logged-in user
            quiz.save()
            return redirect('add_questions', quiz_id=quiz.id)
    else:
        form = QuizForm()
    return render(request, 'create_quiz.html', {'form': form})


@login_required
def add_questions(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)

    if request.method == 'POST':
        question_text = request.POST.get('question_text')
        if not question_text:
            return render(request, 'add_questions.html', {'quiz': quiz, 'error': 'Question text is required.'})

        # Create the question
        question = Question.objects.create(quiz=quiz, text=question_text)
        print(f"Question created: {question.text}")

        # Create options
        for i in range(1, 5):
            option_text = request.POST.get(f'option_{i}')
            is_correct = f'correct_{i}' in request.POST
            if option_text:  # Ensure option text is not empty
                Option.objects.create(question=question, text=option_text, is_correct=is_correct)
                print(f"Option {i} created: {option_text}, Correct: {is_correct}")

        # Check if "Done" was clicked
        if 'done' in request.POST:
            return redirect('homepage')

    return render(request, 'add_questions.html', {'quiz': quiz})

@login_required
def history(request):
    histories = History.objects.filter(user=request.user)
    return render(request, 'history.html', {'histories': histories})

@login_required
def quiz_history_detail(request, history_id):
    history = get_object_or_404(History, id=history_id)
    questions = history.quiz.question_set.all()

    # Build user_answers as {question_id: selected_option_object}
    user_answers = {}
    for question in questions:
        selected_option_id = request.POST.get(str(question.id))  # Assuming POST data
        if selected_option_id:
            try:
                user_answers[question.id] = Option.objects.get(id=selected_option_id)
            except Option.DoesNotExist:
                user_answers[question.id] = None

    # Pass the context to the template
    return render(request, 'quiz_history_detail.html', {
        'history': history,
        'questions': questions,
        'user_answers': user_answers,
    })
