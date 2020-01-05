from api_controllers import db, handle_file
from models import Provider

def create_providers():
    prov1 = Provider(name='Central Mayorista', url='central_mayorista.jpeg')
    prov2 = Provider(name='Walmart', url='walmart_m.jpeg')
    prov3 = Provider(name='La Caserita', url='la_caserita_m.png', description='Mayorista online')
    prov4 = Provider(name='Alvi', url='alvi_m.jpeg', description='Club Mayorista')

    providers = [prov1, prov2, prov3, prov4]

    for prov in providers:
        db.session.add(prov)
    db.session.commit()
    return providers

def seed_all():
    db.drop_all()
    db.create_all()
    providers = create_providers()
    handle_file('tmp/00_seed.csv')

if __name__ == '__main__':
    seed_all()