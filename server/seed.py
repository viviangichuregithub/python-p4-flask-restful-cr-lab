# server/seed.py

from app import app, db
from models import Plant

with app.app_context():
    # Drop all tables and recreate (optional, fresh start)
    db.drop_all()
    db.create_all()

    # Sample plants
    plants = [
        Plant(name="Douglas Fir", image=None, price=25.0),
        Plant(name="Fiddle Leaf Fig", image=None, price=50.0),
        Plant(name="Snake Plant", image=None, price=15.0),
    ]

    db.session.add_all(plants)
    db.session.commit()
    print("Seed data inserted successfully!")
