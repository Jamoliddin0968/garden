
names="Garden,Product,Sell,SellItem,Order,OrderItem,Monthly,MonthlyItem,Expense,ExpenseItem,Storage"
names = list(names.split(',')) 
for User in names:
    print(f"""
router.register(r'{User}', {User}ViewSet)
""")