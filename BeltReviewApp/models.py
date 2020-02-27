from django.db import models


class UserManager(models.Manager):
    def basic_validations(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if postData['password'] != postData['password_confirm']:
            error['password_confrim'] = 'Passwords do not match.'
        if len(postData['first_name']) < 3:
            errors['first_name'] = 'First name should be at least 3 characters.'
        if len(postData['last_name']) < 3:
            errors['last_name'] = 'Last name should be at least 3 characters.'
        if len(postData['alias']) < 5:
            errors['alias'] = 'Alias name should be at least 5 characters.'
        if len(postData['email']) < 5:
            errors['email'] = 'Email should be at least 5 characters.'
        if len(postData['password']) < 8:
            errors['password'] = 'Password should be at least 8 characters.'
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    alias = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Author(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Book(models.Model):
    title = models.CharField(max_length=20)
    author = models.ForeignKey(
        Author, related_name="books", on_delete=models.CASCADE)
    user_review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Review(models.Model):
    user = models.ForeignKey(
        User, related_name='users', on_delete=models.CASCADE)
    users_review = models.ForeignKey(
        Book, related_name='review', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# class Like(models.Model):
#     user_like = models.
