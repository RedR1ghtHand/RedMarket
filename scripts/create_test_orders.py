#!/usr/bin/env python

import os
import random
import sys
from decimal import Decimal

import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'redmarket.settings')
django.setup()

from app_account.models import User
from app_item.models import Enchantment, ItemType, Material
from app_order.models import Order


def get_weapon_tool_item_types():
    item_types = ItemType.objects.filter(
        name__in=['axe', 'sword', 'pickaxe']
    )
    return list(item_types)

def get_applicable_materials(item_type):
    materials = Material.objects.filter(applicable_to=item_type)
    return list(materials)

def get_applicable_enchantments(item_type):
    enchantments = Enchantment.objects.filter(applicable_to=item_type)
    return list(enchantments)

def create_random_order(user, item_type):
    materials = get_applicable_materials(item_type)
    if not materials:
        return None
    material = random.choice(materials)
    quantity = random.randint(1, 100)
    price_per_unit = random.randint(100, 1000)
    total_price = Decimal(price_per_unit * quantity)
    order = Order.objects.create(
        item_type=item_type,
        material=material,
        quantity=quantity,
        price=total_price,
        created_by=user
    )
    enchantments = get_applicable_enchantments(item_type)
    if enchantments:
        num_enchantments = random.randint(0, min(3, len(enchantments)))
        selected_enchantments = random.sample(enchantments, num_enchantments)
        for enchantment in selected_enchantments:
            level = random.randint(1, enchantment.max_level)
            order.enchantments.add(enchantment, through_defaults={'level': level})
    return order

def create_test_orders():
    test_users = User.objects.filter(
        email__startswith='testemail',
        mc_username__startswith='Steve'
    ).order_by('mc_username')
    if not test_users.exists():
        print("No test users found. Please run create_test_users.py first.")
        return
    item_types = get_weapon_tool_item_types()
    if not item_types:
        print("No weapon/tool item types found. Please ensure the database is populated with item data.")
        return
    total_orders_created = 0
    for user in test_users:
        print(f"\nCreating orders for user: {user.mc_username} ({user.email})")
        user_orders_created = 0
        for i in range(10000):
            item_type = random.choice(item_types)
            order = create_random_order(user, item_type)
            if order:
                user_orders_created += 1
                total_orders_created += 1
                if user_orders_created % 20 == 0:
                    print(f"  Created {user_orders_created} orders...")
        print(f"  Total orders created for {user.mc_username}: {user_orders_created}")
    print(f"\nSuccessfully created {total_orders_created} test orders across {test_users.count()} users.")

if __name__ == '__main__':
    create_test_orders()
