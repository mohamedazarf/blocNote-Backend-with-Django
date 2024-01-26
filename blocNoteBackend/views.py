from .models import BlocNotes
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import json
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
@csrf_exempt
def modify_note(request, id):
    if request.method == 'PUT':
        try:
            note = get_object_or_404(BlocNotes, id=id)
            data = json.loads(request.body.decode('utf-8'))  # Decode the request body
            title = data.get('title', '')  # Use .get() to avoid KeyError
            content = data.get('content', '')  # Use .get() to avoid KeyError
            
            # Update the note with the new title and content
            if 'title' in data:
                note.title = data['title']
            
            # Update the note with the new content if provided
            if 'content' in data:
                note.content = data['content']
            note.save()
            
            return JsonResponse({'message': 'Note modified successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return HttpResponseNotAllowed(['PUT'])
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