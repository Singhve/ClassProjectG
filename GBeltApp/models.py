from django.db import models
import re


class UserManager(models.Manager):
    def userValidation(self, formInfo):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        matchingEmail = User.objects.filter(email=formInfo['email'])
        if len(formInfo['fname']) < 2:
            errors['fnamereq'] = "Enter a Valid First Name"
        if len(formInfo['lname']) < 2:
            errors['lnamereq'] = "Enter a Valid Last Name"
        if len(formInfo['email']) < 3:
            errors['email'] = "Invalid Email format"
        elif not EMAIL_REGEX.match(formInfo['email']):
            errors['emailinvalid'] = "Invalid email format"
        elif len(matchingEmail) > 0:
            errors['matchingemail'] = "Emails Taken"
        if len(formInfo['pw']) < 8:
            errors['showdPwReq'] = "Enter a Better password"
        if formInfo['pw'] != formInfo['repw']:
            errors['pwReq'] = "Passwords Dont Match"

        return errors

    def loginValidation(self, formInfo):
        errors = {}
        matchingemail = User.objects.filter(email=formInfo['logemail'])
        if len(formInfo['logemail']) < 3:
            errors['emailReq'] = "Enter a Email To Log In"
        elif len(matchingemail) == 0:
            errors['emailNotFound'] = "Email is not registered"
        else:
            if matchingemail[0].password != formInfo['logpw']:
                errors['wrongpass'] = "Password Not correct"

        return errors

    def editValidation(self, formInfo):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        matchingEmail = User.objects.filter(email=formInfo['email'])
        matching = formInfo['email']
        matching1 = formInfo['email1']

        if len(formInfo['fname']) < 2:
            errors['fnamereq'] = "Enter a Valid First Name"
        if len(formInfo['lname']) < 2:
            errors['lnamereq'] = "Enter a Valid Last Name"
        if len(formInfo['email']) < 3:
            errors['email'] = "Invalid Email format"
        elif not EMAIL_REGEX.match(formInfo['email']):
            errors['emailinvalid'] = "Invalid email format"
        elif len(matchingEmail) > 1:
            errors['matchingEmail'] = "Emails Taken"
        if matching1 != matching:
            errors['matching1email'] = "Emails Taken Already"
        else:
            return {}

        return errors


class QuoteManager(models.Manager):
    def quoteValidator(self, formInfo):
        errors = {}
        if len(formInfo['author']) < 3:
            errors['fnamereq'] = "Enter a Valid First Name"
        if len(formInfo['desc']) < 10:
            errors['lnamereq'] = "Enter a Valid Last Name"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Quote(models.Model):
    author = models.CharField(max_length=255)
    content = models.TextField()
    poster = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name="liked_quotes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()
