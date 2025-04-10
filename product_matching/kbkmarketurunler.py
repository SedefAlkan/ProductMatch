import requests
from bs4 import BeautifulSoup
from .models import Urunler  

def scrape_and_save_products():
    base_url = "https://www.kbkmarket.com"
    
    
    response = requests.get(base_url)
    if response.status_code != 200:
        print("Ana sayfa yüklenemedi.")
        return
    
    soup = BeautifulSoup(response.content, "html.parser")
    
    category_links = soup.select("ul#HeaderMenu2 a")

    for link in category_links:
        category_name = link.text.strip()
        category_url = base_url + link['href'] if link['href'].startswith('/') else link['href']
        
        
        category_response = requests.get(category_url)
        if category_response.status_code != 200:
            print(f"{category_name} kategorisi yüklenemedi.")
            continue
        
        category_soup = BeautifulSoup(category_response.content, "html.parser")
        
        sub_category_links = category_soup.select("section.landing-block a.blokResimLink")

        for sub_link in sub_category_links:
            sub_category_url = sub_link['href']
            
            
            if not sub_category_url.startswith('http://') and not sub_category_url.startswith('https://'):
                if sub_category_url.startswith('/'):
                    sub_category_url = base_url + sub_category_url
                else:
                    sub_category_url = base_url + '/' + sub_category_url
            
            sub_category_response = requests.get(sub_category_url)
            if sub_category_response.status_code != 200:
                print(f"{sub_link.text.strip()} alt kategorisi yüklenemedi.")
                continue
            
            sub_category_soup = BeautifulSoup(sub_category_response.content, "html.parser")
           
            product_containers = sub_category_soup.select("div.productItem")

            if not product_containers:
                print(f"{sub_link.text.strip()} alt kategorisinde ürün bulunamadı.")
                continue

            for container in product_containers:
               
                name = container.select_one("div.productName a").get_text(strip=True)
                price_element = container.select_one("span.discountPriceSpan")
                price = price_element.get_text(strip=True) if price_element else "Fiyat bilgisi yok"
                description = container.select_one("a.detailLink")['title']
                
               
                Urunler.objects.update_or_create(
                    name=name,
                    defaults={
                        'price': price,
                        'description': description,
                    }
                )
                print(f"Ürün kaydedildi: {name} - {price}")


scrape_and_save_products()
