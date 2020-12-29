from django.db import models
import re
from datetime import datetime

class UserManager(models.Manager):
    def create_validator(self, requestPOST):
        errors = {}
        if len(requestPOST['first_name']) < 2:
            errors['first_name'] = "First Name is too short!"
        if len(requestPOST['last_name']) < 2:
            errors['last_name'] = "Last Name is too short!"
        if len(requestPOST['password']) < 8:
            errors['password'] = "Password is too short!"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        NAME_REGEX = re.compile(r'^[a-zA-Z-]+$')
        if not EMAIL_REGEX.match(requestPOST['email']):
            errors['error_format'] = 'Email is not in correct format!'
        if not NAME_REGEX.match(requestPOST['first_name']):
            errors['first_name_format'] = 'First name is not in correct format!'
        if not NAME_REGEX.match(requestPOST['last_name']):
            errors['last_name_format'] = 'Last name is not in correct format!'
        users_with_email = User.objects.filter(email=requestPOST['email'])
        if len(users_with_email) > 0:
            errors['dup_email'] = 'Email already in database'
        if requestPOST['password'] != requestPOST['password_confirm']:
            errors['no_match'] = "Passwords are not the same"
        return errors

    def login_validator(self,requestPOST):
        errors={}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(requestPOST['email']):
            errors['error_format'] = 'Email is not in correct format!'
        return errors
    
    def edit_validator(self,requestPOST):
        errors={}
        if len(requestPOST['first_name']) < 2:
            errors['first_name'] = "First Name is too short!"
        if len(requestPOST['last_name']) < 2:
            errors['last_name'] = "Last Name is too short!"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(requestPOST['email']):
            errors['error_format'] = 'Email is not in correct format!'
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        NAME_REGEX = re.compile(r'^[a-zA-Z-]+$')
        if not EMAIL_REGEX.match(requestPOST['email']):
            errors['error_format'] = 'Email is not in correct format!'
        if not NAME_REGEX.match(requestPOST['first_name']):
            errors['first_name_format'] = 'First name is not in correct format!'
        if not NAME_REGEX.match(requestPOST['last_name']):
            errors['last_name_format'] = 'Last name is not in correct format!'
        users_with_email = User.objects.filter(email=requestPOST['email'])
        if len(users_with_email) > 0:
            errors['dup_email'] = 'Email already in database'
        return errors


class User(models.Model):
    first_name = models.CharField(max_length= 255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    #image

    def __str__(self):
        return self.first_name

class QuoteManager(models.Manager):
    def quote_validator(self, requestPOST):
        errors = {}
        if len(requestPOST['author_by']) < 3:
            errors['author_name_short'] = "Author Name too short!"
        if len(requestPOST['quote']) < 10:
            errors['quote_short'] = "Quote too short!"
        return errors

class Quote(models.Model):
    author_by = models.CharField(max_length=255)
    quote = models.CharField(max_length=255)
    posted_by = models.ForeignKey(User, related_name= "posted_quotes", on_delete = models.CASCADE)
    user_likes = models.ManyToManyField(User, related_name="likes")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = QuoteManager()
    
    def __str__(self):
        return "Author: "+ self.posted_by.first_name + ". Quote: "+ self.quote