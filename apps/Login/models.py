from __future__ import unicode_literals
import re
from django.db import models
import bcrypt
from django.contrib import messages


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
class UserManager(models.Manager):
    def validate_reg(self, post_data):
        errors = {}

        # check all fields for emptyness
        for field, value in post_data.iteritems():
            if len(value) < 1:
                errors[field] = "{} field is reqired".format(field.replace('_', ' '))
                

            # check name fields for min length
            if field == "firstname":
                if not field in errors and not post_data['firstname'].isalpha():
                    errors[field] = "First name must contain letters only"
                if not field in errors and len(value) < 2:
                    errors[field] = "{} field must be at least 2 letters".format(field.replace('_', ' '))
            if field == "lastname":
                if not field in errors and not post_data['lastname'].isalpha():
                    errors[field] = "Last name must contain letters only"
                if not field in errors and len(value) < 2:
                    errors[field] = "{} field must be at least 2 letters".format(field.replace('_', ' '))
            if field == "password":
                if not field in errors and len(value) < 8:
                    errors[field] = "Password must be contain more than 8 characters"
            if field == "confirmpassword":
                if not field in errors and post_data['confirmpassword'] != post_data['password']:
                    errors[field] = "Passwords do not match"
            
        # check email field for valid email
        if not "email" in errors and not re.match(EMAIL_REGEX, post_data['email']):
            errors['email'] = "invalid email"
        
        # if email is valid check db for existing email
        else:
            if len(self.filter(email=post_data['email'])) > 1:
                errors['email'] = "email already in use"

        return errors
    def validate_log(self, post_data):
        errors={}
        for field, value in post_data.iteritems():
            if len(value) < 1:
                errors[field] = "{} field is reqired".format(field.replace('_', ' '))
        if not "email" in errors and not re.match(EMAIL_REGEX, post_data['email']):
            errors['email'] = "invalid email"

        if len(self.filter(email=post_data['email'])) > 0:
            user = self.filter(email=post_data['email'])[0]
            if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
                errors['password']="email or password is incorrect"
        else:
            errors['email']="email or password is incorrect"

        return errors
class User(models.Model):
    firstname= models.CharField(max_length=255)
    lastname=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    objects = UserManager()
    def __str__(self):
        return self.email


# Create your models here.
