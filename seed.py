from api_controllers import db, handle_file
from models import Provider
from constants import CentralMayorista, LaCaserita, Alvi, Lider, Jumbo


def create_providers():
    prov1 = Provider(name=CentralMayorista.name, url="central_mayorista.jpeg")
    prov2 = Provider(
        name=LaCaserita.name, url="la_caserita_m.png", description="Mayorista online"
    )
    prov3 = Provider(name=Alvi.name, url="alvi_m.jpeg", description="Club Mayorista")
    prov4 = Provider(name=Lider.name, url="lider.png", description="Lider")
    prov5 = Provider(name=Jumbo.name, url="jumbo.png", description="Jumbo")

    providers = [prov1, prov2, prov3, prov4, prov5]

    for prov in providers:
        db.session.add(prov)
    db.session.commit()
    return providers


def seed_all():
    db.drop_all()
    db.create_all()
    create_providers()
    handle_file("tmp/00_seed.csv")


if __name__ == "__main__":
    seed_all()
