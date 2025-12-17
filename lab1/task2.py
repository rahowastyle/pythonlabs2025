#  Створіть словник, де ключі - це назви продуктів, а значення - їх кількість на складі. 
#  Напишіть функцію, яка приймає назву продукту та кількість, і оновлює словник відповідно 
#  до додавання або видалення продуктів. 
#  Додатково: створіть список продуктів, в яких кількість менше ніж 5.

inventory = {
    "apple": 10,
    "banan": 5,
    "orange": 2,
    "moloko": 4
}

def update_inventory(inv_dict, product, quantity):
    if product in inv_dict:
        inv_dict[product] += quantity
        if inv_dict[product] < 0:
            inv_dict[product] = 0
    else:
        if quantity > 0:
            inv_dict[product] = quantity

def check_low_stock(inv_dict, limit=5):
    return [item for item, qty in inv_dict.items() if qty < limit]

if __name__ == "__main__":
    print("Початковий склад:", inventory)

    update_inventory(inventory, "apple", 5)
    update_inventory(inventory, "banan", -2)  # стало 3
    update_inventory(inventory, "bread", 10)
    
    print("оновлений склад:", inventory)

    low_stock_items = check_low_stock(inventory)
    print("Продукти яких >5", low_stock_items)
