from django.db.models.signals import post_save
from django.contrib.auth.models import Group
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models


class Books(models.Model):

    name_book = models.CharField("Nome do Livro", max_length=255)

    def __str__(self):
        return self.name_book


class Post(models.Model):

    """
    por padrão o django cria as segintes permissões
        user.add_post
        user.change_post
        user.delete_post
        user.view_post
    """

    title = models.CharField("Tituto")

    def __str__(self):
        return self


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O endereço de e-mail é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class MyCustomUser(AbstractBaseUser, PermissionsMixin):

    """
    O criador pode  criar  alterar excluir e visualizar
    o viewer só pode ver
    O editor editar ou olha
    """

    CREATOR = 1
    VIEWER = 2
    EDITOR = 3

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name='groups_set'  # Defina um related_name personalizado
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='user_permissions_set'  # Defina um related_name personalizado
    )

    ROLE_CHOICES = (
        (CREATOR, 'Criador'),
        (VIEWER, 'Viewer'),
        (EDITOR, 'Editor'),
    )
    role = models.PositiveSmallIntegerField(
        choices=ROLE_CHOICES, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Usuarios Customizados"

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

    def save(self):
        super().save()


doctor_group, created = Group.objects.get_or_create(name='Doctor')


@receiver(post_save, sender=MyCustomUser)
def set_group_and_permissions(sender, instance, **kwargs):
    """
     try number is one he is one a Creator
    """
    if instance.role == 1:
        editor_group, created = Group.objects.get_or_create(name='Criador')
        permission = Permission.objects.filter(
            codename__in=["add_post", "change_post", "delete_post", "view_post"])
        for item in permission:
            instance.user_permissions.add(item)
            editor_group.permissions.add(item)

        editor_group.save()
        instance.groups.add(editor_group)

    if instance.role == 2:
        viewer_group, created = Group.objects.get_or_create(name='Viwer')
        permission = Permission.objects.filter(codename__in=["view_post"])
        for item in permission:
            instance.user_permissions.add(item)
            viewer_group.permissions.add(item)

        viewer_group.save()
        instance.groups.add(viewer_group)

    if instance.role == 3:
        editor_group, created = Group.objects.get_or_create(name='Editor')
        permission = Permission.objects.filter(
            codename__in=["change_post", "view_post"])
        for item in permission:
            instance.user_permissions.add(item)
            editor_group.permissions.add(item)

        editor_group.save()
        instance.groups.add(editor_group)
    return instance
