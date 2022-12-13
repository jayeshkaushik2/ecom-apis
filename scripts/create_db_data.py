from product_categories.models import Category, Sub_category
from product_items.models import Product

data = {
    "Technology": ["Mobiles", "Air Conditioners", "Laptops"],
    "Clothes": ["Jeans", "T-shirts", "Lowers"],
    "Furnitures": ["Tables", "Almirahs"],
}


def clear_data():
    Category.objects.all().delete()
    Sub_category.objects.all().delete()
    Product.objects.all().delete()


def create_data():
    def create_product(sub_category):
        rating = 1
        price = 12000
        for i in range(10):
            if rating > 5:
                rating = 1
            Product.objects.create(
                sub_category=sub_category,
                title=f"{sub_category.category.name}-{sub_category.name} title for {sub_category.name}-{i}.",
                description=f"{sub_category.category.name}-{sub_category.name} is a placeholder text commonly used to demonstrate the visual form of a document or a typeface without relying on meaningful content. Lorem ipsum may be used as a placeholder title for {sub_category.name}-{i}.",
                is_promoted=True,
                sorting_number=i,
                price=price,
                rating=rating,
                discount_pct=20,
            )
            rating += 1
            price += 1000

    def create_sub_category(sub_categories: list, category) -> None:
        j = 0
        for sub_cate in data[category.name]:
            sub_category = Sub_category.objects.create(
                category=category,
                name=sub_cate,
                is_promoted=True,
                sorting_number=j,
            )
            create_product(sub_category)

    i = 1
    for category_name in data:
        category = Category.objects.create(
            name=category_name, is_promoted=True, sorting_number=i
        )
        create_sub_category(data[category_name], category=category)
        i += 1


def run():
    clear_data()
    create_data()
