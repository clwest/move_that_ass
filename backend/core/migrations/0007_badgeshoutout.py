from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_badge_profile_badges'),
    ]

    operations = [
        migrations.CreateModel(
            name='BadgeShoutout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('badge', models.ForeignKey(on_delete=models.deletion.CASCADE, to='core.badge')),
                ('herd', models.ForeignKey(blank=True, null=True, on_delete=models.deletion.CASCADE, to='core.herd')),
                ('user', models.ForeignKey(on_delete=models.deletion.CASCADE, to='auth.user')),
            ],
            options={'ordering': ['-created_at']},
        ),
    ]
