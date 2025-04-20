from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .models import Bb
from .forms import BbForm
from django.contrib.auth.decorators import login_required

# Контроллеры:
def index(request):
    bbs = Bb.objects.all()
    context = {"title": "Главная страница", "bbs": bbs}
    # bbs = Bb.objects.order_by('-published')
    return render(request, template_name='bboard/index.html', context={'bbs': bbs})

def about(request):
    return render(request, template_name='bboard/about.html')

def add_bb(request):
    if request.method == "GET":
        bb_form = BbForm()
        context = {'title': 'Добавить объявление', 'form': bb_form}
        return render(request, template_name='bboard/bb_add.html', context=context)
    if request.method == "POST":
        bb_form = BbForm(data=request.POST, files=request.FILES)
        if bb_form.is_valid():
            bb = Bb()
            bb.title = bb_form.cleaned_data['title']
            bb.content = bb_form.cleaned_data['content']
            bb.price = bb_form.cleaned_data['price']
            bb.image = bb_form.cleaned_data['image']
            bb.save()
            return index(request)

def read_bb(request, pk):
    bb = Bb.objects.get(pk=pk)
    context = {"title": "Информация об объявлении", "bb": bb}
    return render(request, template_name='bboard/bb_detail.html', context=context)

def update_bb(request, pk):
    bb = Bb.objects.get(pk=pk)
    if request.method == "POST":
        bb_form = BbForm(data=request.POST, files=request.FILES)
        if bb_form.is_valid():
            bb.title = bb_form.cleaned_data['title']
            bb.content = bb_form.cleaned_data['content']
            bb.price = bb_form.cleaned_data['price']
            bb.image = bb_form.cleaned_data['image']
            bb.save()
            return redirect('bboard:read_bb', pk=bb.id)
            # return read_bb(request, pk=bb.id)
    else:
        bb_form = BbForm(initial = {
            'tite:': bb.title,
            'content': bb.content,
            'price': bb.price,
            'image': bb.image,
        })
        return render(request, template_name='bboard/bb_edit.html', context={'form': bb_form})

def delete_bb(request, pk):
    bb = get_object_or_404(Bb, pk=pk)
    context = {"bb": bb}
    if request.method == "POST":
        bb.delete()
        return redirect('bboard:index')
    return render(request, template_name='bboard/bb_delete.html', context=context)

    # template = loader.get_template('bboard\index.html')
    # bbs = Bb.objects.order_by('-published')
    # context = {'bbs': bbs}
    # return HttpResponse(template.render(context, request))

    # s = 'Список объявлений\r\n\r\n\r\n'
    # for bb in Bb.objects.order_by('-published'):
    #     s += bb.title + '\r\n' + bb.content + '\r\n\r\n'
    # return HttpResponse(s, content_type='text/plain; charset=utf-8')
    # return HttpResponse("Здесь будет выведен список объявлений.")