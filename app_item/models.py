from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=35, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class ItemType(models.Model):
    name = models.CharField(max_length=35, unique=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="item_types")

    def __str__(self):
        return f"{self.name} ({self.category.name})"


class Material(models.Model):
    name = models.CharField(max_length=25, unique=True)
    icon = models.ImageField(upload_to='materials/')
    description = models.TextField(blank=True)
    applicable_to = models.ManyToManyField('ItemType', related_name='materials', blank=True)

    def __str__(self):
        return self.name


class Enchantment(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    max_level = models.PositiveIntegerField(default=1)
    applicable_to = models.ManyToManyField('ItemType', related_name='enchantments', blank=True)

    def __str__(self):
        return self.name


class BaseItem(models.Model):
    MAX_STACK_CHOICES = [
        (1, '1'),
        (16, '16'),
        (64, '64'),
    ]

    name = models.CharField(max_length=35, unique=True)
    image = models.ImageField(upload_to='items/')
    item_type = models.ForeignKey(ItemType, on_delete=models.CASCADE)
    max_stack = models.IntegerField(choices=MAX_STACK_CHOICES, default=1)

    class Meta:
        abstract = True

    @property
    def category(self):
        return self.item_type.category


class EnchantedItem(BaseItem):
    pass
