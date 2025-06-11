import json
import logging

from app_item.models import Category, ItemType


logger = logging.getLogger('script')

with open('config/item_types.json') as f:
    item_types = json.load(f)


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
    for category_name, itypes in item_types.items():
        try:
            category = Category.objects.get(name=category_name)
        except Category.DoesNotExist:
            logger.error(f" [!] Category '{category_name}' does not exist. Did you forget to add it?")
            return

        for itype in itypes:
            name = itype['name']
            desc = itype['description']
            if ItemType.objects.filter(name=name, category=category).exists():
                logger.debug(f"! Item type '{name}' already exists in category '{category_name}'. Skipping.")
            else:
                ItemType.objects.create(name=name, category=category, description=desc)
                logger.debug(f" [+] Created item type '{name}' in category '{category_name}'.")
