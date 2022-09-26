from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Account(models.Model):
    number = models.IntegerField()
    description = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    should_debit_balance = models.BooleanField(default=True)
    credit_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    debit_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    category = models.ForeignKey(
        "AccountCategory", on_delete=models.CASCADE, related_name="accounts"
    )

    @property
    def balance(self):
        return (
            self.debit_balance - self.credit_balance
            if self.should_debit_balance
            else self.credit_balance - self.debit_balance
        )


class AccountCategory(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    group = models.CharField(
        max_length=2,
        choices=[
            ("AS", _("Assets")),
            ("LI", _("Liabilities")),
            ("CA", _("Capital")),
            ("RV", _("Revenue")),
            ("EX", _("Expense")),
        ] 
    )
    supercategory = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name="subcategories",null=True 
    )

    def get_all_accounts(self):
        return Account.objects.filter(category=self)