from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('common', '0007_auto_20170118_1758')
    ]

    operations = [
        migrations.CreateModel(
            name='ErrorLogEntry',
            fields=[
                (
                    'id', models.AutoField(
                        auto_created=True, primary_key=True, serialize=False,
                        verbose_name='ID'
                    )
                ),
                (
                    'namespace', models.CharField(
                        max_length=128, verbose_name='Namespace'
                    )
                ),
                (
                    'object_id', models.PositiveIntegerField(
                        blank=True, null=True
                    )
                ),
                (
                    'datetime', models.DateTimeField(
                        auto_now_add=True, db_index=True,
                        verbose_name='Date time'
                    )
                ),
                (
                    'result', models.TextField(
                        blank=True, null=True, verbose_name='Result'
                    )
                ),
                (
                    'content_type', models.ForeignKey(
                        blank=True, null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='error_log_content_type',
                        to='contenttypes.ContentType'
                    )
                )
            ],
            options={
                'ordering': ('datetime',),
                'verbose_name': 'Error log entry',
                'verbose_name_plural': 'Error log entries'
            }
        )
    ]
