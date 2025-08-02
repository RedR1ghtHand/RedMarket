from django.db import models


class Enchantment(models.Model):
    """
    Specific Enchantments can be applied to certain item types to maintain a full variety of those
    """
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    max_level = models.PositiveIntegerField(default=1)
    applicable_to = models.ManyToManyField('ItemType', related_name='enchantments', blank=True)

    def __str__(self):
        return self.name
