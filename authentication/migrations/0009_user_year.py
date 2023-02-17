# Generated by Django 4.1.1 on 2022-12-03 00:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_cart_catcourses_users_alter_catcourses_year_cartitem'),
        ('authentication', '0008_user_device_alter_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='year',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='course.year'),
        ),
    ]
