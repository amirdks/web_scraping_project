from django.conf import settings
from django.db import models, transaction, IntegrityError
from django.db.models.signals import post_save
from django.dispatch import receiver

from account_module.models import User


class Wallet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    current_balance = models.PositiveIntegerField(default=0)
    updated_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "user : {0} => {1}".format(self.user.email, self.current_balance)

    @transaction.atomic
    def deposit(self, value):
        self.transaction_set.create(
            value=value,
            running_balance=self.current_balance + value
        )
        self.current_balance += value
        self.save()

    @transaction.atomic
    def withdraw(self, value):
        print(f"value => {value}")
        print(f"balance => {self.current_balance}")
        if value > self.current_balance:
            print("errored")
            raise self.InsufficientBalance('This wallet has insufficient balance.')
        # self.transaction_set.create(
        #     value=-value,
        #     running_balance=self.current_balance - value
        # )
        self.current_balance -= value
        self.save()

    class InsufficientBalance(IntegrityError):
        pass


class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    value = models.PositiveIntegerField(default=0)
    running_balance = models.PositiveIntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{0} => {1} : {2}".format(self.wallet.user, self.running_balance, self.created_date)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance)
