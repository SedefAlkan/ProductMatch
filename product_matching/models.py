from django.db import models


class Urunler(models.Model):
    name = models.CharField(max_length=500)
    price = models.CharField(max_length=100)  # Eğer fiyat sayısal bir değer olacaksa, DecimalField kullanmanız daha iyi olabilir.
    description = models.TextField()

    def __str__(self):
        return self.name


class UrunIliskisi(models.Model):
    kbk_urun = models.ForeignKey(
        'Urunler',
        on_delete=models.CASCADE,
        related_name='kbk_urun_iliskisi',
        db_constraint=False
    )
    partymarty_urun = models.ForeignKey(
        'Urunler',
        on_delete=models.CASCADE,
        related_name='partymarty_urun_iliskisi',
        db_constraint=False
    )
    benzerlik_orani = models.FloatField()  # Benzerlik oranı (0.0 - 1.0 arasında)

    def __str__(self):
        return f"{self.kbk_urun.name} - {self.partymarty_urun.name} (%{self.benzerlik_orani*100:.2f})"



