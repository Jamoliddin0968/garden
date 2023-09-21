
names="Garden,Product,Sell,SellItem,Order,OrderItem,Monthly,MonthlyItem,Expense,ExpenseItem,Storage"
names = list(names.split(',')) 
# for User in names:
#     print(f"""
# router.register(r'{User}', {User}ViewSet)
# """)
from datetime import datetime

# Get the current date
current_month_number = datetime.now().month

print(f"The current month number is: {current_month_number}")
MONTH_NAMES = (('Yanvar', 'Yanvar'), ('Fevral', 'Fevral'), ('Mart', 'Mart'), ('Aprel', 'Aprel'), ('May', 'May'), ('Iyun', 'Iyun'),
               ('Iyul', 'Iyul'), ('Avgust', 'Avgust'), ('Sentyabr', 'Sentyabr'), ('Oktyabr', 'Oktyabr'), ('Noyabr', 'Noyabr'), ('Dekabr', 'Dekabr'))
for i in MONTH_NAMES:
    print(f"'{i[0]}'",end=",")