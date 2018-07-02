# Generated by Django 2.0.6 on 2018-07-02 02:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0009_auto_20180702_0235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='parent_comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comments', to='posts.Comment'),
        ),
        migrations.AlterField(
            model_name='commentlike',
            name='comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='in_comment', to='posts.Comment'),
        ),
    ]
