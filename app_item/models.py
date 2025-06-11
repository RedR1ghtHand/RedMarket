from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    """
    Item categories, such as:
    - armor
    - weapons
    - tools
    - ammunition
    - utilities
    - wooden
    - structural
    - decorative
    """
    name = models.CharField(max_length=35, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ItemType(models.Model):
    """
    Item types needed to classify items from the same category and specify other meta like enchantments,
    materials, etc.
    - armor [helmet, chestplate, leggings, boots, elytra?, horse armor, wolf armor]
    - weapons [sword, bow, crossbow, trident, mace, axe?]
    - tools [pickaxe, axe, shovel, brush, fishing rod, hoe, carrot on a stick, warped fungus on a stick, flind and steel,
    shears, shield, elytra?]
    - ammunition [arrow, tipped arrow, firework rocket]
    - utilities [bottles, buckets, informational, other]
    - wooden [wood, logs, planks, boat, fence gate, sign, button, door, fence, pressure plate, slab, stairs,
    trapdoor]
    - structural [stone blocks, overworld blocks, the nether blocks, the end blocks, materials blocks]
    - decorative [terracotta, glazed terracotta, wool, concrete, concrete powder, glass stained, glass pane stained,
    candles, other]
    """
    name = models.CharField(max_length=35, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="item_types")

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


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


