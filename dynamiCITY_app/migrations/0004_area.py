# Generated by Django 4.1.9 on 2023-05-12 16:48

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('dynamiCITY_app', '0003_alter_county_options_alter_district_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('status', models.IntegerField(choices=[(0, 'Inactive'), (1, 'Active')], default=1, verbose_name='status')),
                ('activate_date', models.DateTimeField(blank=True, help_text='keep empty for an immediate activation', null=True)),
                ('deactivate_date', models.DateTimeField(blank=True, help_text='keep empty for indefinite activation', null=True)),
                ('area_name', models.CharField(max_length=100)),
                ('pop', models.IntegerField(default=0)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('multipolygon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dynamiCITY_app.multipolygon')),
                ('polygon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dynamiCITY_app.polygon')),
            ],
            options={
                'verbose_name_plural': 'Areas',
            },
        ),
    ]
