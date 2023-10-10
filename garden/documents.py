from datetime import datetime

import pdfkit
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.files import File
from docxtpl import DocxTemplate

from .models import Documents, Garden, Limit, LimitItem


def get_format_number(number):
    if number % 1 == 0:
        number = int(number)
    return "{:,}".format(number).replace(',', ' ')


def get_hisob_factura(monthly_id, garden_id):
    # our template file containing the table
    filename = staticfiles_storage.open("temp.docx")
    template = DocxTemplate(f"{filename}")
    limit, _ = Limit.objects.get_or_create(
        monthly_id=monthly_id, garden_id=garden_id)
    garden = Garden.objects.filter(id=garden_id).first()
    # Create a context dictionary with employee data to be inserted
    # into the template
    objects = LimitItem.objects.filter(limit=limit).select_related('product')
    yetkazib_beruvchi = "Muhammadqodir"
    my_adress = "Toshloq"
    telefon = "+9983698008"
    stir = "7895152"
    xaridor = garden.name
    xaridor_adress = garden.adress
    xaridor_telefon = garden.phone_number
    xaridor_stir = garden.stir
    receiver_name = garden.person.title()
    curier_name = "Muhammadqodir"
    items = list()
    cnt = 0
    total_summa = 0
    for item in objects:
        cnt += 1

        temp_dict = {
            "id": cnt,
            "name": item.product.name,
            "measure": item.product.measure,
            "price": get_format_number(item.price),
            "quantity": get_format_number(item.limit_quantity),
            'summa': get_format_number(item.price*item.limit_quantity)
        }
        total_summa += int(item.price*item.limit_quantity)
        items.append(temp_dict)
    context = {
        "yetkazib_beruvchi": yetkazib_beruvchi,
        "my_adress": my_adress,
        "telefon": telefon,
        'stir': stir,
        'xaridor_stir': xaridor_stir,
        'xaridor': xaridor,
        "xaridor_adress": xaridor_adress,
        "xaridor_telefon": xaridor_telefon,
        "items": items,
        'total_summa': get_format_number(total_summa),
        'receiver_name': receiver_name,
        'curier_name': curier_name
    }

    # Render the template with the context data
    template.render(context)
    now = datetime.now()
    filename = now.strftime("%Y-%m-%d-%H-%M-%S")
    base_file_path = f"documents/{filename}"
    filename = f'{base_file_path}.docx'
    # pdffilepath = f'{base_file_path}.pdf'
    # Save the generated document to a new file
    instanse = Documents()
    template.save(filename)
    with open(filename, 'rb') as file:
        instanse.file.save(filename, File(file))
    return instanse
