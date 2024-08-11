from django.db import models

class ObjectiveExamination(models.Model):
    GENERAL_CONDITION_CHOICES = [
        ('satisfactory', 'Удовлетворительное'),
        ('relatively_satisfactory', 'Относительно удовлетворит'),
        ('moderate_severity', 'Средней тяжести'),
        ('severe', 'Тяжелое')
    ]

    CONSCIOUSNESS_CHOICES = [
        ('clear', 'Ясное'),
        ('slowed', 'Заторможенное'),
        ('absent', 'Отсутствует'),
        ('oriented', 'Ориентирован'),
        ('disoriented', 'Не ориентирован')
    ]

    POSITION_CHOICES = [
        ('active', 'Активное'),
        ('inactive', 'Неактивное')
    ]

    SKIN_CONDITION_CHOICES = [
        ('normal', 'Обычной окраски'),
        ('pale', 'Бледные')
    ]

    EDEMA_CHOICES = [
        ('yes', 'Есть'),
        ('no', 'Нет')
    ]

    NAIL_CONDITION_CHOICES = [
        ('dry', 'Сухие'),
        ('dull', 'Тусклые'),
        ('brittle', 'Ломкие'),
        ('healthy', 'Здоровые')
    ]

    JOINT_CONDITION_CHOICES = [
        ('unchanged', 'Внешне не изменены'),
        ('full_movement', 'Движение в полном объеме'),
        ('painful', 'Болезненны')
    ]

    LYMPH_NODES_CHOICES = [
        ('not_enlarged', 'Не увеличены'),
        ('enlarged', 'Увеличены'),
        ('fused', 'Спаяны с окружающей тканью'),
        ('not_fused', 'Не спаяны'),
        ('painful', 'Болезненны'),
        ('painless', 'Безболезненны')
    ]

    NASAL_BREATHING_CHOICES = [
        ('free', 'Свободное'),
        ('difficult', 'Затрудненное'),
        ('discharge', 'Выделения')
    ]

    CHEST_PARTICIPATION_CHOICES = [
        ('symmetrical', 'Симметрично'),
        ('lags_right', 'Отстает справа'),
        ('lags_left', 'Отстает слева')
    ]

    MUSCLE_PARTICIPATION_CHOICES = [
        ('neck', 'Шеи'),
        ('intercostal', 'Межреберий'),
        ('intercostal_retraction', 'Втяжение межреберий'),
        ('shoulder_girdle', 'Плечевого пояса')
    ]

    LUNG_AUSCULTATION_CHOICES = [
        ('vesicular', 'Везикулярное'),
        ('harsh', 'Жесткое'),
        ('weakened', 'Ослабленное')
    ]

    HEART_AREA_CHOICES = [
        ('unchanged', 'Не изменен'),
        ('cardiac_hump', 'Имеется сердечный горб')
    ]

    PERICARDIAL_PULSATION_CHOICES = [
        ('present', 'Есть'),
        ('absent', 'Нет'),
        ('pronounced', 'Выраженное')
    ]

    EPIGASTRIC_PULSATION_CHOICES = [
        ('present', 'Есть'),
        ('absent', 'Нет'),
        ('pronounced', 'Выраженное')
    ]

    CYANOSIS_CHOICES = [
        ('none', 'Нет'),
        ('acrocyanosis', 'Акроцианоз'),
        ('diffuse', 'Диффузный'),
        ('mild', 'Легкий'),
        ('moderate', 'Умеренный'),
        ('severe', 'Выраженный')
    ]

    NECK_VEINS_CHOICES = [
        ('present', 'Есть'),
        ('absent', 'Нет')
    ]

    HEART_TONES_CHOICES = [
        ('rhythmic', 'Ритмичные'),
        ('arrhythmia', 'Аритмия')
    ]

    SYSTOLIC_MURMUR_CHOICES = [
        ('present', 'Есть'),
        ('absent', 'Нет')
    ]

    DIASTOLIC_MURMUR_CHOICES = [
        ('present', 'Есть'),
        ('absent', 'Нет')
    ]

    ORAL_MUCOSA_CHOICES = [
        ('normal', 'Обычной окраски'),
        ('pale', 'Бледная')
    ]

    TONGUE_CHOICES = [
        ('dry', 'Сухой'),
        ('clean', 'Чистый'),
        ('coated', 'Обложен')
    ]

    PHARYNX_CHOICES = [
        ('hyperemic', 'Гиперемирован'),
        ('normal', 'Обычной окраски')
    ]

    TONSILS_CHOICES = [
        ('enlarged', 'Увеличены'),
        ('not_enlarged', 'Не увеличены')
    ]

    ABDOMEN_CHOICES = [
        ('normal_size', 'Обычных размеров'),
        ('soft', 'Мягкий'),
        ('painful', 'Болезненный'),
        ('painless', 'Безболезненный')
    ]

    LIVER_CHOICES = [
        ('enlarged', 'Увеличен'),
        ('not_enlarged', 'Не увеличен')
    ]

    GALLBLADDER_CHOICES = [
        ('palpable', 'Пальпируется'),
        ('not_palpable', 'Не пальпируется')
    ]

    STOOL_CHOICES = [
        ('regular', 'Регулярный'),
        ('constipation', 'Запоры'),
        ('loose', 'Жидкий')
    ]

    URINATION_CHOICES = [
        ('free', 'Свободное'),
        ('difficult', 'Затрудненное'),
        ('painful', 'Болезненное'),
        ('clear', 'Прозрачное'),
        ('cloudy', 'Мутное'),
        ('small_amount', 'Мало'),
        ('large_amount', 'Много')
    ]

    TAPPING_SYMPTOM_CHOICES = [
        ('negative', 'Отрицательный'),
        ('positive_right', 'Положительный справа'),
        ('positive_left', 'Положительный слева')
    ]

    NEUROLOGICAL_STATUS_CHOICES = [
        ('good', 'Воспринимает хорошо'),
        ('reduced', 'Снижено'),
        ('lost', 'Утрачено')
    ]

    EYE_SLITS_CHOICES = [
        ('equal', 'Одинаковые'),
        ('ptosis_right', 'Птоз справа'),
        ('ptosis_left', 'Птоз слева'),
        ('half_ptosis', 'Полуптоз')
    ]

    FACE_CHOICES = [
        ('symmetrical', 'Симметричное'),
        ('flattened', 'Сглаженность')
    ]

    DIZZINESS_CHOICES = [
        ('none', 'Нет'),
        ('present', 'Есть'),
        ('systemic', 'Системное')
    ]

    MENINGEAL_SYMPTOMS_CHOICES = [
        ('negative', 'Отрицательные'),
        ('positive', 'Положительные')
    ]

    general_condition = models.CharField(max_length=50, choices=GENERAL_CONDITION_CHOICES)
    consciousness = models.CharField(max_length=50, choices=CONSCIOUSNESS_CHOICES)
    position = models.CharField(max_length=50, choices=POSITION_CHOICES)
    skin_condition = models.CharField(max_length=50, choices=SKIN_CONDITION_CHOICES)
    edema = models.CharField(max_length=50, choices=EDEMA_CHOICES)
    edema_comments = models.TextField(blank=True, null=True)

    nail_condition = models.CharField(max_length=50, choices=NAIL_CONDITION_CHOICES)
    joint_condition = models.CharField(max_length=50, choices=JOINT_CONDITION_CHOICES)
    joint_comments = models.TextField(blank=True, null=True)

    lymph_nodes = models.CharField(max_length=100, choices=LYMPH_NODES_CHOICES)
    nasal_breathing = models.CharField(max_length=50, choices=NASAL_BREATHING_CHOICES)
    chest_participation = models.CharField(max_length=50, choices=CHEST_PARTICIPATION_CHOICES)
    muscle_participation = models.CharField(max_length=100, choices=MUSCLE_PARTICIPATION_CHOICES)
    lung_auscultation = models.CharField(max_length=50, choices=LUNG_AUSCULTATION_CHOICES)
    heart_area = models.CharField(max_length=50, choices=HEART_AREA_CHOICES)
    pericardial_pulsation = models.CharField(max_length=50, choices=PERICARDIAL_PULSATION_CHOICES)
    epigastric_pulsation = models.CharField(max_length=50, choices=EPIGASTRIC_PULSATION_CHOICES)
    cyanosis = models.CharField(max_length=50, choices=CYANOSIS_CHOICES)
    neck_veins = models.CharField(max_length=50, choices=NECK_VEINS_CHOICES)
    heart_tones = models.CharField(max_length=50, choices=HEART_TONES_CHOICES)
    systolic_murmur = models.CharField(max_length=50, choices=SYSTOLIC_MURMUR_CHOICES)
    diastolic_murmur = models.CharField(max_length=50, choices=DIASTOLIC_MURMUR_CHOICES)
    oral_mucosa = models.CharField(max_length=50, choices=ORAL_MUCOSA_CHOICES)
    tongue = models.CharField(max_length=50, choices=TONGUE_CHOICES)
    pharynx = models.CharField(max_length=50, choices=PHARYNX_CHOICES)
    tonsils = models.CharField(max_length=50, choices=TONSILS_CHOICES)
    abdomen = models.CharField(max_length=100, choices=ABDOMEN_CHOICES)
    abdomen_comments = models.TextField(blank=True, null=True)
    liver = models.CharField(max_length=50, choices=LIVER_CHOICES)
    gallbladder = models.CharField(max_length=50, choices=GALLBLADDER_CHOICES)
    stool = models.CharField(max_length=50, choices=STOOL_CHOICES)
    stool_comments = models.TextField(blank=True, null=True)

    urination = models.CharField(max_length=100, choices=URINATION_CHOICES)
    urination_comments = models.TextField(blank=True, null=True)

    tapping_symptom = models.CharField(max_length=50, choices=TAPPING_SYMPTOM_CHOICES)
    neurological_status = models.CharField(max_length=50, choices=NEUROLOGICAL_STATUS_CHOICES)
    eye_slits = models.CharField(max_length=50, choices=EYE_SLITS_CHOICES)
    face = models.CharField(max_length=50, choices=FACE_CHOICES)
    dizziness = models.CharField(max_length=50, choices=DIZZINESS_CHOICES)
    meningeal_symptoms = models.CharField(max_length=50, choices=MENINGEAL_SYMPTOMS_CHOICES)


