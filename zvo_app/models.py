from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
import re
import bcrypt
import _datetime
import datetime


class UserManager(models.Manager):
    def login_validator(self, postData):
        print(postData)
        errors = {}
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        existingEmailEntries = User.objects.filter(email=postData['userEmail'].lower())

        if not EMAIL_REGEX.match(postData['userEmail']):
            errors['emailRegex'] = "Please provide an e-mail in a valid format!"
        elif len(existingEmailEntries) == 0:
            errors['noEmail'] = "No user found with that email!"
        else:
            foundUser = existingEmailEntries[0]
            if len(postData['userPw']) < 8:
                errors['pwLen'] = "Invalid password!"
            elif bcrypt.checkpw(postData['userPw'].encode(), foundUser.pw_hash.encode()) != True:
                errors['wrongPw'] = "Incorrect password!"

        return errors

    def pw_update_validator(self, postData):
        print(postData)
        errors = {}
        currentUser = User.objects.get(id=postData['currentUserId'])
        if bcrypt.checkpw(postData['currentPw'].encode(), currentUser.pw_hash.encode()) != True:
            errors['currentPw'] = "Current password incorrect!"
        if len(postData['newPw']) < 8:
            errors['newPw'] = "New password must be at least 8 characters long!"
        if postData['newPw'] != postData['confNewPw']:
            errors['confNewPw'] = "New password and the confirmation field must match!"

        return errors


class MessageManager(models.Manager):
    def message_validator(self, postData):
        print(postData)
        errors = {}
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['msgName']) < 3:
            errors['nameLength'] = "Sender name must be at least 2 characters long!"
        if not EMAIL_REGEX.match(postData['msgEmail']):
            errors['emailRegex'] = "Please provide an e-mail in valid format!"
        if len(postData['msgContent']) < 11:
            errors['msgLen'] = "Message content is too short!"

        return errors


class PostManager(models.Manager):
    def demo_validator(self, postData):
        print(postData)
        errors = {}

        if len(postData['demoLabel']) < 2:
            errors['labelLength'] = "Demo label must be at least 2 characters long!"
        if len(postData['demoGenre']) < 2:
            errors['genreLength'] = "Demo genre must be at least 2 characters long!"

        return errors


    def article_validator(self, postData):
        print(postData)
        errors = {}

        if len(postData['articleHeadline']) < 2:
            errors['headlineLength'] = "Article headline must be at least 2 characters long!"
        if len(postData['articleBody']) < 2:
            errors['bodyLength'] = "Article body must be at least 2 characters long!"

        return errors


class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    pw_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return f"<User object: {self.name} (id#: {self.id})>"


class Message(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    content = models.CharField(max_length=1500)
    script_url = models.URLField()
    isNew = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = MessageManager()

    def __str__(self):
        return f"<Message object: (Sender:{self.name}) (Sent: {self.created_at})>"


class Article(models.Model):
    headline = models.TextField()
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = PostManager()

    def __str__(self):
        return f"<Article object: {self.headline} (Created: {self.created_at})>"


class Demo(models.Model):
    label = models.TextField()
    genre = models.TextField()
    file = models.FileField(upload_to='demos/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = PostManager()

    # .delete() override ensures the associated file will always be deleted
    def delete(self):
        file = self.file
        if file:
            file.delete()
        super(Demo, self).delete()

    def __str__(self):
        return f"<Demo object: {self.label} (Genre: {self.genre})>"


class Video(models.Model):
    file = models.FileField(upload_to='videos/')
    # the backup-url is intended to allow a secondary source for serving the file from a remote server
    backup_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # .delete() override ensures the associated file will always be deleted
    def delete(self):
        file = self.file
        if file:
            file.delete()
        super(Video, self).delete()

    def __str___(self):
        return f"<Video object: {self.file.url} (Updated: {self.updated_at})>"

class About(models.Model):
    pic = models.FileField(upload_to='pics/')
    header = models.TextField()
    paragraph_1 = models.TextField()
    paragraph_2 = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = PostManager()

    def __str___(self):
        return f"<About object: (Pic: {self.file.url}) (Updated: {self.updated_at})>"