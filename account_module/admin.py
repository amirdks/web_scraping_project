from django.contrib import admin

from account_module.models import User, Wallet, Transaction

# Register your models here.

admin.site.register(User)
admin.site.register(Wallet)
admin.site.register(Transaction)
