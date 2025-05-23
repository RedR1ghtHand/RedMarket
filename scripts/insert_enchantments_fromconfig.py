import json
import logging
from app_item.models import Enchantment, ItemType


logger = logging.getLogger('script')

with open('config/item_enchantments.json') as f:
    enchantments = json.load(f)


def run():
    """
    If running script directly:

    import django
    import os
    import sys


    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "redmarket.settings")
    django.setup()

    from app_item.models import Model #after django.setup()


    def run():
        ...

    if __name__ == "__main__":
    run()
    """
    for enchantment_data in enchantments:
        name = enchantment_data["name"]
        description = enchantment_data.get("description", "")
        max_lvl = enchantment_data["max_lvl"]
        applicable_to = enchantment_data["applicable_to"]

        enchantment, created = Enchantment.objects.get_or_create(name=name, description=description, max_level=max_lvl)

        if created:
            logger.debug(f" [+] Created enchantment: {enchantment.name}")
        else:
            logger.debug(f"! Enchantment already exists: {enchantment.name}")

        for itype_name in applicable_to:
            try:
                item_type = ItemType.objects.get(name=itype_name)
                if not enchantment.applicable_to.filter(id=item_type.id).exists():
                    enchantment.applicable_to.add(item_type)
                    logger.debug(f"+ Linked '{itype_name}' to enchantment '{enchantment.name}'")
                else:
                    logger.debug(f"! '{itype_name}' already linked to enchantment '{enchantment.name}'")
            except ItemType.DoesNotExist:
                logger.error(f" [!] ItemType '{itype_name}' does not exist. Please check your item types!")

