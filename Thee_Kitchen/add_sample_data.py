from app import app
from models import MenuItem, db
from extensions import db

def add_sample_menu_items():
    with app.app_context():
        # Check if items already exist
        if MenuItem.query.first():
            print("Menu items already exist!")
            return
        
        # Sample menu items
        items = [
            MenuItem(
                name_ar="كبسة الدجاج",
                name_en="Chicken Kabsa",
                description_ar="طبق تقليدي شهير من الدجاج مع الأرز البسمتي والتوابل العربية",
                description_en="Traditional famous dish of chicken with basmati rice and Arabic spices",
                price=120.0,
                category="main"
            ),
            MenuItem(
                name_ar="مندي لحم",
                name_en="Mandi Lamb",
                description_ar="لحم ضأن مطهو ببطء على الفحم مع أرز معطر",
                description_en="Slow-cooked lamb on charcoal with fragrant rice",
                price=150.0,
                category="main"
            ),
            MenuItem(
                name_ar="سمبوسك خضار",
                name_en="Vegetable Samosa",
                description_ar="معجنات مقرمشة محشوة بالخضار المتبلة",
                description_en="Crispy pastries filled with seasoned vegetables",
                price=25.0,
                category="side"
            ),
            MenuItem(
                name_ar="سلطة عربية",
                name_en="Arabic Salad",
                description_ar="سلطة طازجة بالخضار الموسمية وتوابل السماق",
                description_en="Fresh salad with seasonal vegetables and sumac spices",
                price=30.0,
                category="side"
            ),
            MenuItem(
                name_ar="أم علي",
                name_en="Um Ali",
                description_ar="حلوى مصرية تقليدية بالكريم والتمر والمكسرات",
                description_en="Traditional Egyptian dessert with cream, dates and nuts",
                price=35.0,
                category="dessert"
            ),
            MenuItem(
                name_ar="كنافة بالجبن",
                name_en="Kunafa with Cheese",
                description_ar="كنافة مقرمشة بالجبن والشرق الحلو",
                description_en="Crispy kunafa with cheese and sweet syrup",
                price=40.0,
                category="dessert"
            )
        ]
        
        # Add items to database
        for item in items:
            db.session.add(item)
        
        db.session.commit()
        print(f"Added {len(items)} sample menu items!")

if __name__ == "__main__":
    add_sample_menu_items()
