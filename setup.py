from models import STORAGE, app
from models.branch import Branch


def create_super():
    with app.app_context():

        STORAGE.create_all()
        STORAGE.new(
            Branch(
                name="GLD 1",
                phone="080111222333",
                location="No 36 maken street, Ikeja , Lagos",
            )
        )
        STORAGE.new(
            Branch(
                name="GLD 2",
                phone="080111222333",
                location="No 23 isiba oluwo street, egbeda, Lagos",
            )
        )
        STORAGE.save()


create_super()
