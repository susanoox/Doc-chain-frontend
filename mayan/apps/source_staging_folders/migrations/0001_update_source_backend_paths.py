from django.db import migrations

SOURCE_BACKEND_MAPPING = {
    'mayan.apps.sources.source_backends.staging_folder_backends.SourceBackendStagingFolder': 'mayan.apps.source_staging_folders.source_backends.staging_folder_backends.SourceBackendStagingFolder',
}


def code_source_backend_path_update(apps, schema_editor):
    Source = apps.get_model(app_label='sources', model_name='Source')

    for key, value in SOURCE_BACKEND_MAPPING.items():
        queryset = Source.objects.using(alias=schema_editor.connection.alias).filter(backend_path=key)
        queryset.update(backend_path=value)


def reverse_code_source_backend_path_update(apps, schema_editor):
    Source = apps.get_model(app_label='sources', model_name='Source')

    for key, value in SOURCE_BACKEND_MAPPING.items():
        queryset = Source.objects.using(alias=schema_editor.connection.alias).filter(backend_path=value)
        queryset.update(backend_path=key)


class Migration(migrations.Migration):
    dependencies = [
        ('sources', '0029_update_source_backend_paths')
    ]

    operations = [
        migrations.RunPython(
            code=code_source_backend_path_update,
            reverse_code=reverse_code_source_backend_path_update
        )
    ]
