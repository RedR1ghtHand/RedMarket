#!/usr/bin/env python

import os
import sys

import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'redmarket.settings')
django.setup()

from app_account.models import User
from app_order.models import Order


def cleanup_test_data():
    test_users = User.objects.filter(
        email__startswith='testemail',
        mc_username__startswith='Steve'
    ).order_by('mc_username')
    
    if not test_users.exists():
        print("No test users found to delete.")
        return
    
    print(f"Found {test_users.count()} test users to delete:")
    for user in test_users:
        print(f"  - {user.mc_username} ({user.email})")
    
    total_orders = Order.objects.filter(created_by__in=test_users).count()
    print(f"\nThis will also delete {total_orders} associated orders.")
    
    confirm = input("\nConfirm deletion? (yes/no): ")
    if confirm.lower() not in ['yes', 'y']:
        print("Deletion cancelled.")
        return
    
    deleted_count = 0
    for user in test_users:
        username = user.mc_username
        email = user.email
        user.delete()
        deleted_count += 1
        print(f"Deleted user: {username} ({email})")
    
    print(f"\nSuccessfully deleted {deleted_count} test users and their associated data.")


if __name__ == '__main__':
    cleanup_test_data()
