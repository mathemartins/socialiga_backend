from django.conf import settings
from django.db import models

# Create your models here.
from django.db.models import Prefetch, Q
from django.db.models.signals import post_save
from django.urls import reverse

from event.utils import make_display_price


class MyEvents(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    events = models.ManyToManyField('Event', related_name='owned', blank=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.events.all().count())

    class Meta:
        verbose_name = 'My events'
        verbose_name_plural = 'My events'


def post_save_user_create(sender, instance, created, *args, **kwargs):
    if created:
        MyEvents.objects.get_or_create(user=instance)


post_save.connect(post_save_user_create, sender=settings.AUTH_USER_MODEL)


class EventQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(Q(category__slug__iexact='featured'))  # | Q(secondary__slug__iexact='featured'))

    def owned(self, user):
        if user.is_authenticated:
            qs = MyEvents.objects.filter(user=user)
        else:
            qs = MyEvents.objects.none()
        return self.prefetch_related(
            Prefetch('owned', queryset=qs, to_attr='is_owner')
        )


class EventManager(models.Manager):
    def get_queryset(self):
        return EventQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().all().active()
        # return super(CourseManager, self).all()


def handle_upload(instance, filename):
    if instance.slug:
        return "%s/images/%s" % (instance.slug, filename)
    return "unknown/images/%s" % (filename)


class Event(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True)  # unique = False
    image = models.ImageField(upload_to=handle_upload,
                              height_field='image_height',
                              width_field='image_width',
                              blank=True, null=True)
    image_height = models.IntegerField(blank=True, null=True)
    image_width = models.IntegerField(blank=True, null=True)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=100)
    discounts = models.PositiveIntegerField(blank=True, null=True)
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = EventManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("events:detail", kwargs={"slug": self.slug})

    def get_purchase_url(self):
        return reverse("events:purchase", kwargs={"slug": self.slug})

    def display_price(self):
        return make_display_price(self.price)

