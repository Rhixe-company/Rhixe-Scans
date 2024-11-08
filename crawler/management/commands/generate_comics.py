import json
from pprint import pprint

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "Generates transactions for testing"

    def handle(self, *args, **options):
        def save_chapter():
            base = settings.BASE_DIR
            chapters_file = str(base / "chapters2.json")
            with open(chapters_file) as f:
                chapters_data = json.load(f)
                for c in chapters_data:
                    pprint(
                        {
                            # "chapter": c,
                            "updated_at": c["updated_at"],
                        },
                    )

        def save_comic():
            base = settings.BASE_DIR
            comics_file = str(base / "comics.json")
            with open(comics_file) as f:
                comics_data = json.load(f)
                for c in comics_data:
                    pprint(
                        {
                            # "comic": c,
                            "description": c["description"],
                        },
                    )

        save_comic()
        # save_chapter()
