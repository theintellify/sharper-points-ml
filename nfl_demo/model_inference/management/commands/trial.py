from model_inference.models import play_by_play
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        # Since the CSV headers match the model fields,
        # you only need to provide the file's path (or a Python file object)
        insert_count = play_by_play.objects.from_csv('/var/www/html/sharperpoints/nfl_demo/model_inference/2023_2024.csv')
        print("{} records inserted".format(insert_count))
