from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.html import escape
from django.utils.text import slugify

from tasks.models import Collection, Task


# Create your views here.
def index(request):
    context = {}

    collection_slug = request.GET.get('collection')

    collection = Collection.get_default_collection()
    if collection_slug:
        collection = get_object_or_404(Collection, slug=collection_slug)

    context['collections'] = Collection.objects.order_by('slug')
    context['collection'] = collection
    context['tasks'] = collection.task_set.order_by('description')

    return render(request, 'tasks/index.html', context=context)


def add_collection(request):
    collection_name = escape(request.POST.get('collection_name'))
    collection, created = Collection.objects.get_or_create(name=collection_name, slug=slugify(collection_name))

    if not created:
        return HttpResponse('La collection existe déjà', status=409)

    return render(request, 'tasks/collections.html', context={'collection': collection})


def add_task(request):
    if request.POST.get('collection') == 'null':
        collection = Collection.get_default_collection()
    else:
        collection = Collection.objects.get(slug=request.POST.get('collection'))

    description = escape(request.POST.get('task-description'))
    task = Task.objects.create(description=description, collection=collection)

    return render(request, 'tasks/task.html', context={'task': task})


def get_tasks(request, collection_pk: int):
    collection = get_object_or_404(Collection, pk=collection_pk)
    tasks = collection.task_set.order_by('description')
    return render(request, 'tasks/tasks.html', context={'tasks': tasks, 'collection': collection})


def delete_task(request, task_pk: int):
    task = get_object_or_404(Task, pk=task_pk)
    task.delete()
    return HttpResponse("")


def delete_collection(request, collection_pk: int):
    collection = get_object_or_404(Collection, pk=collection_pk)
    collection.delete()
    return redirect('home')
