import requests
from bs4 import BeautifulSoup
from .models import Urunler

def scrape_products():
    base_url = 'https://www.partymarty.com.tr/'  # Ana URL
    response = requests.get(base_url)

    if response.status_code == 200:  # İstek başarılıysa
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Kategorileri bulmak için <li> etiketlerini arıyoruz
        category_links = []
        for item in soup.find_all('li', attrs={'data-selector': 'first-level-navigation'}):
            category_link = item.find('a')['href']
            category_links.append(base_url + category_link.lstrip('/'))
        
        # Her kategori için ürünleri çekiyoruz
        for category_url in category_links:
            page_number = 1
            while True:
                page_url = f"{category_url}?tp={page_number}"  # Sayfa numarasını ekliyoruz
                category_response = requests.get(page_url)

                if category_response.status_code == 200:  # Sayfa var
                    category_soup = BeautifulSoup(category_response.text, 'html.parser')

                    # Ürünleri içeren showcase sınıfını buluyoruz
                    showcases = category_soup.find_all('div', class_='showcase')
                    
                    # Eğer mevcut sayfada ürün yoksa, diğer sayfaya geçiyoruz
                    if not showcases:
                        print(f"{category_url} için sayfa {page_number} 'da ürün bulunamadı, diğer kategoriye geçiliyor.")
                        break  # Sayfa bitti, bir sonraki kategoriye geç
                    
                    tukenmis = False  # Tükendi durumu kontrolü

                    for showcase in showcases:
                        # "Tükendi" yazısını kontrol ediyoruz
                        sold_out_label = showcase.find('div', class_='sold-out-label')
                        if sold_out_label and sold_out_label.text.strip() == "Tükendi":
                            print(f"{category_url} için sayfa {page_number} 'da 'Tükendi' durumu tespit edildi, diğer kategoriye geçiliyor.")
                            tukenmis = True
                            break  # "Tükendi" varsa, döngüyü kır ve diğer kategoriye geç
                        
                        # Ürün adı (title) için <a> etiketindeki title özelliğini alıyoruz
                        name = showcase.find('a', title=True)['title']
                        
                        # Fiyatı bulmak için showcase-price-new sınıfındaki span içeriğini çekiyoruz
                        price_tag = showcase.find('div', class_='showcase-price-new')
                        price = price_tag.find('span').text.strip() if price_tag else 'Fiyat bilgisi yok'
                        
                        # Ürün resmi için img etiketinin data-src özelliğini kullanıyoruz
                        image_tag = showcase.find('img', class_='lazyload')
                        image_url = image_tag['data-src'] if image_tag else 'Resim yok'
                        
                        # Ürünü veritabanına kaydediyoruz
                        Urunler.objects.create(name=name, price=price, description=image_url)

                    if tukenmis:
                        break  # "Tükendi" durumu varsa, diğer kategoriye geç

                    page_number += 1  # Sonraki sayfaya geç
                elif category_response.status_code == 404:
                    print(f"{page_url} bulunamadı, diğer kategoriye geçiliyor.")
                    break  # Sayfa yoksa, döngüyü kır ve diğer kategoriye geç
                else:
                    print("Kategori sayfasına erişim sağlanamadı:", page_url, category_response.status_code)
                    break  # Sayfaya erişim sağlanamazsa döngüyü kır
    else:
        print("Ana sayfaya erişim sağlanamadı:", response.status_code)
