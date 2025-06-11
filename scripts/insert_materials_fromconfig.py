import json
import logging
from app_item.models import Material, ItemType


logger = logging.getLogger('script')

with open('config/item_materials.json') as f:
    materials = json.load(f)


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
    for material_data in materials:
        name = material_data["name"]
        description = material_data.get("description", "")
        applicable_to = material_data["applicable_to"]

        material, created = Material.objects.get_or_create(name=name, description=description)

        if created:
            logger.debug(f" [+] Created material: {material.name}")
        else:
            logger.debug(f"! Material already exists: {material.name}")

        for itype_name in applicable_to:
            try:
                item_type = ItemType.objects.get(name=itype_name)
                if not material.applicable_to.filter(id=item_type.id).exists():
                    material.applicable_to.add(item_type)
                    logger.debug(f"+ Linked '{itype_name}' to material '{material.name}'")
                else:
                    logger.debug(f"! '{itype_name}' already linked to material '{material.name}'")
            except ItemType.DoesNotExist:
                logger.error(f" [!] ItemType '{itype_name}' does not exist. Please check your item types!")

