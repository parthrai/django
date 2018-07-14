from django.views import generic
from .models import Album, Song
from django.shortcuts import get_object_or_404, get_list_or_404
from django.shortcuts import render, redirect
from urllib import request
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .forms import UserForm
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.http import HttpResponse


def check(request, pk):
    print("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWw")
    print(pk)
    print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQq")
    album = Album.objects.filter(id= pk).first()
    songs = Song.objects.filter(album_id=pk).all()
    print("VVVVVVVVVVVVVVVVVVVVVVVVVVVVVV")
    return render(request, 'music/album_detail.html', {'songs': songs, 'album': album})

class IndexView(generic.ListView):
    template_name = 'music/index.html'
    context_object_name = 'all_albums'

    def get_queryset(self):
        return Album.objects.all()


class DetailView(generic.DetailView):
    model = Album
    print('***************************************88')
    print(Song.objects.raw('select * from music_song'))
    print('***************************************88')
    songs = Song.objects.all()
    # template_name = 'music/detail.html'

    def details(request):
        songs = Song.objects.all()
        print("VVVVVVVVVVVVVVVVVVVVVVVVVVVVVV")
        return render(request, 'music:detail', songs)


#    contact_object_name = 'all_songs'

#    def get_queryset(self):
#        return Song.objects.all()


class AlbumCreate(CreateView):
    model = Album
    fields = ['artist', 'album_title', 'genre', 'album_logo']


class SongCreate(CreateView):
    model = Song
    fields = ['album', 'file_type', 'song_title', 'is_favorite']


class AlbumUpdate(UpdateView):
    model = Album
    fields = ['artist', 'album_title', 'genre', 'album_logo']


class AlbumDelete(DeleteView):
    model = Album
    success_url = reverse_lazy('music:index')


class UserFormView(View):
    form_class = UserForm
    template_name = 'music/registration_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            if user is not None:

                if user.is_active:
                    login(request, user)
                    return redirect('music:index')

        return render(request, self.template_name, {'form': form})
