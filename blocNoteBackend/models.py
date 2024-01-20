# blocNoteBackend/models.py
from django.db import models

class BlocNotes(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()  # Champ de type texte
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_content_list(self):
        return self.content.split('\n')  # Utiliser le retour à la ligne comme délimiteur

    def set_content_list(self, content_list):
        self.content = '\n'.join(content_list)

    content_list = property(get_content_list, set_content_list)

    def __str__(self):
        return self.title
    
# class AppUsers(models.Model):
#     username = models.CharField(max_length=50) 
#     password = models.CharField(max_length=50)



