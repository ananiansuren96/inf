import os
import django
from django.test import Client

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'infomax.settings')
django.setup()

from news.models import Category, Article
from users.models import CustomUser

def verify():
    print("Verifying...")
    
    # Create User
    user, created = CustomUser.objects.get_or_create(username='testuser', email='test@example.com')
    if created:
        user.set_password('password')
        user.save()
        print("User created.")
    
    # Create Category
    cat, created = Category.objects.get_or_create(name='World', slug='world')
    print("Category created.")

    # Create Article
    article, created = Article.objects.get_or_create(
        title='Test Article',
        slug='test-article',
        category=cat,
        author=user,
        content='<p>This is a test article content.</p>',
        is_published=True
    )
    print("Article created.")

    # Test Views
    c = Client()
    
    # Home
    response = c.get('/')
    print(f"Home: {response.status_code}")
    assert response.status_code == 200
    
    # Category
    response = c.get('/category/world/')
    print(f"Category: {response.status_code}")
    assert response.status_code == 200

    # Article
    response = c.get('/article/test-article/')
    print(f"Article: {response.status_code}")
    assert response.status_code == 200

    # Sitemap
    response = c.get('/sitemap.xml')
    print(f"Sitemap: {response.status_code}")
    assert response.status_code == 200

    # Robots
    response = c.get('/robots.txt')
    print(f"Robots: {response.status_code}")
    assert response.status_code == 200

    # Sorting
    response = c.get('/category/world/?sort=popular')
    print(f"Sorting (Popular): {response.status_code}")
    assert response.status_code == 200

    print("Verification Complete!")

if __name__ == '__main__':
    verify()
