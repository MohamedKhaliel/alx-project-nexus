from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expires_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255)),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='polls.poll')),
            ],
        ),
        migrations.AddIndex(model_name='option', index=models.Index(fields=['poll'], name='poll_idx'),),
        migrations.AlterUniqueTogether(name='option', unique_together={('poll', 'text')}),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voter_id', models.CharField(max_length=255)),
                ('cast_at', models.DateTimeField(auto_now_add=True)),
                ('option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='polls.option')),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='polls.poll')),
            ],
        ),
        migrations.AddIndex(model_name='vote', index=models.Index(fields=['poll'], name='vote_poll_idx'),),
        migrations.AddIndex(model_name='vote', index=models.Index(fields=['option'], name='vote_option_idx'),),
        migrations.AlterUniqueTogether(name='vote', unique_together={('poll', 'voter_id')}),
    ]


