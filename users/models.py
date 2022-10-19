from django.db import models
from django.utils.text import slugify
# Create your models here.


class FoodPreference(models.Model):
    slug = models.SlugField(db_index=True, unique=True, max_length=50)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.slug = slugify(self.name)
        super(FoodPreference, self).save(force_insert, force_update, using, update_fields)


class UserFoodPreference(models.Model):
    user_id = models.CharField(max_length=20)
    preference = models.ForeignKey(FoodPreference, related_name='users', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user_id', 'preference')
