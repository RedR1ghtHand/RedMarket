from django.db import models
from django.utils.text import slugify


class Material(models.Model):
    """
    Item materials that can be applied to
    armor [leather, chainmail, iron, turtle, gold, diamond, netherite]
    as a tier of weapon [wood, stone, iron, gold, diamond, netherite]
    as a type of wood [oak, spruce, birch, jungle, acacia, dark oak, mangrove, cherry, pale oak, crimson, warped,
    bamboo]
    """
    name = models.CharField(max_length=25, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    icon = models.ImageField(upload_to='materials/')
    description = models.TextField(blank=True)
    applicable_to = models.ManyToManyField('ItemType', related_name='materials', blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
