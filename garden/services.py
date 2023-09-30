import threading

from decouple import config
from eskiz.client import SMSClient

from .models import Contact

email = config('email', '')
pswd = config('password', '')
client = SMSClient(
    api_url="https://notify.eskiz.uz/api/",
    email=email,
    password=pswd,
)


def get_order_shablon(garden_name):
    msg = f"""{garden_name} tomonidan yangi buyurtma qoldirildi
    """
    return msg


def add_contact(phone_number, name):
    contact, _ = Contact.objects.get_or_create(phone_number=phone_number)
    if _:
        client._add_sms_contact(
            first_name=name,
            phone_number=phone_number,
            group="Garden"
        )


def send_sms_order(phone_number, data, name=""):
    # sms_thread = threading.Thread(target=send_sms, args=(message, recipient))

    # # Start the thread
    # sms_thread.start()

    # # You can continue with other tasks here

    # # Wait for the SMS thread to finish (optional)
    # sms_thread.join()
    phone_number = phone_number.replace('+', '')
    add_contact(phone_number=phone_number, name=name)
    res = client._send_sms(
        phone_number=phone_number, message=get_order_shablon(data)
    )

    print(res)
