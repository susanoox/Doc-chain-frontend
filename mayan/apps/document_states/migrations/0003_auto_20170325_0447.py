from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('document_states', '0002_workflowstate_completion')
    ]

    operations = [
        migrations.CreateModel(
            name='WorkflowRuntimeProxy',
            fields=[],
            options={
                'verbose_name': 'Workflow runtime proxy',
                'proxy': True,
                'verbose_name_plural': 'Workflow runtime proxies'
            },
            bases=('document_states.workflow',)
        ),
        migrations.CreateModel(
            name='WorkflowStateRuntimeProxy',
            fields=[],
            options={
                'verbose_name': 'Workflow state runtime proxy',
                'proxy': True,
                'verbose_name_plural': 'Workflow state runtime proxies'
            },
            bases=('document_states.workflowstate',)
        ),
        migrations.AlterModelOptions(
            name='workflow',
            options={
                'ordering': ('label',),
                'verbose_name': 'Workflow',
                'verbose_name_plural': 'Workflows'
            }
        ),
        migrations.AlterModelOptions(
            name='workflowstate',
            options={
                'ordering': ('label',),
                'verbose_name': 'Workflow state',
                'verbose_name_plural': 'Workflow states'
            }
        ),
        migrations.AlterModelOptions(
            name='workflowtransition',
            options={
                'ordering': ('label',),
                'verbose_name': 'Workflow transition',
                'verbose_name_plural': 'Workflow transitions'
            }
        )
    ]
