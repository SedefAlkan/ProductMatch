from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Urunler, UrunIliskisi
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def home(request):
    return render(request, 'home.html')

# KBK Market ürünleri sayfası (default veritabanından veri çekiyor)
def kbkmarket_products(request):
    products = Urunler.objects.using('default').all()  # 'default' veritabanından ürünleri alır
    paginator = Paginator(products, 10)  # Her sayfada 10 ürün göster
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'kbkmarket.html', {'page_obj': page_obj})

# Party Marty ürünleri sayfası (secondary veritabanından veri çekiyor)
def partymarty_products(request):
    products = Urunler.objects.using('secondary').all()  # 'secondary' veritabanından ürünleri alır
    paginator = Paginator(products, 10)  # Her sayfada 10 ürün göster
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'partymarty.html', {'page_obj': page_obj})

def find_similar_products(request):
    # Her iki veritabanından ürünleri al
    products_db1 = Urunler.objects.using('default').all()
    products_db2 = Urunler.objects.using('secondary').all()

    # Ürün isimlerini birleştirme
    product_names_db1 = [product.name for product in products_db1]
    product_names_db2 = [product.name for product in products_db2]

    # TF-IDF vektörleştirici oluşturma
    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    tfidf_matrix_db1 = vectorizer.fit_transform(product_names_db1)
    tfidf_matrix_db2 = vectorizer.transform(product_names_db2)

    # Cosine benzerliğini hesaplama
    similarity_matrix = cosine_similarity(tfidf_matrix_db1, tfidf_matrix_db2)

    similar_products = []
    for i, product_db1 in enumerate(products_db1):
        for j in range(len(products_db2)):
            if similarity_matrix[i][j] >= 0.5:  # %50 veya daha fazla benzerlik
                # UrunIliskisi tablosuna ekleme
                UrunIliskisi.objects.using('third').create(  # 'third' veritabanına kaydediyoruz
                    kbk_urun_id=product_db1.id,
                    partymarty_urun_id=products_db2[j].id,
                    benzerlik_orani=similarity_matrix[i][j]
                )
                similar_products.append((product_db1, products_db2[j]))

    paginator = Paginator(similar_products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'similar_products.html', {'page_obj': page_obj})
