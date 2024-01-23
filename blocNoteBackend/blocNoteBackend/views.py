from .models import BlocNotes
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
def getAllNotes(request):
    response = HttpResponse()
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
    response['Access-Control-Allow-Headers'] = 'Content-Type, X-Requested-With'
    all_notes = BlocNotes.objects.all()
    notes_list = [{'id': note.id, 'title': note.title, 'content': note.get_content_list()} for note in all_notes]  # Call the method
    return JsonResponse({'notes': notes_list})

@csrf_exempt
def add_note(request):
  if request.method == 'POST':
    title = request.POST['title']
    content = request.POST['content']
    note = BlocNotes(title=title, content=content)
    note.save()
    return redirect('/')
  return render(request, 'addNote.html')

from django.middleware.csrf import get_token
@csrf_exempt
def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})
from django.http import HttpResponseNotAllowed
@csrf_exempt
def delete_note(request, id):
    if request.method == 'DELETE':
        try:
            note = BlocNotes.objects.get(id=id)
            note.delete()
            return HttpResponse(status=204)  # No content for a successful delete
        except BlocNotes.DoesNotExist:
            return HttpResponse(status=404)  # Note not found
    else:
        return HttpResponseNotAllowed(['DELETE'])
        
def default_view(request):
    return render(request, 'default.html')