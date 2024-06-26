from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('events', '0003_notification')
    ]

    operations = [
        migrations.RenameModel(
            old_name='EventType',
            new_name='StoredEventType'
        ),
        migrations.AlterModelOptions(
            name='storedeventtype',
            options={
                'verbose_name': 'Stored event type',
                'verbose_name_plural': 'Stored event types'
            }
        ),
        migrations.RemoveField(
            model_name='eventsubscription',
            name='event_type',
        ),
        migrations.AddField(
            model_name='eventsubscription',
            name='stored_event_type',
            field=models.ForeignKey(
                default=1, on_delete=django.db.models.deletion.CASCADE,
                related_name='event_subscriptions',
                to='events.StoredEventType', verbose_name='Event type'
            ),
            preserve_default=False
        ),
        migrations.AlterField(
            model_name='eventsubscription',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='event_subscriptions',
                to=settings.AUTH_USER_MODEL, verbose_name='User'
            )
        )
    ]
