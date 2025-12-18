import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

dates = []
rates = []

for i in range(7):

    day = datetime.now() - timedelta(days=6-i)
    api_date = day.strftime("%Y%m%d") 
    plot_date = day.strftime("%d.%m") 

    url = f"https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode=USD&date={api_date}&json"
    response = requests.get(url).json()

    dates.append(plot_date)
    rates.append(response[0]['rate'])

plt.figure(figsize=(10, 5))
plt.plot(dates, rates, marker='o', color='green', label='USD')

plt.title('Курс долара НБУ (останні 7 днів)')
plt.xlabel('Дата')
plt.ylabel('Курс (грн)')
plt.grid(True)
plt.legend()

plt.show()
