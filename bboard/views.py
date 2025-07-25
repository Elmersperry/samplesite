from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .models import Bb
from .forms import BbForm, FilterForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.db.models import Q

# Контроллеры:

def index(request):
    bbs = Bb.objects.all().order_by('-published')
    count_bbs = Bb.objects.count()
    per_page = 5
    paginator = Paginator(bbs, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    filter_form = FilterForm()
    context = {"title": "Главная страница", "page_obj": page_obj, "count_bbs": count_bbs, "filter_form": filter_form}
    return render(request, template_name='bboard/index.html', context=context)

def about(request):
    count_bbs = Bb.objects.count()
    context = {"title": "О сайте", "count_bbs": count_bbs}
    return render(request, template_name='bboard/about.html', context=context)

@login_required
def add_bb(request):
    if request.method == "GET":
        bb_form = BbForm(author=request.user)
        context = {'title': 'Добавить объявление', 'form': bb_form}
        return render(request, template_name='bboard/bb_add.html', context=context)
    if request.method == "POST":
        bb_form = BbForm(data=request.POST, files=request.FILES, author=request.user)
        if bb_form.is_valid():
            # bb = Bb()
            # bb.author = bb_form.cleaned_data['author']
            # bb.title = bb_form.cleaned_data['title']
            # bb.content = bb_form.cleaned_data['content']
            # bb.price = bb_form.cleaned_data['price']
            # bb.image = bb_form.cleaned_data['image']
            bb_form.save()
            return index(request)
    return None

def read_bb(request, pk):
    # bb = Bb.objects.get(pk=pk)
    bb = get_object_or_404(Bb, pk=pk)
    context = {"title": "Информация об объявлении", "bb": bb}
    return render(request, template_name='bboard/bb_detail.html', context=context)

@login_required
def update_bb(request, pk):
    bb = get_object_or_404(Bb, pk=pk)
    if request.method == "POST":
        bb_form = BbForm(data = request.POST, files = request.FILES, author=request.user)
        if bb_form.is_valid():
            bb.author = bb_form.cleaned_data['author']
            bb.title = bb_form.cleaned_data['title']
            bb.content = bb_form.cleaned_data['content']
            bb.price = bb_form.cleaned_data['price']
            bb.image = bb_form.cleaned_data['image']
            bb.save()
            return redirect('bboard:read_bb', pk=bb.id)
    else:
        bb_form = BbForm(initial = {
            'title:': bb.title,
            'author': bb.author,
            'content': bb.content,
            'price': bb.price,
            'image': bb.image,
        }, author=request.user)
        return render(request, template_name="bboard/bb_edit.html", context = {"form": bb_form})

@login_required
def delete_bb(request, pk):
    bb = get_object_or_404(Bb, pk=pk)
    context = {"bb": bb}
    if request.method == "POST":
        bb.delete()
        return redirect('bboard:index')
    return render(request, template_name='bboard/bb_delete.html', context=context)

def page_not_found(request, exception):
    return render(request, template_name="bboard/404.html", context = {"title": "404"})

def forbidden(request, exception):
    return render(request, template_name="bboard/403.html", context = {"title": "403"})

def server_error(request):
    return render(request, template_name="bboard/500.html", context = {"title": "500"})

def user_bbs(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    # bbs = user.bbs.all()
    bbs = Bb.objects.filter(author=user).select_related('author')
    context = {'user': user, 'bbs': bbs}
    return render(request, template_name='bboard/user_bbs.html', context=context)

@login_required
def user_info(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    bbs = Bb.objects.filter(author=user).select_related('author')
    context = {'user': user, 'bbs': bbs}
    return render(request, template_name='bboard/user_info.html', context=context)

def search_bb(request):
    query = request.GET.get('query')
    query_text = Q(title__icontains=query) | Q(content__icontains=query)
    results = Bb.objects.filter(query_text)
    per_page = 5
    paginator = Paginator(results, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    count_bbs = results.count()
    context = {"title": "Главная страница", "page_obj": page_obj, "count_bbs": count_bbs}
    return render(request, template_name='bboard/index.html', context=context)

# def filter_bb(request):
#     author_id = request.GET.get('author')
#     published_id = request.GET.get('published')
#     if not author_id:
#         results = Bb.objects.all()
#     else:
#         author = User.objects.get(pk=author_id)
#         query_text = Q(author__exact=author)
#         results = Bb.objects.filter(query_text)
#     per_page = 5
#     paginator = Paginator(results, per_page)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     count_bbs = results.count()
#     filter_form = FilterForm()
#     context = {"title": "Главная страница", "page_obj": page_obj, "count_bbs": count_bbs, "filter_form": filter_form}
#     return render(request, template_name='bboard/index.html', context=context)

def filter_bb(request):
    filter_form = FilterForm(request.GET)
    query = Bb.objects.all()

    if filter_form.is_valid():
        author = filter_form.cleaned_data['author']
        created_at = filter_form.cleaned_data['created_at']
        if author:
            query = query.filter(author__exact=author)
        if created_at:
            query = query.filter(published__icontains=created_at)

    per_page = 5
    paginator = Paginator(query, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    count_bbs = query.count()

    context = {"title": "Главная страница", "page_obj": page_obj, "count_bbs": count_bbs, "filter_form": filter_form}
    return render(request, template_name='bboard/index.html', context=context)

# @login_required
# def update_bb(request, slug):
#     bb = get_object_or_404(Bb, slug=slug)
#     if request.method == "POST":
#         bb_form = BbForm(data=request.POST, files=request.FILES, author=request.user)
#         if bb_form.is_valid():
#             # bb.author = bb_form.cleaned_data['author']
#             bb.title = bb_form.cleaned_data['title']
#             bb.content = bb_form.cleaned_data['content']
#             bb.price = bb_form.cleaned_data['price']
#             bb.image = bb_form.cleaned_data['image']
#             bb_form.save()
#             # return redirect('bboard:read_bb', pk=bb.id)
#     else:
#         bb_form = BbForm(initial = {
#             'title:': bb.title,
#             'content': bb.content,
#             'price': bb.price,
#             'image': bb.image,
#         }, author=request.user)
#         return render(request, template_name='bboard/bb_edit.html', context={'form': bb_form})