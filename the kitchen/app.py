from flask import Flask, render_template
from flask_cors import CORS
from config import Config  # Back to original config
from extensions import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Configure CORS to support credentials
    CORS(app, 
         supports_credentials=True,
         origins=["https://thekitchen.fly.dev", "http://localhost:5000", "http://127.0.0.1:5000"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         allow_headers=["Content-Type", "Authorization"])

    db.init_app(app)

    # Import models so SQLAlchemy sees them before create_all / queries
    import models  # noqa: F401

    # API Blueprints
    from routes.products_api import products_api
    from routes.auth_api import auth_api

    app.register_blueprint(products_api, url_prefix="/api")
    app.register_blueprint(auth_api, url_prefix="/api")

    @app.cli.command("init-db")
    def init_db():
        """Create database tables."""
        with app.app_context():
            db.create_all()
        print("✅ Database tables created.")

    @app.cli.command("seed-db")
    def seed_db():
        """Seed database with sample products."""
        from models import Product

        with app.app_context():
            db.create_all()

            if Product.query.first():
                print("ℹ️ Products already exist. Skipping seed.")
                return

            samples = [
                Product(
                    name_ar="فتة لحمة بلدي",
                    name_en="Beef Fatta",
                    description_ar="لحمة بلدي مستوية على النار الهادي مع رز أبيض وعيش محمّص وصوص ثومي.",
                    description_en="Slow-cooked local beef with rice, toasted bread, and homemade garlic sauce.",
                    price=250,
                    prep_time_minutes=45,
                    is_available=True,
                    image_url="path/to/image.jpg",
                ),
                Product(
                    name_ar="تبولة شامية",
                    name_en="Tabbouleh",
                    description_ar="بقدونس فريش، طماطم، برغل ناعم، مع عصير ليمون وزيت زيتون بكر.",
                    description_en="Fresh parsley, tomato, fine bulgur with lemon juice and extra virgin olive oil.",
                    price=90,
                    prep_time_minutes=20,
                    is_available=True,
                    image_url="path/to/image.jpg",
                ),
                Product(
                    name_ar="أم علي",
                    name_en="Om Ali",
                    description_ar="رقائق جلاش بالحليب والمكسرات، مخبوزة لحد ما توصل لأحلى لون وطعم.",
                    description_en="Flaky pastry with milk and nuts baked to golden perfection.",
                    price=130,
                    prep_time_minutes=30,
                    is_available=True,
                    image_url="path/to/image.jpg",
                ),
            ]

            db.session.add_all(samples)
            db.session.commit()
            print("✅ Seeded sample products.")

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/signup")
    def signup():
        return render_template("signup.html")

    @app.route("/signin")
    def signin():
        return render_template("signin.html")

    @app.route("/forgot-password")
    def forgot_password():
        return render_template("forgot_password.html")

    @app.route("/menu")
    def menu():
        return render_template("menu.html")

    @app.route("/cart")
    def cart():
        return render_template("cart.html")

    @app.route("/admin")
    def admin_panel():
        return render_template("admin.html")

    return app


if __name__ == "__main__":
    application = create_app()
    application.run(debug=True)