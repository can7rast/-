from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('workouts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workout',
            name='workout_type',
            field=models.CharField(
                choices=[
                    ('cardio', 'Кардио'),
                    ('strength', 'Силовая'),
                    ('hiit', 'HIIT'),
                    ('yoga', 'Йога'),
                    ('stretching', 'Растяжка'),
                    ('other', 'Другое')
                ],
                max_length=20,
                verbose_name='Тип тренировки'
            ),
        ),
        migrations.DeleteModel(
            name='WorkoutType',
        ),
    ] 