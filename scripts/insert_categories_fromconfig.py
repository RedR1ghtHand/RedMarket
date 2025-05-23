import json
import logging

from app_item.models import Category

logger = logging.getLogger('script')

with open('config/item_categories.json') as f:
    categories = json.load(f)


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
    for category in categories:
        name = category["name"]
        description = category["description"]

        obj, created = Category.objects.get_or_create(name=name, defaults={"description": description})
        if created:
            logger.debug(f" [+] Created category: {name}")
        else:
            logger.debug(f"! Category already exists: {name}")


