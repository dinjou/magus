from django.db import migrations, models

def create_profiles(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Profile = apps.get_model('magus', 'Profile')
    for user in User.objects.all():
        Profile.objects.get_or_create(user=user)

class Migration(migrations.Migration):

    dependencies = [
        ('magus', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clock_in_time', models.DateTimeField(blank=True, null=True)),
                ('clock_out_time', models.DateTimeField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=models.CASCADE, to='auth.User')),
            ],
        ),
        migrations.RunPython(create_profiles),
    ]
