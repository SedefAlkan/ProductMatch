
# ProductMatch

ProductMatch, farklı e-ticaret platformlarından (KBK Market ve Party Marty) alınan ürün verilerini akıllı metin benzerliği algoritmaları kullanarak eşleştiren Django tabanlı bir web uygulamasıdır. Bu proje, aynı ürünün farklı platformlardaki varyasyonlarını otomatik olarak tespit ederek ürün karşılaştırması yapmayı sağlar.

## Özellikler

- **Çoklu Veritabanı Desteği**: Farklı kaynaklardan (KBK Market ve Party Marty) ürün verilerini ayrı veritabanlarında yönetme
- **Metin Benzerliği Analizi**: TF-IDF ve Cosine Similarity algoritmaları kullanarak ürün isimlerinde benzerlik tespiti
- **Otomatik Eşleştirme**: %50 ve üzeri benzerlik oranına sahip ürünleri otomatik eşleştirme
- **İlişki Kaydı**: Eşleşen ürünleri ve benzerlik oranlarını üçüncü bir veritabanında saklama
- **Sayfalandırma**: Büyük veri setlerini kolayca gezinmek için sayfalandırma özelliği
- **Kullanıcı Arayüzü**: Ürünleri ve eşleşmeleri görüntülemek için basit ve kullanışlı web arayüzü

## Teknik Detaylar

- **Framework**: Django web çerçevesi
- **Programlama Dili**: Python
- **Makine Öğrenimi**: scikit-learn kütüphanesi ile TF-IDF vektörleştirme ve Cosine Similarity hesaplama
- **Veritabanı Yapılandırması**: Üç farklı veritabanı bağlantısı (default, secondary, third)
- **Frontend**: Django şablonları ile HTML/CSS arayüzü

### Gereksinimler
- Python 3.8+
- Django 3.0+
- scikit-learn
- Veritabanı (PostgreSQL, MySQL, SQLite vb.)
- 
## Benzerlik Algoritması

Proje, ürün isimlerini karşılaştırmak için aşağıdaki adımları kullanır:

1. Ürün isimleri TF-IDF (Term Frequency-Inverse Document Frequency) kullanılarak vektörleştirilir
2. N-gram (1,2) kullanılarak kelime çiftleri de analize dahil edilir
3. Cosine Similarity ile ürün isimlerinin benzerlik değerleri hesaplanır
4. %50 veya daha yüksek benzerlik oranına sahip ürünler eşleştirilir
5. Eşleşen ürün çiftleri ve benzerlik oranları veritabanına kaydedilir

