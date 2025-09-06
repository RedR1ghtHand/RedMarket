#!/usr/bin/env python

import os
import sys

import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'redmarket.settings')
django.setup()

from django.contrib.auth.hashers import make_password

from app_account.models import User


def create_test_users():
    users_data = [
        {
            'email': 'testemail1@tmail.com',
            'mc_username': 'Steve1',
            'password': 'test_S3CR3T'
        },
        {
            'email': 'testemail2@tmail.com',
            'mc_username': 'Steve2',
            'password': 'test_S3CR3T'
        },
        {
            'email': 'testemail3@tmail.com',
            'mc_username': 'Steve3',
            'password': 'test_S3CR3T'
        },
        {
            'email': 'testemail4@tmail.com',
            'mc_username': 'Steve4',
            'password': 'test_S3CR3T'
        },
        {
            'email': 'testemail5@tmail.com',
            'mc_username': 'Steve5',
            'password': 'test_S3CR3T'
        }
    ]
    
    created_users = []
    
    for user_data in users_data:
        if User.objects.filter(email=user_data['email']).exists():
            print(f"User with email {user_data['email']} already exists. Skipping...")
            continue
            
        if User.objects.filter(mc_username=user_data['mc_username']).exists():
            print(f"User with username {user_data['mc_username']} already exists. Skipping...")
            continue
        
        user = User.objects.create(
            email=user_data['email'],
            mc_username=user_data['mc_username'],
            password=make_password(user_data['password']),
            is_active=True
        )
        
        created_users.append(user)
        print(f"Created user: {user.email} ({user.mc_username})")
    
    print(f"\nSuccessfully created {len(created_users)} test users.")
    return created_users


if __name__ == '__main__':
    create_test_users()
