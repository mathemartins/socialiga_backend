from billing.utils import PaystackAPI, SECRET_KEY
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.urls import reverse

User = get_user_model()

# Initialize the PaystackAPI Instance
ps_instance = PaystackAPI(secret_key=SECRET_KEY)


class BillingProfileManager(models.Manager):
    def new_or_get(self, request):
        user = request.user
        created = False
        obj = None
        if user.is_authenticated:
            'logged in user checkout; remember payment stuff'
            obj, created = self.model.objects.get_or_create(
                user=user, email=user.email)
        return obj, created


class BillingProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField()
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    customer_id = models.CharField(max_length=120, null=True,
                                   blank=True)  # customer_id in Stripe, Braintree or Paystack

    objects = BillingProfileManager()

    def __str__(self):
        return self.email

    def charge(self, order_obj, card=None):
        return Charge.objects.do(self, order_obj, card)

    def get_cards(self):
        return self.card_set.all()

    def get_payment_method_url(self):
        return reverse('billing-payment-method')

    @property
    def has_card(self):  # instance.has_card
        card_qs = self.get_cards()
        return card_qs.exists()  # True or False

    @property
    def default_card(self):
        default_cards = self.get_cards().filter(active=True, default=True)
        if default_cards.exists():
            return default_cards.first()
        return None

    def set_cards_inactive(self):
        cards_qs = self.get_cards()
        cards_qs.update(active=False)
        return cards_qs.filter(active=True).count()


def billing_profile_created_receiver(sender, instance, *args, **kwargs):
    if not instance.customer_id and instance.email:
        print("ACTUAL API REQUEST Send to Paystack")
        customer = ps_instance.create_customer(email=instance.email)
        print(customer)
        instance.customer_id = customer['data']['id']


pre_save.connect(billing_profile_created_receiver, sender=BillingProfile)


def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance, email=instance.email)


post_save.connect(user_created_receiver, sender=User)


class CardManager(models.Manager):
    def all(self, *args, **kwargs):  # ModelKlass.objects.all() --> ModelKlass.objects.filter(active=True)
        return self.get_queryset().filter(active=True)

    def add_new(self, billing_profile, card_data: dict):
        if card_data:
            customer: dict = ps_instance.get_customer(paystack_cus_id=billing_profile.customer_id)
            paystack_id = customer['data'].get('id')
            new_card = self.model(
                billing_profile=billing_profile,
                paystack_id=paystack_id,
                brand=card_data.get('brand'),
                country=card_data.get('country'),
                exp_month=card_data.get('exp_month'),
                exp_year=card_data.get('exp_year'),
                card_number=card_data.get('card_number'),
            )
            new_card.save()
            return new_card
        return None


class Card(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    paystack_id = models.CharField(max_length=120)
    brand = models.CharField(max_length=120, null=True, blank=True)
    country = models.CharField(max_length=20, null=True, blank=True)
    exp_month = models.IntegerField(null=True, blank=True)
    exp_year = models.IntegerField(null=True, blank=True)
    card_number = models.CharField(max_length=4, null=True, blank=True)
    default = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CardManager()

    def __str__(self):
        return "{} {}".format(self.brand, self.card_number)

    def get_last4(self):
        return self.card_number[-4]


def new_card_post_save_receiver(sender, instance, created, *args, **kwargs):
    if instance.default:
        billing_profile = instance.billing_profile
        qs = Card.objects.filter(billing_profile=billing_profile).exclude(pk=instance.pk)
        qs.update(default=False)


post_save.connect(new_card_post_save_receiver, sender=Card)


class ChargeManager(models.Manager):
    def do(self, billing_profile, order_obj, card=None):  # Charge.objects.do()
        card_obj = card
        if card_obj is None:
            cards = billing_profile.card_set.filter(default=True)  # card_obj.billing_profile
            if cards.exists():
                card_obj = cards.first()
        if card_obj is None:
            return False, "No cards available"
        c = ps_instance.charge(
            amount=int(order_obj.total * 100),  # 39.19 --> 3919
            currency="usd",
            customer=billing_profile.customer_id,
            source=card_obj.stripe_id,
            metadata={"order_id": order_obj.order_id},
        )
        new_charge_obj = self.model(
            billing_profile=billing_profile,
            stripe_id=c.id,
            paid=c.paid,
            refunded=c.refunded,
            outcome=c.outcome,
            outcome_type=c.outcome['type'],
            seller_message=c.outcome.get('seller_message'),
            risk_level=c.outcome.get('risk_level'),
        )
        new_charge_obj.save()
        return new_charge_obj.paid, new_charge_obj.seller_message


class Charge(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    paystack_id = models.CharField(max_length=120)
    paid = models.BooleanField(default=False)
    refunded = models.BooleanField(default=False)
    outcome = models.TextField(null=True, blank=True)
    outcome_type = models.CharField(max_length=120, null=True, blank=True)
    seller_message = models.CharField(max_length=120, null=True, blank=True)
    risk_level = models.CharField(max_length=120, null=True, blank=True)

    objects = ChargeManager()
