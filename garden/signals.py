import math

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ExcelFile, Garden, Limit, LimitItem, Product
from .serializers import get_current_monthly


@receiver(post_save, sender=ExcelFile)
def my_model_post_save(sender, instance, created, **kwargs):
    product_list = garden_list = []
    try:
        if created:
            import pandas as pd

            excel_file_path = instance.excel_file
            df = pd.read_excel(excel_file_path)
            row_dict_list = df.to_dict(orient='records')
            monthly = get_current_monthly()
            objects = []
            for i in row_dict_list:
                i.pop('T/r')
                name = i.pop('Mahsulot nomi')
                count = i.pop('Miqdori')
                price = i.pop('Narxi')
                summa = i.pop('Summasi')
                shop_price = i.pop('Bozor narxi')
                total_sum = i.pop('Umumiy summa')
                measure = i.pop("O'lchov birligi")
                product, _ = Product.objects.get_or_create(name=name)
                if _:
                    product.measure = measure
                    product.save()
                    product_list.append(product)
                for j in i.keys():
                    cnt = i.get(j)
                    if isinstance(cnt, float) or math.isnan(cnt) or cnt == 0:
                        continue
                    try:
                        cnt = float(cnt)
                    except:
                        continue

                    garden, is_avialibel = Garden.objects.get_or_create(name=j)
                    if is_avialibel:
                        garden_list.append(garden)

                    limit, _ = Limit.objects.get_or_create(
                        monthly=monthly, garden=garden)
                    obj = LimitItem(limit=limit, product=product, limit_quantity=cnt,
                                    remaining_quantity=cnt, price=price, market_price=shop_price
                                    )
                    objects.append(obj)
            LimitItem.objects.bulk_create(objects)
    except:
        Product.objects.filter(
            pk__in=[product.pk for product in product_list]).delete()
        Garden.objects.filter(
            pk__in=[garden.pk for garden in garden_list]).delete()
        instance.delete()
