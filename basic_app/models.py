from django.db import models

class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    
    def __str__(self):
        return self.username

class Group(models.Model):
    name = models.CharField(max_length=64)
    members_count = models.PositiveIntegerField()
    date_created = models.DateField()

    def __str__(self):
        return self.name

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=1024)
    datetime_posted = models.DateTimeField()

    def __str__(self):
        return self.author.username + ': ' + self.content

class Association(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    is_leader = models.BooleanField(default=False)

    def __str__(self):
        return self.group.name + ': ' + self.member.username