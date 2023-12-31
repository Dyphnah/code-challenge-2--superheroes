from models import Hero, Power, HeroPower, db
from app import app
import random
from faker import Faker

with app.app_context():
    Hero.query.delete()
    Power.query.delete()
    HeroPower.query.delete()
    db.session.commit()

    fake = Faker()

    powers = ['stretch', "super_speed", "super_strength", "thunder", "fistman"]
    s_names = ['elastic', "flashy", "thor", "thunder_bolt", "the_fister"]

    power_list = []
    for item in powers:
        existing_power = Power.query.filter_by(name=item).first()
        if not existing_power:
            power = Power(name=item, description=fake.sentence())
            power_list.append(power)
            db.session.add(power)
            db.session.commit()

    heroes_list = []
    for person in range(10):
        hero = Hero(name=fake.name(), super_name=random.choice(s_names))
        heroes_list.append(hero)
        db.session.add(hero)
        db.session.commit()

    for hp in range(10):
        try:
            hero_powers = HeroPower(
                strength=random.choice(['Strong', 'Weak', 'Average']),
                hero_id=random.choice(heroes_list).id,
                power_id=random.choice(power_list).id
            )
            db.session.add(hero_powers)
            db.session.commit()
            print(f"Successfully added HeroPower: {hero_powers.to_dict()}")
        except Exception as e:
            print(f"Error adding HeroPower: {e}")
            import traceback
            traceback.print_exc()
