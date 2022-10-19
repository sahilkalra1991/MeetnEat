from django.db import models
from datetime import datetime


class Campus(models.Model):
    """
    A campus will represent a university campus e.g. TUM Main Campus, TUM Garching campus
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=datetime.now)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Campuses"

    def __str__(self):
        return self.name


class EventLocation(models.Model):
    """
    A location where the Event will take place. 
    The location can be public or private
    Public location: TUM Kitchen, Mensa etc
    Private location: User's private Kitchen
    """
    name = models.CharField(max_length=100)
    campus = models.ForeignKey(Campus, null=True, blank=True, on_delete=models.CASCADE,
                               help_text="Campus of the University")
    description = models.TextField(blank=True)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=datetime.now)
    modified_at = models.DateTimeField(auto_now=True)
    user_id = models.CharField(max_length=20, blank=True, verbose_name="Event Location Creator",
                               help_text="Id of the Event creator")

    def __str__(self):
        return self.name


class Event(models.Model):
    """
    An event will be a gathering of people with a pre-specified food items and cuisines
    A User will create an event and other users can join it if they like the type of food it offers
    """
    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=datetime.now)
    modified_at = models.DateTimeField(auto_now=True)
    start_at = models.DateTimeField(default=datetime.now)
    end_at = models.DateTimeField(default=datetime.now)
    capacity = models.IntegerField(default=10)
    location = models.ForeignKey(EventLocation, on_delete=models.CASCADE)
    user_id = models.CharField(max_length=20, verbose_name="Event Creator", help_text="Id of the Event creator")

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        is_new_object = not self.id
        # Save event to database
        super(Event, self).save(force_insert, force_update, using, update_fields)
        if is_new_object:
            # Create an Event User object with the Creator
            EventUser.objects.get_or_create(event_id=self.id, user_id=self.user_id, defaults={'is_creator': True})


class EventPreference(models.Model):
    """
    An event preference is the food preference that this event qualifies for.
    """
    event = models.ForeignKey(Event, related_name='preferences', on_delete=models.CASCADE)
    food_preference = models.ForeignKey('users.FoodPreference', related_name='events', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now)
    modified_at = models.DateTimeField(auto_now=True)


class EventUser(models.Model):
    """
    An event user is the participant in the Event.
    An event can either be the creator or not
    """
    event = models.ForeignKey(Event, related_name='users', on_delete=models.CASCADE)
    user_id = models.CharField(max_length=20, verbose_name="Event Member",  help_text="Id of the Event participant")
    is_creator = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=datetime.now)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('event', 'user_id')
        verbose_name = "Event Member"


class EventMessage(models.Model):
    """
    An event message will be a message shared by EventUser.
    """
    event = models.ForeignKey(Event, related_name='messages', on_delete=models.CASCADE)
    user_id = models.CharField(max_length=20, verbose_name="Message Creator", help_text="Id of the Message creator")
    text = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    modified_at = models.DateTimeField(auto_now=True)


class EventShoppingItem(models.Model):
    """
    An Event shopping item is an item which needs to be bought and brought to the event.
    It can be food items or cooking utensil
    """
    event = models.ForeignKey(Event, related_name='shop_items', on_delete=models.CASCADE)
    user_id = models.CharField(max_length=20, verbose_name="Item Creator",  help_text="Id of the Shopping item creator")
    created_at = models.DateTimeField(default=datetime.now)
    modified_at = models.DateTimeField(auto_now=True)
    amount = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=100)
    bringer_id = models.CharField(max_length=20, verbose_name="Item Bringer",
                                  help_text="Id user who will bring the shopping item", blank=True)


class EventMeal(models.Model):
    """
    An Event Meal is a food meal which can be one of the options to cook at the event.
    """
    event = models.ForeignKey(Event, related_name='meals', on_delete=models.CASCADE)
    user_id = models.CharField(max_length=20, verbose_name="Meal Creator",  help_text="Id of the Meal creator")
    meal_id = models.CharField(max_length=20, verbose_name="Meal Id", help_text="Id of the Global Meal")
    created_at = models.DateTimeField(default=datetime.now)
    modified_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100)


class EventMealVote(models.Model):
    """
    An Event Meal Vote represent a vote on the Meal
    """
    meal = models.ForeignKey(EventMeal, related_name="votes", on_delete=models.CASCADE)
    user_id = models.CharField(max_length=20, verbose_name="Meal Creator",  help_text="Id of the Meal creator")
    created_at = models.DateTimeField(default=datetime.now)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user_id', 'meal')
