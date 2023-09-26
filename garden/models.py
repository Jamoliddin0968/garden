from django.db import models

MONTH_NAMES = (('Yanvar', 'Yanvar'), ('Fevral', 'Fevral'), ('Mart', 'Mart'), ('Aprel', 'Aprel'), ('May', 'May'), ('Iyun', 'Iyun'),
               ('Iyul', 'Iyul'), ('Avgust', 'Avgust'), ('Sentyabr', 'Sentyabr'), ('Oktyabr', 'Oktyabr'), ('Noyabr', 'Noyabr'), ('Dekabr', 'Dekabr'))
# Create your models here.


class Monthly(models.Model):
    """
        Yangi oylik davr
        HUJJAT modeli
    """
    month = models.CharField(max_length=10, choices=MONTH_NAMES)
    year = models.CharField(max_length=4)
    is_active = models.BooleanField(
        default=True, help_text="Agar bu oylik hisobot tugatilsa bu atribut false bo'ladi")

    def __str__(self) -> str:
        return self.year+' '+self.month



class Garden(models.Model):
    name = models.CharField(max_length=255)
    person = models.CharField(max_length=63)
    phone_number = models.CharField(max_length=15)

    def __str__(self) -> str:
        return f"{self.name}"
    
    class Meta:
        verbose_name = "Bog'cha"
        verbose_name_plural = "Bog'chalar"


class Product(models.Model):
    name = models.CharField(max_length=255)
    measure = models.CharField(max_length=15)

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"


class Sell(models.Model):
    """
        Yetkazib berilgan tovarlar uchun
        HUJJAT modeli
    """
    monthly = models.ForeignKey(Monthly, on_delete=models.CASCADE)
    garden = models.ForeignKey(Garden, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.garden} {self.date}"


class SellItem(models.Model):
    """
        Yetkazob berilgan tovarlar hujjati tarkibi
    """
    sell = models.ForeignKey(Sell, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField()
    price = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.sell.garden} {self.product}"


class Order(models.Model):
    """
        Buyurtma uchun
        HUJJAT modeli
    """
    monthly = models.ForeignKey(Monthly, on_delete=models.CASCADE)
    garden = models.ForeignKey(Garden, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.garden} {self.date}"
    
    class Meta:
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"


class OrderItem(models.Model):
    """
        Buyurtma hujjati tarkibi
    """
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField()

    def __str__(self) -> str:
        return f"{self.order} {self.product}"


class Limit(models.Model):
    monthly = models.ForeignKey(Monthly, on_delete=models.CASCADE)
    garden = models.ForeignKey(Garden, on_delete=models.CASCADE)


class LimitItem(models.Model):
    """
        Yangi oylik davr
        HUJJAT modeli tarkibi
    """
    limit = models.ForeignKey(Limit, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    limit_quantity = models.FloatField(default=0)
    remaining_quantity = models.FloatField(default=0)
    price = models.IntegerField(default=0)
    market_price = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.product.name


class Expense(models.Model):
    """ 
        Xarajat hujjati modeli
    """
    monthly = models.ForeignKey(
        Monthly, verbose_name="Oy", on_delete=models.CASCADE)
    date = models.DateField(verbose_name="Kun",  auto_now_add=True)
    total_amount = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.monthly} {self.date}"
    
    class Meta:
        verbose_name = "Xarajat"
        verbose_name_plural = "Xarajatlar"


class ExpenseItem(models.Model):
    """
       Xarajat hujjati tarkibi
    """
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField()
    price = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.monthly} {self.product}"


class Storage(models.Model):
    """ 
        ombor hujjati
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    balance = models.FloatField(verbose_name="Qoldiq", default=0)

    def __str__(self) -> str:
        return f"{self.product}"

    class Meta:
        verbose_name = "Ombor"
        verbose_name_plural = "Ombor"
