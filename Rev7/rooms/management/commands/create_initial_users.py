from django.core.management.base import BaseCommand
from rooms.models import CustomUser

class Command(BaseCommand):
    help = 'Create initial users for Hotel Snow PMS'

    def handle(self, *args, **options):
        users_to_create = [
            {
                'username': 'superadmin',
                'password': 'snow2024!',
                'email': 'super@hotelsnow.com',
                'user_type': 'SUPER',
                'is_superuser': True,
                'is_staff': True,
                'first_name': 'Super',
                'last_name': 'Admin'
            },
            {
                'username': 'admin',
                'password': 'admin2024!',
                'email': 'admin@hotelsnow.com',
                'user_type': 'ADMIN',
                'is_staff': True,
                'first_name': 'Hotel',
                'last_name': 'Admin'
            },
            {
                'username': 'frontdesk',
                'password': 'front2024!',
                'email': 'frontdesk@hotelsnow.com',
                'user_type': 'MEMBER',
                'first_name': 'Front',
                'last_name': 'Desk'
            }
        ]

        for user_data in users_to_create:
            username = user_data['username']
            if not CustomUser.objects.filter(username=username).exists():
                user = CustomUser.objects.create_user(
                    username=user_data['username'],
                    password=user_data['password'],
                    email=user_data['email'],
                    user_type=user_data['user_type'],
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name']
                )
                
                if user_data.get('is_superuser'):
                    user.is_superuser = True
                    user.is_staff = True
                    user.save()
                elif user_data.get('is_staff'):
                    user.is_staff = True
                    user.save()
                
                self.stdout.write(
                    self.style.SUCCESS(f'Created user: {username} ({user_data["user_type"]})')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'User already exists: {username}')
                )

        self.stdout.write(
            self.style.SUCCESS('\nInitial users setup completed!')
        )
        self.stdout.write('Login credentials:')
        self.stdout.write('- superadmin / snow2024! (Super User)')
        self.stdout.write('- admin / admin2024! (Admin User)')
        self.stdout.write('- frontdesk / front2024! (Member User)')