from django.core.files.storage import FileSystemStorage
from django.db import migrations, models

import mayan.apps.document_signatures.models


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0033_auto_20160325_0052'),
        ('document_signatures', '0002_auto_20150608_1902')
    ]

    operations = [
        migrations.CreateModel(
            name='SignatureBaseModel',
            fields=[
                (
                    'id', models.AutoField(
                        verbose_name='ID', serialize=False, auto_created=True,
                        primary_key=True
                    )
                ),
                (
                    'date', models.DateField(
                        null=True, verbose_name='Date signed', blank=True
                    )
                ),
                (
                    'key_id', models.CharField(
                        max_length=40, verbose_name='Key ID'
                    )
                ),
                (
                    'signature_id', models.CharField(
                        max_length=64, null=True, verbose_name='Signature ID',
                        blank=True
                    )
                ),
                (
                    'public_key_fingerprint', models.CharField(
                        verbose_name='Public key fingerprint', unique=True,
                        max_length=40, editable=False
                    )
                )
            ],
            options={
                'verbose_name': 'Document version signature',
                'verbose_name_plural': 'Document version signatures'
            }
        ),
        migrations.RemoveField(
            model_name='documentversionsignature',
            name='has_embedded_signature'
        ),
        migrations.AddField(
            model_name='documentversionsignature',
            name='date',
            field=models.DateField(
                null=True, verbose_name='Date signed', blank=True
            )
        ),
        migrations.AddField(
            model_name='documentversionsignature',
            name='signature_id',
            field=models.CharField(
                max_length=64, null=True, verbose_name='Signature ID',
                blank=True
            )
        ),
        migrations.AlterField(
            model_name='documentversionsignature',
            name='document_version',
            field=models.ForeignKey(
                editable=False, on_delete=models.CASCADE,
                related_name='signature', to='documents.DocumentVersion',
                verbose_name='Document version'
            )
        ),
        migrations.CreateModel(
            name='DetachedSignature',
            fields=[
                (
                    'signaturebasemodel_ptr', models.OneToOneField(
                        auto_created=True, on_delete=models.CASCADE,
                        parent_link=True, primary_key=True, serialize=False,
                        to='document_signatures.SignatureBaseModel'
                    )
                ),
                (
                    'signature_file', models.FileField(
                        storage=FileSystemStorage(),
                        upload_to=mayan.apps.document_signatures.models.upload_to,
                        null=True, verbose_name='Signature file', blank=True
                    )
                )
            ],
            options={
                'verbose_name': 'Document version detached signature',
                'verbose_name_plural': 'Document version detached signatures'
            },
            bases=('document_signatures.signaturebasemodel',)
        ),
        migrations.CreateModel(
            name='EmbeddedSignature',
            fields=[
                (
                    'signaturebasemodel_ptr', models.OneToOneField(
                        auto_created=True, on_delete=models.CASCADE,
                        parent_link=True, primary_key=True, serialize=False,
                        to='document_signatures.SignatureBaseModel'
                    )
                )
            ],
            options={
                'verbose_name': 'Document version embedded signature',
                'verbose_name_plural': 'Document version embedded signatures'
            },
            bases=('document_signatures.signaturebasemodel',)
        ),
        migrations.AddField(
            model_name='signaturebasemodel',
            name='document_version',
            field=models.ForeignKey(
                editable=False, on_delete=models.CASCADE,
                related_name='signaturebasemodel',
                to='documents.DocumentVersion',
                verbose_name='Document version'
            )
        )
    ]
