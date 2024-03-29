from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0020_auto_20150714_2233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentversion',
            name='comment',
            field=models.TextField(
                default='', null=True, verbose_name='Comment', blank=True
            ),
            preserve_default=True,
        ),
    ]
