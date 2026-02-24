from app import app
from extensions import db
from models import MenuItem

def seed_menu():
    """Seed the database with menu items"""
    with app.app_context():
        # Clear existing menu items
        MenuItem.query.delete()
        db.session.commit()
        
        menu_items = [
            # Main Dishes - الطواجن كلها و الفراخ و الملوخيه و البانيه
            {
                "name_ar": "محشي ورق عنب – طبق صغير",
                "name_en": "Stuffed Grape Leaves – Small",
                "description_ar": "طبق ورق عنب صغير متعمل بحب وطعم بيتي.",
                "description_en": "Small plate of homemade stuffed grape leaves.",
                "price": 150,
                "is_available": True,
                "image_urls": "",
                "category": "main"
            },
            {
                "name_ar": "فراخ مشوية",
                "name_en": "Grilled Chicken",
                "description_ar": "فراخ مشوية على تتبيلة خاصة وطعم مشبع 🔥",
                "description_en": "Grilled chicken with special seasoning and rich flavor.",
                "price": 350,
                "is_available": True,
                "image_urls": "",
                "category": "main"
            },
            {
                "name_ar": "ملوخية",
                "name_en": "Molokhia",
                "description_ar": "ملوخية خضرا طازة على الطريقة البيتي.",
                "description_en": "Fresh homemade Egyptian molokhia.",
                "price": 70,
                "is_available": True,
                "image_urls": "",
                "category": "main"
            },
            {
                "name_ar": "طاجن بامية باللحمة",
                "name_en": "Okra Casserole with Meat",
                "description_ar": "طاجن بامية باللحمة متسبك في الفرن وطعمه تقيل 👌",
                "description_en": "Oven-baked okra casserole with tender meat.",
                "price": 400,
                "is_available": True,
                "image_urls": "",
                "category": "main"
            },
            {
                "name_ar": "طاجن بصل باللحمة",
                "name_en": "Onion Casserole with Meat",
                "description_ar": "طاجن بصل باللحمة بطعم غني ومختلف.",
                "description_en": "Oven-baked onion casserole with seasoned meat.",
                "price": 350,
                "is_available": True,
                "image_urls": "",
                "category": "main"
            },
            {
                "name_ar": "طاجن رز معمر باللحمة",
                "name_en": "Baked Rice with Meat",
                "description_ar": "رز معمر كريمي باللحمة ومتسوّي في الفرن 😍",
                "description_en": "Creamy baked rice casserole with meat.",
                "price": 400,
                "is_available": True,
                "image_urls": "",
                "category": "main"
            },
            {
                "name_ar": "طاجن بطاطس باللحمة",
                "name_en": "Potato Casserole with Meat",
                "description_ar": "طاجن بطاطس باللحمة بطعم بيتي أصيل.",
                "description_en": "Homestyle potato casserole with meat.",
                "price": 350,
                "is_available": True,
                "image_urls": "",
                "category": "main"
            },
            {
                "name_ar": "بانيه مقلي – نصف كيلو",
                "name_en": "Fried Pane – Half Kilo",
                "description_ar": "بانيه مقلي مقرمش ودهبي 🔥",
                "description_en": "Crispy golden fried pane.",
                "price": 300,
                "is_available": True,
                "image_urls": "",
                "category": "main"
            },
            {
                "name_ar": "بانيه مقلي – كيلو",
                "name_en": "Fried Pane – One Kilo",
                "description_ar": "كيلو بانيه مقلي مشبع ومناسب للعيلة.",
                "description_en": "One kilo of crispy fried pane, perfect for families.",
                "price": 450,
                "is_available": True,
                "image_urls": "",
                "category": "main"
            },
            
            # Side Dishes - رز كبير و صغير و سمبوسك و سلطات كلها
            {
                "name_ar": "أرز بالشعرية – صغير",
                "name_en": "Rice with Vermicelli – Small",
                "description_ar": "طبق أرز بالشعرية بيتي.",
                "description_en": "Small plate of rice with vermicelli.",
                "price": 50,
                "is_available": True,
                "image_urls": "",
                "category": "side"
            },
            {
                "name_ar": "أرز بالشعرية – كبير",
                "name_en": "Rice with Vermicelli – Large",
                "description_ar": "طبق أرز بالشعرية حجم عائلي.",
                "description_en": "Large plate of rice with vermicelli.",
                "price": 80,
                "is_available": True,
                "image_urls": "",
                "category": "side"
            },
            {
                "name_ar": "سمبوسك لحمة – كيلو",
                "name_en": "Meat Samosa – 1 Kilo",
                "description_ar": "سمبوسك محشي لحمة مفرومة متبلة، مقرمش وطعم ولا أروع 🔥 مناسب للعزومات.",
                "description_en": "Crispy samosas stuffed with seasoned minced meat. Perfect for gatherings.",
                "price": 400,
                "is_available": True,
                "image_urls": "",
                "category": "side"
            },
            {
                "name_ar": "سمبوسك لحمة – نصف كيلو",
                "name_en": "Meat Samosa – Half Kilo",
                "description_ar": "نصف كيلو سمبوسك لحمة مقرمش ومحشي حشوة تقيلة 👌",
                "description_en": "Half kilo of crispy meat samosas with rich filling.",
                "price": 250,
                "is_available": True,
                "image_urls": "",
                "category": "side"
            },
            {
                "name_ar": "سمبوسك جبنة – كيلو",
                "name_en": "Cheese Samosa – 1 Kilo",
                "description_ar": "سمبوسك محشي جبنة سايحة بطعم غني ومقرمش 😍",
                "description_en": "Crispy samosas filled with rich melted cheese.",
                "price": 300,
                "is_available": True,
                "image_urls": "",
                "category": "side"
            },
            {
                "name_ar": "سمبوسك جبنة – نصف كيلو",
                "name_en": "Cheese Samosa – Half Kilo",
                "description_ar": "نصف كيلو سمبوسك جبنة، خفيف ومناسب لأي وقت.",
                "description_en": "Half kilo of crispy cheese samosas, perfect for any time.",
                "price": 200,
                "is_available": True,
                "image_urls": "",
                "category": "side"
            },
            {
                "name_ar": "طحينة",
                "name_en": "Tahini",
                "description_ar": "طحينة بيتي طعمها غني وكريمي، مثالية مع أي وجبة.",
                "description_en": "Homemade tahini with rich creamy flavor, perfect with any meal.",
                "price": 45,
                "is_available": True,
                "image_urls": "",
                "category": "side"
            },
            {
                "name_ar": "سلطة خضراء",
                "name_en": "Green Salad",
                "description_ar": "سلطة خضراء طازة ومنعشة، مناسبة بجانب أي طبق.",
                "description_en": "Fresh green salad, perfect as a side for any dish.",
                "price": 30,
                "is_available": True,
                "image_urls": "",
                "category": "side"
            },
            {
                "name_ar": "بابا غنوج",
                "name_en": "Baba Ganoush",
                "description_ar": "بابا غنوج بيتّي، طعمه مدخن ودهني شهي 🔥",
                "description_en": "Homemade smoky and creamy baba ganoush.",
                "price": 50,
                "is_available": True,
                "image_urls": "",
                "category": "side"
            },
            {
                "name_ar": "كلو سلو",
                "name_en": "Coleslaw",
                "description_ar": "سلطة كلو سلو طازة ومقرمشة، رائعة مع أي وجبة.",
                "description_en": "Fresh and crunchy coleslaw salad, perfect with any meal.",
                "price": 45,
                "is_available": True,
                "image_urls": "",
                "category": "side"
            },
            
            # Desserts - رز بالبن و ام علي و بسبوسه
            {
                "name_ar": "رز بلبن",
                "name_en": "Rice Pudding",
                "description_ar": "رز بلبن بيتي كريمي وحلو، مثالي للحلوى بعد أي وجبة 😍",
                "description_en": "Homemade creamy rice pudding, perfect dessert after any meal.",
                "price": 50,
                "is_available": True,
                "image_urls": "",
                "category": "dessert"
            },
            {
                "name_ar": "أم علي",
                "name_en": "Umm Ali",
                "description_ar": "أم علي بلدي، طعمه غني ومليان مكونات شهية 🔥",
                "description_en": "Traditional Umm Ali with rich, delicious ingredients.",
                "price": 50,
                "is_available": True,
                "image_urls": "",
                "category": "dessert"
            },
            {
                "name_ar": "بسبوسة",
                "name_en": "Basbousa",
                "description_ar": "بسبوسة طرية وحلوة، مشبعة وطعمها بيتّي أصيل 😍",
                "description_en": "Soft, sweet basbousa with authentic homemade flavor.",
                "price": 100,
                "is_available": True,
                "image_urls": "",
                "category": "dessert"
            }
        ]
        
        # Add all menu items
        for item_data in menu_items:
            item = MenuItem(**item_data)
            db.session.add(item)
        
        db.session.commit()
        print(f"✅ Successfully seeded {len(menu_items)} menu items!")
        
        # Show items by category
        categories = db.session.query(MenuItem.category).distinct().all()
        for category in categories:
            count = MenuItem.query.filter_by(category=category[0]).count()
            print(f"📋 {category[0]}: {count} items")

if __name__ == '__main__':
    seed_menu()
