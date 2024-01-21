from .models import BlocNotes
from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
def getAllNotes(request):
    response = HttpResponse()
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
    response['Access-Control-Allow-Headers'] = 'Content-Type, X-Requested-With'
    all_notes = BlocNotes.objects.all()
    notes_list = [{'title': note.title, 'content': note.get_content_list()} for note in all_notes]  # Call the method
    return JsonResponse({'notes': notes_list})

        
def default_view(request):
    return render(request, 'default.html')