Система 'Служба Таксі'
======================
Посилання на гітхаб: https://github.com/MarkiianMazur/Mazur_Taxi
Для запуску програми необхідно:
Встановити Python 3.10 та виконати наступні команди:
```shell
from src.models import *
connection.get_database().create_tables([Passenger, Taxi, Order, Offer])
```

```shell
pip install -r requirements.txt
python main.py
```