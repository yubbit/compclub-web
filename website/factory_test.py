import factory

from datetime import timedelta
from random import randrange

from factory import PostGenerationMethodCall, Faker
from factory import LazyAttribute, Iterator
from factory.django import DjangoModelFactory
from django.contrib.auth.models import User

from . import models

class UserFactory(DjangoModelFactory):
    class Meta:
        model = models.CustomUser

    username = Faker('user_name')
    email = Faker('email')
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    password = PostGenerationMethodCall('set_password', 'admin')

    is_staff = Faker('boolean')
    is_active = Faker('boolean')
    is_superuser = Faker('boolean')


class EventFactory(DjangoModelFactory):
    class Meta:
        model = models.Event

    name = Faker('catch_phrase')
    start_date = Faker('future_date', end_date='+120d')
    finish_date = LazyAttribute(lambda obj: obj.start_date + timedelta(days=randrange(1, 30)))
    description = Faker('paragraph', nb_sentences=randrange(1, 10))
    owner = Iterator(models.Volunteer.objects.all())
    prerequisite = Faker('text', max_nb_chars=200)
    period = Faker('text', max_nb_chars=200)


class WorkshopFactory(DjangoModelFactory):
    class Meta:
        model = models.Workshop

    event = Iterator(models.Event.objects.all())
    name = Faker('catch_phrase')
    date = LazyAttribute(lambda obj: obj.event.start_date + timedelta(days=randrange(1, 30)))
    start_time = LazyAttribute(lambda obj: obj.date + timedelta(hours=randrange(1, 10)))
    #end_time = LazyAttribute(lambda obj: obj.start_time + timedelta(hours=randrange(1, 10)))
    description = Faker('paragraph', nb_sentences=randrange(1, 10))
    location = Faker('address')
    
    @factory.post_generation
    def available(self):
        for volunteer in models.Volunteers.objects.all():
            if random.random() > 0.5:
                self.available.add(volunteer)

    @factory.post_generation
    def assigned(self):
        for volunteer in models.Volunteers.objects.all():
            if random.random() > 0.5:
                self.available.add(volunteer)