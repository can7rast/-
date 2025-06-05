from django.db import migrations

def add_default_workout_types(apps, schema_editor):
    WorkoutType = apps.get_model('workouts', 'WorkoutType')
    
    default_types = [
        {
            'name': 'Силовая тренировка',
            'description': 'Тренировка, направленная на развитие силы и мышечной массы',
            'calories_per_hour': 400
        },
        {
            'name': 'Растяжка',
            'description': 'Упражнения для улучшения гибкости и подвижности суставов',
            'calories_per_hour': 150
        },
        {
            'name': 'Кардио тренировка',
            'description': 'Тренировка для улучшения сердечно-сосудистой системы и выносливости',
            'calories_per_hour': 500
        }
    ]
    
    for type_data in default_types:
        WorkoutType.objects.get_or_create(
            name=type_data['name'],
            defaults={
                'description': type_data['description'],
                'calories_per_hour': type_data['calories_per_hour']
            }
        )

def remove_default_workout_types(apps, schema_editor):
    WorkoutType = apps.get_model('workouts', 'WorkoutType')
    WorkoutType.objects.filter(
        name__in=['Силовая тренировка', 'Растяжка', 'Кардио тренировка']
    ).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('workouts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_default_workout_types, remove_default_workout_types),
    ] 