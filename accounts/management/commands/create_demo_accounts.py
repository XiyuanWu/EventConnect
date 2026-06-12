from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from accounts.models import Profile


class Command(BaseCommand):
    help = "Create the default admin account for project presentation."

    def handle(self, *args, **options):
        admin_user = self._upsert_user(
            username="admin",
            email="admin@admin.com",
            password="123",
            is_staff=True,
            is_superuser=True,
        )
        self._upsert_profile(
            user=admin_user,
            display_name="Demo Admin",
            major="Administration",
            interests="User management and platform setup",
            bio="Default administrator account for the EventConnect demo.",
        )

        self.stdout.write(self.style.SUCCESS("Default admin account is ready."))
        self.stdout.write("Admin: username=admin password=123")

    def _upsert_user(self, username, email, password, is_staff, is_superuser):
        user, created = User.objects.get_or_create(
            username=username,
            defaults={"email": email},
        )
        user.email = email
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.set_password(password)
        user.save()

        action = "Created" if created else "Updated"
        self.stdout.write(f"{action} user: {username}")
        return user

    def _upsert_profile(self, user, display_name, major, interests, bio):
        profile, _ = Profile.objects.get_or_create(user=user)
        profile.display_name = display_name
        profile.major = major
        profile.interests = interests
        profile.bio = bio
        profile.save()
