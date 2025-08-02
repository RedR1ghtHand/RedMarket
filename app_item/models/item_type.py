from django.db import models
from django.utils.text import slugify

from app_item.models import Category


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
