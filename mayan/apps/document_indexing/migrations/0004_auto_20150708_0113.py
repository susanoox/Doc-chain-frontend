from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('document_indexing', '0003_auto_20150708_0101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='index',
            name='label',
            field=models.CharField(
                unique=True, max_length=128, verbose_name='Label'
            ),
            preserve_default=True,
        ),
    ]
