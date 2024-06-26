from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('sources', '0012_auto_20170205_0743')
    ]

    operations = [
        migrations.AddField(
            model_name='sanescanner',
            name='adf_mode',
            field=models.CharField(
                blank=True, choices=[
                    ('simplex', 'Simples'), ('duplex', 'Duplex')
                ], default='simplex',
                help_text='Selects the document feeder mode '
                '(simplex/duplex). If this option is not supported by '
                'your scanner, leave it blank.', max_length=16,
                verbose_name='ADF mode'
            )
        ),
        migrations.AddField(
            model_name='sanescanner',
            name='source',
            field=models.CharField(
                blank=True, choices=[
                    ('flatbed', 'Flatbed'),
                    ('document-feeder', 'Document feeder')
                ], default='flatbed', help_text='Selects the scan source '
                '(such as a document-feeder). If this option is not '
                'supported by your scanner, leave it blank.', max_length=16,
                verbose_name='Paper source'
            )
        ),
        migrations.AlterField(
            model_name='sanescanner',
            name='mode',
            field=models.CharField(
                blank=True, choices=[
                    ('lineart', 'Lineart'), ('monochrome', 'Monochrome'),
                    ('color', 'Color')
                ], default='color', help_text='Selects the scan mode '
                '(e.g., lineart, monochrome, or color). If this option is '
                'not supported by your scanner, leave it blank.',
                max_length=16, verbose_name='Mode'
            )
        ),
        migrations.AlterField(
            model_name='sanescanner',
            name='resolution',
            field=models.PositiveIntegerField(
                blank=True, help_text='Sets the resolution of the scanned '
                'image in DPI (dots per inch). Typical value is 200. If '
                'this option is not supported by your scanner, leave it '
                'blank.', verbose_name='Resolution'
            )
        )
    ]
