from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager

# Create your models here.
class CorpsMemberManager(BaseUserManager):

    def create_user(self, state_code, password=None, **extra_fields):
        if not state_code:
            raise ValueError("State code is required")

        user = self.model(state_code=state_code, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, state_code, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(state_code, password, **extra_fields)

#  begin of Corps Members

class CorpsMember(AbstractUser):
    username = None
    state_code = models.CharField(max_length=20, unique=True)
    unit_name = models.CharField(max_length=100)
    
    USERNAME_FIELD = 'state_code'
    REQUIRED_FIELDS = []

    objects = CorpsMemberManager()
    
    def __str__(self):
        return self.state_code
    
    #  This checks if the corps member has voted in that election.

    def has_voted_in(self, election):
       return self.votes.filter(position__election=election).exists()
    

# Election Models
class Election(models.Model):
    title = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Position(models.Model):
    title = models.CharField(max_length=100)
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name="positions")

    def __str__(self):
        return self.title
    
class Candidate(models.Model):
    name = models.CharField(max_length=100)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name="candidates")
    photo = models.ImageField(upload_to='candidates/', blank=True, null=True)

    def __str__(self):
        return self.name

class vote(models.Model):
    voter = models.ForeignKey(CorpsMember, on_delete=models.CASCADE, related_name="votes")
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="votes")
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name="votes")
    timestamp = models.DateTimeField(auto_now_add=True)

#  One corps member cannot vote twice for the same position


    class Meta:
        unique_together = ('voter','position')


# unique_together will prevent double voting per positon

    def __str__(self):
        return f"{self.voter} voted for {self.candidate}"