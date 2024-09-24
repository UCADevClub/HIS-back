from django.db import models
from django.core.files.storage import FileSystemStorage
from appointment.models import Appointment,ReferralAppointment
from staff.models import Doctor

fs = FileSystemStorage(location='/media/labs')


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

    general_condition = models.CharField(max_length=50, choices=GENERAL_CONDITION_CHOICES, blank=True, null=True)
    consciousness = models.CharField(max_length=50, choices=CONSCIOUSNESS_CHOICES, blank=True, null=True)
    position = models.CharField(max_length=50, choices=POSITION_CHOICES, blank=True, null=True)
    skin_condition = models.CharField(max_length=50, choices=SKIN_CONDITION_CHOICES, blank=True, null=True)
    edema = models.CharField(max_length=50, choices=EDEMA_CHOICES, blank=True, null=True)
    edema_comments = models.TextField(blank=True, null=True)
    nail_condition = models.CharField(max_length=50, choices=NAIL_CONDITION_CHOICES, blank=True, null=True)
    joint_condition = models.CharField(max_length=50, choices=JOINT_CONDITION_CHOICES, blank=True, null=True)
    joint_comments = models.TextField(blank=True, null=True)
    lymph_nodes = models.CharField(max_length=100, choices=LYMPH_NODES_CHOICES, blank=True, null=True)
    nasal_breathing = models.CharField(max_length=50, choices=NASAL_BREATHING_CHOICES, blank=True, null=True)
    chest_participation = models.CharField(max_length=50, choices=CHEST_PARTICIPATION_CHOICES, blank=True, null=True)
    muscle_participation = models.CharField(max_length=100, choices=MUSCLE_PARTICIPATION_CHOICES, blank=True, null=True)
    lung_auscultation = models.CharField(max_length=50, choices=LUNG_AUSCULTATION_CHOICES, blank=True, null=True)
    heart_area = models.CharField(max_length=50, choices=HEART_AREA_CHOICES, blank=True, null=True)
    pericardial_pulsation = models.CharField(max_length=50, choices=PERICARDIAL_PULSATION_CHOICES, blank=True, null=True)
    epigastric_pulsation = models.CharField(max_length=50, choices=EPIGASTRIC_PULSATION_CHOICES, blank=True, null=True)
    cyanosis = models.CharField(max_length=50, choices=CYANOSIS_CHOICES, blank=True, null=True)
    neck_veins = models.CharField(max_length=50, choices=NECK_VEINS_CHOICES, blank=True, null=True)
    heart_tones = models.CharField(max_length=50, choices=HEART_TONES_CHOICES, blank=True, null=True)
    systolic_murmur = models.CharField(max_length=50, choices=SYSTOLIC_MURMUR_CHOICES, blank=True, null=True)
    diastolic_murmur = models.CharField(max_length=50, choices=DIASTOLIC_MURMUR_CHOICES, blank=True, null=True)
    oral_mucosa = models.CharField(max_length=50, choices=ORAL_MUCOSA_CHOICES, blank=True, null=True)
    tongue = models.CharField(max_length=50, choices=TONGUE_CHOICES, blank=True, null=True)
    pharynx = models.CharField(max_length=50, choices=PHARYNX_CHOICES, blank=True, null=True)
    tonsils = models.CharField(max_length=50, choices=TONSILS_CHOICES, blank=True, null=True)
    abdomen = models.CharField(max_length=100, choices=ABDOMEN_CHOICES, blank=True, null=True)
    abdomen_comments = models.TextField(blank=True, null=True)
    liver = models.CharField(max_length=50, choices=LIVER_CHOICES, blank=True, null=True)
    gallbladder = models.CharField(max_length=50, choices=GALLBLADDER_CHOICES, blank=True, null=True)
    stool = models.CharField(max_length=50, choices=STOOL_CHOICES, blank=True, null=True)
    stool_comments = models.TextField(blank=True, null=True)
    urination = models.CharField(max_length=100, choices=URINATION_CHOICES, blank=True, null=True)
    urination_comments = models.TextField(blank=True, null=True)
    tapping_symptom = models.CharField(max_length=50, choices=TAPPING_SYMPTOM_CHOICES, blank=True, null=True)
    neurological_status = models.CharField(max_length=50, choices=NEUROLOGICAL_STATUS_CHOICES, blank=True, null=True)
    eye_slits = models.CharField(max_length=50, choices=EYE_SLITS_CHOICES, blank=True, null=True)
    face = models.CharField(max_length=50, choices=FACE_CHOICES, blank=True, null=True)
    dizziness = models.CharField(max_length=50, choices=DIZZINESS_CHOICES, blank=True, null=True)
    meningeal_symptoms = models.CharField(max_length=50, choices=MENINGEAL_SYMPTOMS_CHOICES, blank=True, null=True)


class Referral(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, blank=True, null=True)
    referral_conclusion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Referral for {self.appointment.patient} on {self.appointment.created_at}"
    

class Medications(models.Model):
    medication_name = models.CharField(max_length=255)
    dosage = models.TextField()
    frequency = models.TextField()

    def __str__(self):
        return f"{self.medication_name} - {self.dosage} ({self.frequency})"


class Treatment(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    objective_examination = models.OneToOneField(ObjectiveExamination, on_delete=models.SET_NULL, null=True, blank=True)
    examination_plan = models.TextField(blank=True, null=True)

    # Laboratory and Instrumental Study Results
    lab_tests = models.FileField(upload_to='labs/', blank=True, null=True)
    
    # Referral replaced with new model
    is_referral = models.BooleanField(default=False)
    referral_appointment = models.OneToOneField(ReferralAppointment, on_delete=models.SET_NULL,
                                                related_name='treatment_ref_appointment',null=True, blank=True)
    referral = models.OneToOneField(Referral, on_delete=models.SET_NULL, null=True, blank=True)

    justification_and_formulation = models.TextField(blank=True, null=True)
    recommendations = models.TextField(blank=True, null=True)

    # Medications
    medications = models.ManyToManyField(Medications, related_name='treatments', blank=True)
    category = models.CharField(blank=True, null=True, max_length=50)

    def __str__(self):
        return f"Treatment for {self.appointment.patient} on {self.appointment.created_at}"