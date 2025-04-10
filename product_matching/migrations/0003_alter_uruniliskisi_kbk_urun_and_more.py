# Generated by Django 4.2.14 on 2024-11-01 18:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proje', '0002_uruniliskisi'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uruniliskisi',
            name='kbk_urun',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='kbk_urun_iliskisi', to='proje.urunler'),
        ),
        migrations.AlterField(
            model_name='uruniliskisi',
            name='partymarty_urun',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='partymarty_urun_iliskisi', to='proje.urunler'),
        ),
    ]
