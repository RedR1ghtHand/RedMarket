#!/usr/bin/env python

import os
import random
import sys
import time
from decimal import Decimal

import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'redmarket.settings')
django.setup()

from django.db import connection, transaction

from app_account.models import User
from app_item.models import Enchantment, ItemType, Material
from app_order.models import Order, OrderEnchantment

ORDERS_PER_USER = 10000
BATCH_SIZE = 100 

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

def preload_item_data():
    """Preload all materials and enchantments for each item type to avoid repeated queries"""
    item_types = get_weapon_tool_item_types()
    item_data = {}
    
    for item_type in item_types:
        materials = get_applicable_materials(item_type)
        enchantments = get_applicable_enchantments(item_type)
        item_data[item_type] = {
            'materials': materials,
            'enchantments': enchantments
        }
    
    return item_data

def create_random_order(user, item_type, item_data):
    materials = item_data[item_type]['materials']
    if not materials:
        return None, 0
    
    material = random.choice(materials)
    quantity = random.randint(1, 100)
    price_per_unit = random.randint(10, 10000)
    
    db_start_time = time.time()
    order = Order.objects.create(
        item_type=item_type,
        material=material,
        quantity=quantity,
        price=price_per_unit,
        created_by=user
    )
    
    enchantments = item_data[item_type]['enchantments']
    if enchantments:
        num_enchantments = random.randint(0, min(3, len(enchantments)))
        selected_enchantments = random.sample(enchantments, num_enchantments)
        for enchantment in selected_enchantments:
            level = random.randint(1, enchantment.max_level)
            order.enchantments.add(enchantment, through_defaults={'level': level})
    db_end_time = time.time()
    
    return order, db_end_time - db_start_time

def create_orders_bulk(user, item_data, num_orders=1000):
    """Create multiple orders in bulk for better performance"""
    orders_to_create = []
    enchantments_to_create = []
    
    item_types = list(item_data.keys())
    
    for _ in range(num_orders):
        item_type = random.choice(item_types)
        materials = item_data[item_type]['materials']
        if not materials:
            continue
            
        material = random.choice(materials)
        quantity = random.randint(1, 100)
        price_per_unit = random.randint(10, 10000)
        
        order = Order(
            item_type=item_type,
            material=material,
            quantity=quantity,
            price=price_per_unit,
            created_by=user
        )
        orders_to_create.append(order)
    
    db_start_time = time.time()
    
    with transaction.atomic():
        Order.objects.bulk_create(orders_to_create)
        
        for i, order in enumerate(orders_to_create):
            item_type = order.item_type
            enchantments = item_data[item_type]['enchantments']
            if enchantments:
                num_enchantments = random.randint(0, min(3, len(enchantments)))
                selected_enchantments = random.sample(enchantments, num_enchantments)
                for enchantment in selected_enchantments:
                    level = random.randint(1, enchantment.max_level)
                    enchantments_to_create.append(OrderEnchantment(
                        order=order,
                        enchantment=enchantment,
                        level=level
                    ))
        
        if enchantments_to_create:
            OrderEnchantment.objects.bulk_create(enchantments_to_create)
    
    db_end_time = time.time()
    
    return len(orders_to_create), db_end_time - db_start_time

def create_test_orders():
    script_start_time = time.time()
    
    print(" Preloading item data...")
    preload_start = time.time()
    item_data = preload_item_data()
    preload_time = time.time() - preload_start
    print(f" Preloaded data in {preload_time:.4f}s")
    
    test_users = User.objects.filter(
        email__startswith='testemail',
        mc_username__startswith='Steve'
    ).order_by('mc_username')
    if not test_users.exists():
        print("No test users found. Please run create_test_users.py first.")
        return
    
    item_types = list(item_data.keys())
    if not item_types:
        print("No weapon/tool item types found. Please ensure the database is populated with item data.")
        return
    
    total_orders_created = 0
    total_db_time = 0
    batch_start_time = None
    batch_orders_count = 0
    
    orders_per_user = ORDERS_PER_USER
    batch_size = BATCH_SIZE
    
    for user in test_users:
        print(f"\nCreating orders for user: {user.mc_username} ({user.email})")
        user_orders_created = 0
        user_db_time = 0
        
        num_batches = (orders_per_user + batch_size - 1) // batch_size
        
        for batch_num in range(num_batches):
            if batch_orders_count == 0:
                batch_start_time = time.time()

            orders_this_batch = min(batch_size, orders_per_user - user_orders_created)
            orders_created, db_time = create_orders_bulk(user, item_data, orders_this_batch)
            
            if orders_created > 0:
                user_orders_created += orders_created
                total_orders_created += orders_created
                total_db_time += db_time
                user_db_time += db_time
                batch_orders_count += orders_created
                
                batch_end_time = time.time()
                batch_total_time = batch_end_time - batch_start_time
                avg_db_time_per_order = total_db_time / total_orders_created
                avg_total_time_per_order = batch_total_time / orders_created
                
                print(f"  Created {user_orders_created}/{orders_per_user} orders...")
                print(f"  BATCH STATS (Last {orders_created} orders):")
                print(f"     • Total DB time: {total_db_time:.4f}s")
                print(f"     • Total script time: {batch_total_time:.4f}s")
                print(f"     • Average DB time per order: {avg_db_time_per_order:.4f}s")
                print(f"     • Average total time per order: {avg_total_time_per_order:.4f}s")
                print(f"     • DB queries executed: {len(connection.queries)}")
                
                batch_start_time = time.time()
                batch_orders_count = 0
        
        print(f"  Total orders created for {user.mc_username}: {user_orders_created}")
        print(f"  User DB time: {user_db_time:.4f}s")
    
    script_end_time = time.time()
    total_script_time = script_end_time - script_start_time
    
    expected_total = test_users.count() * ORDERS_PER_USER
    print(f"\nFINAL STATS:")
    print(f"   • Total orders created: {total_orders_created}/{expected_total}")
    print(f"   • Total script time: {total_script_time:.4f}s")
    print(f"   • Total DB time: {total_db_time:.4f}s")
    print(f"   • Average DB time per order: {total_db_time/total_orders_created:.4f}s")
    print(f"   • Average total time per order: {total_script_time/total_orders_created:.4f}s")
    print(f"   • Total DB queries executed: {len(connection.queries)}")
    print(f"   • DB efficiency: {(total_db_time/total_script_time)*100:.2f}% of total time")
    print(f"   • Orders per user: {ORDERS_PER_USER}")

if __name__ == '__main__':
    create_test_orders()
