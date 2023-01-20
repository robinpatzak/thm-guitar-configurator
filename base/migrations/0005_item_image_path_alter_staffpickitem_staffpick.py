# Generated by Django 4.1.4 on 2023-01-20 09:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_rename_staffpickitems_staffpickitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='image_path',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='staffpickitem',
            name='staffPick',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.staffpick', verbose_name='fk_StaffPick'),
        ),
    ]
