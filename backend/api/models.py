import typing
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from ckeditor.fields import RichTextField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class ResultModel(models.Model):
    max_length = 255

    date = models.DateField(verbose_name='Время прохождения')
    frontend = models.CharField(max_length=max_length)
    backend = models.CharField(max_length=max_length)
    ux_ui = models.CharField(max_length=max_length)
    data_science = models.CharField(max_length=max_length)
    mobile_development = models.CharField(max_length=max_length)
    machine_learning = models.CharField(max_length=max_length) 

    class Meta:
        verbose_name_plural = "Результаты"


class UserModel(AbstractUser):
    max_length = 255

    STATUS_VARIANTS: typing.Final = (
        ("working", "работаю"),
        ("studying", "учусь"),
        ("looking_for_job", "в поиске работы"),
    )

    email = models.EmailField(verbose_name="Электронная почта", null=False, blank=False, unique=True)
    name =  models.CharField(max_length=max_length, verbose_name="Имя", null=True, blank=True)
    surname = models.CharField(max_length=max_length, verbose_name="Фамилия", null=True, blank=True)
    patronymic = models.CharField(max_length=max_length, verbose_name="Отчество", null=True, blank=True)

    photo = models.ImageField(upload_to='profile_photos/', verbose_name='Фотография', null=True, blank=True)
    telegram = models.CharField(max_length=max_length, verbose_name="Телеграм аккаунт", null=True, blank=True)
    status = models.CharField(max_length=max_length, verbose_name="Статус", choices=STATUS_VARIANTS, null=True, blank=True)
    about_me = models.TextField(verbose_name="Обо мне", null=True, blank=True)

    result = models.ForeignKey(ResultModel, verbose_name='Результаты', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.surname} {self.name} {self.patronymic} ({self.username})"
    
    def save(self, *args, **kwargs):
        if not self.patronymic:
            self.patronymic = ""
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["surname", "name", "patronymic"]
        verbose_name_plural = "Пользователи"


class MentorModel(AbstractUser):
    max_length = 255

    STATUS_VARIANTS: typing.Final = (
        ("career_start", "старт в карьере"),
        ("transition_to_another_area", "переход в другую сферу "),
        ("resume", "резюме"),
        ("motivation", "мотивация"),
        ("choosing_professional_path", "выбор профессионального пути"),
        ("interview", "собеседование")
    )

    email = models.EmailField(verbose_name="Электронная почта", null=False, blank=False)
    name =  models.CharField(max_length=max_length, verbose_name="Имя", null=True, blank=True)
    surname = models.CharField(max_length=max_length, verbose_name="Фамилия", null=True, blank=True)
    patronymic = models.CharField(max_length=max_length, verbose_name="Отчество", null=True, blank=True)

    photo = models.ImageField(upload_to='profile_photos/', verbose_name='Фотография', null=True, blank=True)
    telegram = models.CharField(max_length=max_length, verbose_name="Телеграм аккаунт", null=True, blank=True)
    status = models.CharField(max_length=max_length, verbose_name="Статус", choices=STATUS_VARIANTS, null=True, blank=True)
    about_me = models.TextField(verbose_name="Обо мне", null=True, blank=True)

    def __str__(self):
        return f"{self.surname} {self.name} {self.patronymic} ({self.username})"
    
    def save(self, *args, **kwargs):
        if not self.patronymic:
            self.patronymic = ""
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["surname", "name", "patronymic"]
        verbose_name_plural = "Менторы"

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_('The groups this user belongs to.'),
        related_name='mentors_groups'  # Пользовательское имя для обратной связи
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='mentors_permissions'  # Пользовательское имя для обратной связи
    )


class Meta(models.Model):
    key = models.TextField(unique=True, verbose_name="Ключ (ссылка)")
    title = models.TextField(verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")

    class Meta:
        verbose_name = "Мета"
        verbose_name_plural = "Мета"

    def __str__(self):
        return self.title


class EventModel(models.Model):
    max_length = 255

    date = models.DateField(verbose_name='Время мероприятия')
    title = models.CharField(verbose_name='Название', max_length=max_length)
    description = RichTextField(verbose_name='Описание')
    photo = models.ImageField(upload_to='profile_photos/', verbose_name='Фотография', null=True, blank=True)
    
    class Meta: 
        ordering = ["date"]
        verbose_name_plural = "Мероприятия"
        

class CategoryModel(models.Model):
    max_length = 255

    title = models.CharField(max_length=max_length, verbose_name="Название")

    def __str__(self):
        return self.title  
    
    class Meta:
        verbose_name_plural = "Категории"


class ArticleModel(models.Model):
    max_length = 255

    title = models.CharField(max_length=max_length, verbose_name="Название")
    title_en = models.CharField(max_length=max_length, verbose_name="Название (англ)")
    text = RichTextField(verbose_name="Текст", null=True, blank=True)
    author = models.CharField(max_length=max_length, verbose_name="Автор")
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Дата обновления", auto_now=True)
    categories = models.ManyToManyField(CategoryModel, verbose_name="Категории", blank=True)

    image = models.ImageField(upload_to='article_images/', verbose_name='Фотография', null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.title}"
    
    class Meta:
        verbose_name_plural = "Статьи"


class ContactModel(models.Model):
    max_length = 255
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="contacts")
    mail = models.CharField(max_length=max_length, verbose_name='почта')
    telegram = models.CharField(max_length=max_length, verbose_name='telegram', null=True, blank=True)
    message = models.TextField(verbose_name="Сообщение")

    def __str__(self) -> str:
        return f"{self.user}"
    
    class Meta:
        verbose_name_plural = "Сообщения"


class MentorAppointmentModel(ContactModel):
    mentor = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name="Ментор", related_name="mentor_forms")
    description = models.TextField(verbose_name="Текст")

    def __str__(self) -> str:
        return f"Запись к {self.mentor}"

    class Meta:
        verbose_name_plural = "Записи к менторам"


@receiver(post_save, sender=UserModel)
def set_user_active(sender, instance, created, **kwargs):
    if created:
        instance.is_active = True
        instance.save()