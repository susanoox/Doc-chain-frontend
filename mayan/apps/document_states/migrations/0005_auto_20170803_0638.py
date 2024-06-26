from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('events', '0001_initial'),
        ('document_states', '0004_workflow_internal_name')
    ]

    operations = [
        migrations.CreateModel(
            name='WorkflowTransitionTriggerEvent',
            fields=[
                (
                    'id', models.AutoField(
                        auto_created=True, primary_key=True, serialize=False,
                        verbose_name='ID'
                    )
                ),
                (
                    'stored_event_type', models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='trigger_events', to='events.EventType',
                        verbose_name='Event type'
                    )
                )
            ],
            options={
                'verbose_name': 'Workflow transition trigger event',
                'verbose_name_plural': 'Workflow transitions trigger events'
            }
        ),
        migrations.AddField(
            model_name='workflowtransition',
            name='trigger_time_period',
            field=models.PositiveIntegerField(
                blank=True, help_text='Amount of time after which this '
                'transition will trigger on its own.', null=True,
                verbose_name='Trigger time period'
            )
        ),
        migrations.AddField(
            model_name='workflowtransition',
            name='trigger_time_unit',
            field=models.CharField(
                blank=True, choices=[
                    ('days', 'Days'), ('hours', 'Hours'),
                    ('minutes', 'Minutes')
                ], max_length=8, null=True, verbose_name='Trigger time unit'
            )
        ),
        migrations.AddField(
            model_name='workflowtransitiontriggerevent',
            name='transition',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to='document_states.WorkflowTransition',
                verbose_name='Transition'
            )
        )
    ]
