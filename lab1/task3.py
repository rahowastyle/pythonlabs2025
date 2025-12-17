#  Статистика продажів. Створіть список словників, де кожен словник представляє 
#  продаж з ключами: "продукт", "кількість", "ціна". Напишіть функцію, яка обчислює
#  загальний дохід для кожного продукту та повертає словник, де ключі - це назви продуктів,
#  а значення - загальний дохід. Створіть список продуктів, що принесли дохід більший ніж 1000.

def calculate_revenue(sales_list):
    revenue_dict = {}
  
  for sale in sales_list:
        prod_name = sale.get("product")
        qty = sale.get("quantity")
        price = sale.get("price")
        
        income = qty * price
        
        # if in revenue - add, else - create
        if prod_name in revenue_dict:
            revenue_dict[prod_name] += income
        else:
            revenue_dict[prod_name] = income
    return revenue_dict

def filter_high_revenue(rev_dict, threshold=1000):
    return [prod for prod, income in rev_dict.items() if income > threshold]
  
if __name__ == "__main__":
    sales_data = [
        {"product": "Laptop", "quantity": 2, "price": 1500},  #  3000
        {"product": "Mouse", "quantity": 10, "price": 20},    # 200
        {"product": "Monitor", "quantity": 5, "price": 300},  #  1500
        {"product": "Mouse", "quantity": 5, "price": 20},     #разом 300
        {"product": "Keyboard", "quantity": 10, "price": 50}, # 500
    ]

    total_revenues = calculate_revenue(sales_data)
    print("Загальний дохід по продуктах:", total_revenues)
    
    # >1000
    best_sellers = filter_high_revenue(total_revenues, 1000)
    print("Продукти з доходом > 1000:", best_sellers)
