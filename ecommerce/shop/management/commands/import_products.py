import csv
from django.core.management.base import BaseCommand
from shop.models import Product, Category

class Command(BaseCommand):
    help = 'Load products from a CSV file'

    def handle(self, *args, **kwargs):
        with open('C:/Users/DELL/Desktop/CalynaProject/Ecommerce/ecommerce/shop/products1.csv', mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for row in reader:
                # Vérifiez si la catégorie est présente
                if row['category']:
                    category, created = Category.objects.get_or_create(name=row['category'])
                else:
                    self.stdout.write(self.style.WARNING(f"Category missing for product {row['name']}, skipping..."))
                    continue

                Product.objects.create(
                    title=row['name'],
                    price=row['price'],
                    description=row['description'],
                    category=category,
                    image=row['image;']  # Utilisation de 'image;' si nécessaire
                )

            self.stdout.write(self.style.SUCCESS('Products imported successfully!'))
