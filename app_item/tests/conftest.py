import pytest


@pytest.fixture
def category_data():
    return [
        {"name": "combat", "description": "Offensive equipment for combat"},
        {"name": "armor", "description": "Items worn for protection"}
    ]


@pytest.fixture
def item_type_data():
    return [
        {"name": "sword", "description": "A melee weapon used for attacking", "category": "combat"},
        {"name": "helmet", "description": "A piece of armor for the head", "category": "armor"},
        {"name": "chestplate", "description": "A piece of armor for the torso", "category": "armor"}
    ]


@pytest.fixture
def material_data():
    return [
        {
            "name": "iron",
            "description": "Metal.",
            "applicable_to": [
                "sword",
                "helmet",
                "chestplate",
            ]
        },
        {
            "name": "wood",
            "description": "Just a wood, nothing special",
            "applicable_to": ["sword"]
        },
        {
            "name": "leather",
            "description": "Comfort.",
            "applicable_to": [
                "helmet",
                "chestplate",
            ]
        },
    ]


@pytest.fixture
def enchantment_data():
    return [
        {
            "name": "mending",
            "description": "Repairs the item when gaining XP orbs.",
            "max_level": 1,
            "applicable_to": [
                "sword",
                "helmet",
                "chestplate"
            ]
        },
        {
            "name": "Protection",
            "description": "Reduces most types of damage by 4% per level.",
            "max_level": 4,
            "applicable_to": [
                "helmet",
                "chestplate"
            ]
        },
        {
            "name": "Sharpness",
            "description": "Increases weapon damage.",
            "max_level": 5,
            "applicable_to": ["sword"]
        },
    ]
