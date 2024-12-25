import random
from PIL import ImageDraw, Image
from io import BytesIO
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile

from warehouse_app.models import City, Store, Product, ProductPhoto, ProductStock, ProductViewCounter, UserProfile


class Command(BaseCommand):
    help = "Fill the database with related test data"

    def generate_image(self, text):
        """Генерация простого изображения с текстом."""
        img = Image.new('RGB', (200, 200),
                        color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        draw = ImageDraw.Draw(img)
        draw.text((10, 90), text, fill=(255, 255, 255))

        # Сохранение изображения в память
        image_io = BytesIO()
        img.save(image_io, format='PNG')
        image_io.seek(0)
        return image_io


    def handle(self, *args, **kwargs):
        # Удаление всех данных (если нужно)
        UserProfile.objects.all().delete()
        ProductViewCounter.objects.all().delete()
        ProductStock.objects.all().delete()
        ProductPhoto.objects.all().delete()
        Product.objects.all().delete()
        Store.objects.all().delete()
        City.objects.all().delete()


        city_model_data = []
        counter = 0
        city_list = ['Astana', 'Almaty', 'Shymkent', 'Oral', 'Aktau',
                     'Atyrau', 'Taraz', 'Semey', 'Oskemen', 'Kostanay',
                     'Kokshetau', 'Karagandy', 'Turkestan', 'Aktobe', 'Petropavl']
        for city in city_list:
            counter += 1
            new_city_model_ins = City.objects.create(name=city)
            city_model_data.append(new_city_model_ins)
        self.stdout.write(self.style.SUCCESS(f"Successfully filled City table with test data. Row count: {counter}"))


        store_model_data = []
        counter = 0
        for city_model in city_model_data:
            for _ in range(random.randint(3, 10)):
                counter += 1
                new_store_model_ins = Store.objects.create(name=f"store_{counter}", city=city_model)
                store_model_data.append(new_store_model_ins)
        self.stdout.write(self.style.SUCCESS(f"Successfully filled Store table with test data. Row count: {counter}"))


        product_model_data = []
        counter = 0
        for i in range(100):
            counter += 1
            new_product_model_ins = Product.objects.create(name=f"product_{counter}",
                                                           description=f"description_{counter}",
                                                           default_price=random.randint(10, 100000))
            product_model_data.append(new_product_model_ins)
        self.stdout.write(self.style.SUCCESS(f"Successfully filled Product table with test data. Row count: {counter}"))


        product_photo_model_data = []
        counter = 0
        for product_model in product_model_data:
            for _ in range(random.randint(3, 8)):
                counter += 1
                image = self.generate_image(f"product_photo_{counter}")
                new_product_photo_model_ins = ProductPhoto.objects.create(
                    product=product_model,
                    city=random.choice(city_model_data),
                )
                new_product_photo_model_ins.photo.save(f"product_photo_{counter}.png",
                                                       ContentFile(image.getvalue()), save=True)
                product_photo_model_data.append(new_product_photo_model_ins)
        self.stdout.write(self.style.SUCCESS(f"Successfully filled ProductPhoto table with test data. Row count: {counter}"))


        product_stock_model_data = []
        counter = 0
        for store_model in store_model_data:
            for product_model in product_model_data:
                counter += 1
                new_product_stock_model_ins = ProductStock.objects.create(
                    product=product_model,
                    store=store_model,
                    price=random.randint(10, 100000),
                    quantity=random.randint(0, 100),
                )
                product_stock_model_data.append(new_product_stock_model_ins)

        self.stdout.write(self.style.SUCCESS(f"Successfully filled ProductStock table with test data. Row count: {counter}"))
