from product_categories.models import Category, Sub_category
from product_items.models import Product, ProductImage, ProductTag
from home.models import Homepage, Detail, Founder, Homepage_Images
from faker import Faker
import random
from accounts.models import User
from order.models import DeliveryLocation

fake = Faker()

data = {
    "Technology": {
        "Mobiles": [
            "Apple",
            "Samsung",
            "Google",
            "OnePlus",
            "Xiaomi",
            "Huawei",
            "Motorola",
            "Nokia",
            "LG",
            "Sony",
            "HTC",
            "BlackBerry",
            "Oppo",
            "Vivo",
            "Realme",
            "Micromax",
            "Lenovo",
        ],
        "Televisions": [
            "Sony",
            "Samsung",
            "LG",
            "TCL",
            "Vizio",
            "Hisense",
            "Panasonic",
            "Sharp",
            "Philips",
            "Sceptre",
            "Haier",
            "Toshiba",
            "Element",
            "Westinghouse",
            "Insignia",
            "JVC",
        ],
        "Laptops": [
            "Apple",
            "Dell",
            "Lenovo",
            "HP",
            "Acer",
            "Asus",
            "Microsoft",
            "Razer",
            "Alienware",
            "MSI",
            "Huawei",
            "LG",
            "Samsung",
            "Vaio",
        ],
        "Tablets": [
            "Apple",
            "Samsung",
            "Lenovo",
            "Huawei",
            "Amazon",
            "Microsoft",
            "Asus",
            "Google",
            "Sony",
            "LG",
            "Acer",
            "Xiaomi",
            "Alcatel",
            "TCL",
            "ZTE",
            "Nokia",
        ],
        "Smart Watches": [
            "Apple",
            "Samsung",
            "Fitbit",
            "Garmin",
            "Huawei",
            "Xiaomi",
            "Fossil",
            "Ticwatch",
            "Amazfit",
            "Polar",
            "Skagen",
            "Michael Kors",
            "Diesel",
            "Misfit",
            "Casio",
            "G-Shock",
        ],
    },
    "Furniture": {
        "Tables": [
            "Godrej Interio",
            "Durian",
            "Urban Ladder",
            "Woodsworth",
            "Home Centre",
        ],
        "Almirahs": [
            "Godrej Interio",
            "Durian",
            "Urban Ladder",
            "Woodsworth",
            "Home Centre",
        ],
        "Sofas": ["Urban Ladder", "Pepperfry", "Godrej Interio", "Durian", "Furny"],
        "Beds": [
            "Godrej Interio",
            "Durian",
            "Urban Ladder",
            "Woodsworth",
            "Home Centre",
        ],
        "Dining Tables": [
            "Godrej Interio",
            "Durian",
            "Urban Ladder",
            "Woodsworth",
            "Home Centre",
        ],
    },
    "Clothes": {
        "Jeans": ["Levi's", "Wrangler", "Lee", "Pepe Jeans", "Spykar"],
        "T-shirts": ["United Colors of Benetton", "Puma", "Adidas", "Nike", "Reebok"],
        "Lowers": ["Jockey", "Hanes", "Jack & Jones", "Zara", "H&M"],
        "Sarees": ["Chhabra 555", "Biba", "FabIndia", "W", "Mimosa"],
        "Kurtas": ["Manyavar", "Biba", "W", "Global Desi", "FabIndia"],
    },
}


def generate_price():
    return round(random.uniform(50, 1000), 2)


def generate_quantity():
    return random.randint(1, 100)


def generate_discount():
    return random.randint(10, 60)


def generate_description(word_len=10):
    return fake.sentence(nb_words=word_len)


def run():
    if User.objects.all().count() > 0:
        return

    def create_product(products, sub_category):
        sorting_number = 1
        rating = 1
        for product_name in products:
            if rating > 5:
                rating = 0
            kw = dict(
                title=f"{product_name}, {generate_description()}",
                description=generate_description(word_len=30),
                is_promoted=False if sorting_number % 2 == 0 else True,
                sorting_number=sorting_number,
                price=generate_price(),
                rating=rating,
                sub_category=sub_category,
                discount_pct=generate_discount(),
            )
            print("Product", kw)
            sorting_number += 1
            rating += 1
            product = Product.objects.create(**kw)

    def create_sub_category(sub_categories, category):
        sorting_number = 1
        for sub_category_name in sub_categories:
            kw = dict(
                name=sub_category_name,
                category=category,
                is_promoted=False if sorting_number % 2 == 0 else True,
                sorting_number=sorting_number,
            )
            print("Sub_category", kw)
            sorting_number += 1
            sub_cate = Sub_category.objects.create(**kw)
            create_product(
                products=sub_categories[sub_category_name], sub_category=sub_cate
            )

    def create_category():
        sorting_number = 1
        for category_name in data:
            kw = dict(
                name=category_name,
                is_promoted=False if sorting_number % 2 == 0 else True,
                sorting_number=sorting_number,
            )
            print("category", kw)
            sorting_number += 1
            cat = Category.objects.create(**kw)
            create_sub_category(sub_categories=data[category_name], category=cat)

    def create_homepage_image(homepage):
        for i in range(3):
            kw = dict(
                homepage=homepage,
                sorting_number=i,
            )
            Homepage_Images.objects.create(**kw)

    def create_homepage():
        kw = dict(
            title=generate_description(),
            description=generate_description(word_len=50),
        )
        homepage = Homepage.objects.create(**kw)
        create_homepage_image(homepage=homepage)

    def create_founder(detail):
        kw = dict(
            detail=detail,
            is_head=True,
            name="jayesh kaushik",
            profession="software engineer",
        )
        Founder.objects.create(**kw)

    def create_detail():
        kw = dict(
            instagram_link="https://instagram.com",
            facebook_link="https://facebook.com",
            twitter_link="https://twitter.com",
            youtube_link="https://youtube.com",
            about_us=generate_description(word_len=100),
            email="EcomBuy@gmail.com",
        )
        detail = Detail.objects.create(**kw)
        create_founder(detail)

    def create_user():
        kw = dict(
            first_name="jayesh",
            last_name="kaushik",
            username="jayesh kaushik",
            email="jayeshkaushik@gmail.com",
            mobile="9090909090",
            is_active=True,
            is_admin=True,
            is_staff=True,
            is_manager=True,
            is_superuser=True,
        )
        user = User.objects.create(**kw)
        user.set_password("0000")
        user.save()

    def create_home_data():
        create_homepage()
        create_detail()

    def create_delivery_locations():
        pincode = 110039
        for i in range(pincode, pincode + 6):
            kw = dict(
                pincode=i,
                is_active=True,
                delivery_charge=i - pincode,
            )
            print("delivery locations", kw)
            DeliveryLocation.objects.create(**kw)

    create_category()
    create_home_data()
    create_user()
    create_delivery_locations()


if __name__ == "__main__":
    run()
