from django_seed import Seed

from network.models import Post, User

seeder = Seed.seeder()

seeder.add_entity(User, 10, {"email": seeder.faker.email()})
seeder.add_entity(Post, 5)

inserted_pks = seeder.execute()
