from django.core.management.base import BaseCommand
from products.models import Category, Product
from faker import Faker
import random
import requests
from django.core.files.base import ContentFile

fake = Faker()

class Command(BaseCommand):
    help = 'Generate test data for products'

    def handle(self, *args, **kwargs):
        # Creating categories
        categories = ['Electronics', 'Books', 'Clothing', 'Home Appliances']
        for name in categories:
            Category.objects.get_or_create(name=name, slug=name.lower())

        # Creating products with images
        for _ in range(10):
            category = Category.objects.order_by('?').first()
            product = Product.objects.create(
                name=fake.word().capitalize(),
                description=fake.text(max_nb_chars=200),
                price=round(random.uniform(10.0, 100.0), 2),
                category=category
            )

            # Adding a random image
            image_url = "https://picsum.photos/640/426"
            response = requests.get(image_url)
            if response.status_code == 200:
                if 'image' in response.headers.get('Content-Type', ''):
                    try:
                        product.image.save(
                            f'{fake.word()}.jpg',
                            ContentFile(response.content),
                            save=True
                        )
                        print("Image saved successfully!")
                    except Exception as e:
                            print(f"Error saving image: {e}")
                            traceback.print_exc()
                else:
                    print("Invalid content type:", response.headers.get('Content-Type', ''))
            else:
                print(f"Failed to fetch image. Status code: {response.status_code}")

        self.stdout.write(self.style.SUCCESS('Successfully added test data!'))