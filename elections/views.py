from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Election, Position, Candidate, vote, CorpsMember
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Count
from django.contrib.admin.views.decorators import staff_member_required



# Create your views here.

def home(request):
    return render(request,"home.html")

#  Login details

# REGISTER
def register_view(request):
    if request.method == 'POST':
        state_code = request.POST['state_code']
        unit_name = request.POST['unit_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if CorpsMember.objects.filter(state_code=state_code).exists():
            messages.error(request, "State code already exists")
            return redirect('register')

        user = CorpsMember.objects.create_user(
            state_code=state_code,
            password=password1,
            unit_name=unit_name
        )
        messages.success(request, "Account created successfully")
        return redirect('login')

    return render(request, 'register.html')


# LOGIN
def login_view(request):
    if request.method == 'POST':
        state_code = request.POST['state_code']
        password = request.POST['password']

        user = authenticate(request, state_code=state_code, password=password)

        if user is not None:
            login(request, user)
            return redirect('election_list')
        else:
            messages.error(request, "Invalid login details")
            return redirect('login')

    return render(request, 'login.html')


# LOGOUT
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def election_list(request):
    elections = Election.objects.filter(is_active=True)
    return render(request, 'election_list.html', {'elections': elections})

@login_required
def vote_election(request, election_id):
    election = get_object_or_404(Election, id=election_id)
    positions = Position.objects.filter(election=election)

    # Check if user has already voted
    if request.user.has_voted_in(election):
        return render(request, 'already_voted.html', {'election': election})

    if request.method == 'POST':
        for position in positions:
            candidate_id = request.POST.get(f'position_{position.id}')
            if candidate_id:
                candidate = Candidate.objects.get(id=candidate_id)
                vote.objects.create(voter=request.user, position=position, candidate=candidate)
        return render(request, 'thank_you.html', {'election': election})

    return render(request, 'vote_election.html', {'election': election, 'positions': positions})

# result viewing
@login_required
def results_view(request, election_id):
    election = get_object_or_404(Election, id=election_id)
    positions = Position.objects.filter(election=election)

    results = []

    for position in positions:
        candidates = Candidate.objects.filter(position=position).annotate(
            vote_count=Count('votes')
        )
        results.append({
            'position': position,
            'candidates': candidates
        })

    return render(request, 'results.html', {
        'election': election,
        'results': results
    })
    
# 🛑 NOT STARTED
@login_required
def not_started(request, election_id):
    election = get_object_or_404(Election, id=election_id)
    return render(request, 'not_started.html', {'election': election})


# ⚠️ ALREADY VOTED
@login_required
def already_voted(request, election_id):
    election = get_object_or_404(Election, id=election_id)
    return render(request, 'already_voted.html', {'election': election})


# 👨‍💼 ADMIN DASHBOARD
@staff_member_required
def admin_dashboard(request):
    elections = Election.objects.all()
    return render(request, 'admin_dashboard.html', {'elections': elections})
