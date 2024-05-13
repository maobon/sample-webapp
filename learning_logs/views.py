from django.shortcuts import render, redirect, get_list_or_404
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required
from django.http import Http404


# Create your views here.
def index(request):
    return render(request, 'learning_logs/index.html')


@login_required
def topics(request):
    # topics = Topic.objects.order_by('date_created')
    ts = Topic.objects.filter(owner=request.user).order_by('date_created')

    context = {
        'topics': ts
    }
    return render(request, 'learning_logs/topics.html', context)


@login_required
def topic(request, topic_id):
    # t = Topic.objects.get(id=topic_id)
    t = get_list_or_404(Topic, id=topic_id)

    if t.owner != request.user:
        raise Http404

    entries = t.entry_set.order_by('-date_created')

    context = {
        'topic': t,
        'entries': entries
    }
    return render(request, 'learning_logs/topic.html', context)


@login_required
def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()

    else:
        form = TopicForm(request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            new.owner = request.user
            new.save()

            return redirect('learning_logs:topics')

    context = {
        'form': form
    }

    return render(request, 'learning_logs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    tt = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            new.topic = tt
            new.save()
            return redirect('learning_logs:topic', topic_id=topic_id)

    context = {
        'topic': tt,
        'form': form
    }

    return render(request, 'learning_logs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    e = Entry.objects.get(id=entry_id)
    t = e.topic

    if t.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = EntryForm(instance=e)
    else:
        form = EntryForm(instance=e, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=t.id)

    context = {
        'topic': t,
        'entry': e,
        'form': form
    }

    return render(request, 'learning_logs/edit_entry.html', context)
