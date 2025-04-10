# your_app/management/commands/scrape.py

from django.core.management.base import BaseCommand
from proje.partymartyurunler import scrape_products
from proje.kbkmarketurunler import scrape_and_save_products  # utils.py içindeki fonksiyonu buradan çağırıyoruz


class Command(BaseCommand):
    help = 'Scrape products from the website'

    def handle(self, *args, **options):
        scrape_and_save_products()
        #scrape_products()
        
     
        self.stdout.write(self.style.SUCCESS('Successfully scraped products'))
