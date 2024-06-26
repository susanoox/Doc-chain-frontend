from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('converter', '0009_auto_20150714_2228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transformation',
            name='name',
            field=models.CharField(
                max_length=128, verbose_name='Name',
                choices=[
                    ('rotate', 'Rotate: degrees'), ('zoom', 'Zoom: percent'),
                    ('resize', 'Resize: width, height'),
                    ('crop', 'Crop: left, top, right, bottom')
                ]
            ),
            preserve_default=True,
        ),
    ]
