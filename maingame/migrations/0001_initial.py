# Generated by Django 2.1.3 on 2018-12-21 16:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=64)),
                ('is_valid', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.IntegerField(default=2)),
                ('name', models.CharField(default='A', max_length=64)),
                ('flag', models.CharField(default='Iran', max_length=16)),
                ('win_strike', models.IntegerField(default=0)),
                ('level', models.IntegerField(default=0)),
                ('experience', models.BigIntegerField(default=0)),
                ('average_score', models.FloatField(default=0)),
                ('game_number', models.IntegerField(default=0)),
                ('won_number', models.IntegerField(default=0)),
                ('gem', models.IntegerField(default=0)),
                ('coins', models.IntegerField(default=0)),
                ('friends', models.ManyToManyField(related_name='_profile_friends_+', to='maingame.Profile')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(default='', max_length=512)),
                ('question_animation', models.FileField(blank=True, default='', upload_to='')),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='maingame.Question'),
        ),
    ]
