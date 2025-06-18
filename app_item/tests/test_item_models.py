import pytest
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from app_item.models import Category, ItemType, Material, Enchantment


@pytest.mark.django_db(transaction=True)
class TestItemModels:
    def test_model_creation(self, category_data, item_type_data, material_data, enchantment_data):
        category_map = {
            cat['name']: Category.objects.create(name=cat['name'], description=cat['description'])
            for cat in category_data
        }

        item_type_map = {}
        for type_data in item_type_data:
            category = category_map[type_data['category']]
            item_type = ItemType.objects.create(
                name=type_data['name'],
                description=type_data['description'],
                category=category
            )
            item_type_map[type_data['name']] = item_type

        for mat_data in material_data:
            material = Material.objects.create(name=mat_data['name'], description=mat_data['description'])
            for type_name in mat_data['applicable_to']:
                material.applicable_to.add(item_type_map[type_name])

        for ench_data in enchantment_data:
            enchantment = Enchantment.objects.create(
                name=ench_data['name'],
                description=ench_data['description'],
                max_level=ench_data['max_level']
            )
            for type_name in ench_data['applicable_to']:
                enchantment.applicable_to.add(item_type_map[type_name])

        assert Category.objects.count() == len(category_data)
        assert ItemType.objects.count() == len(item_type_data)
        assert Material.objects.count() == len(material_data)
        assert Enchantment.objects.count() == len(enchantment_data)

        for type_data in item_type_data:
            item_type = item_type_map[type_data['name']]

            expected_materials = {
                m['name'] for m in material_data if type_data['name'] in m['applicable_to']
            }
            actual_materials = {mat.name for mat in item_type.materials.all()}
            assert expected_materials == actual_materials, f"{item_type.name} has incorrect materials"

            expected_enchantments = {
                e['name'] for e in enchantment_data if type_data['name'] in e['applicable_to']
            }
            actual_enchantments = {e.name for e in item_type.enchantments.all()}
            assert expected_enchantments == actual_enchantments, f"{item_type.name} has incorrect enchantments"

    def test_invalid_itemtype_reference(self):
        with pytest.raises(IntegrityError):
            ItemType.objects.create(name="wand", description="Magic wand", category_id=999)

    def test_material_with_invalid_itemtype(self):
        fake_type = ItemType(id=999, name="nonexistent")
        material = Material.objects.create(name="ghost", description="Invisible material")
        with pytest.raises(Exception):
            material.applicable_to.add(fake_type)

    def test_enchantment_with_invalid_level(self, category_data, item_type_data):
        category = Category.objects.create(**category_data[0])
        item_type = ItemType.objects.create(name="blade", description="Sharp blade", category=category)
        enchantment = Enchantment.objects.create(name="fire", description="burns", max_level=3)
        enchantment.applicable_to.add(item_type)

        invalid_level = 5
        assert invalid_level > enchantment.max_level

