from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string
from django.core.validators import MinValueValidator, MaxValueValidator

from app.courses.fields import OrderField

User = get_user_model()


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=200)

    class Meta:
        abstract = True

    @classmethod
    def generate_unique_slug(cls, value):
        origin_slug = slugify(value)
        unique_slug = origin_slug
        numb = 1
        while cls.objects.filter(slug=unique_slug).exists():
            unique_slug = "%s-%d" % (origin_slug, numb)
            numb += 1
        return unique_slug

    def save(self, *args, **kwargs):
        self.slug = self.generate_unique_slug(self.title)
        super().save(*args, **kwargs)


class Subject(BaseModel):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(
        max_length=200, unique=True, unique_for_date="created"
    )

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Course(BaseModel):
    owner = models.ForeignKey(
        User, related_name="courses_created", on_delete=models.CASCADE
    )
    subject = models.ForeignKey(
        Subject, related_name="courses", on_delete=models.CASCADE
    )
    slug = models.SlugField(
        max_length=200, unique=True, unique_for_date="created"
    )
    overview = models.TextField(blank=True)
    image = models.ImageField(
        upload_to="images", blank=True, default="default.jpg"
    )

    students = models.ManyToManyField(
        User, related_name="courses_joined", blank=True
    )

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.title


class Rating(models.Model):
    user = models.ForeignKey(
        User, related_name="user_rating", on_delete=models.CASCADE
    )
    course = models.ForeignKey(
        Course, related_name="ratings", on_delete=models.CASCADE
    )
    value = models.IntegerField(
        verbose_name="Rating",
        validators=[MinValueValidator(0), MaxValueValidator(5)],
    )

    class Meta:
        unique_together = ("user", "course")


class Module(models.Model):
    course = models.ForeignKey(
        Course, related_name="modules", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=["course"])

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return "<Module {}. {}>".format(self.order, self.title)


class Content(models.Model):
    module = models.ForeignKey(
        Module, related_name="contents", on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey("content_type", "object_id")
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={"model__in": ("text", "video", "image", "file")},
    )
    order = OrderField(blank=True, for_fields=["module"])

    class Meta:
        ordering = ["order"]


class ModuleContentType(models.Model):
    owner = models.ForeignKey(
        User, related_name="%(class)s_related", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def render(self):
        return render_to_string(
            "course/{}.html".format(self._meta.model_name), {"item": self}
        )


class Text(ModuleContentType):
    content = models.TextField()


class File(ModuleContentType):
    file = models.FileField(upload_to="files")


class Image(ModuleContentType):
    file = models.ImageField(upload_to="images", default="default.jpg")


class Video(ModuleContentType):
    url = models.URLField(blank=True)
