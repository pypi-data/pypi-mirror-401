# 📊 MpetsAPI — API для игры Удивительные питомцы. 
 
Пиши красивый и лаконичный код, забыв про парсинг страниц, обработку ошибок и краши от неожиданных ошибок. Библиотека MpetsApi сделает всё за тебя.
### Установка

1. Иметь ```python3.7+```
2. Скачать и распаковать в папку с проектом.

### Пример использования.
Все доступные методы находятся в файле ```__init__.py``` <br>
Обязательно укажите API ключ от сервиса ruCaptcha.
```python
import asyncio

from mpets import MpetsApi


async def main(name, password, rucaptcha_api):
    mpets = MpetsApi(name=name, password=password,
                     rucaptcha_api=rucaptcha_api, timeout=5, fast_mode=True)
    resp = await mpets.login()
    if resp.status is False:
        print(f"Авторизация не удалась: {resp}")
        return False
    profile = await mpets.profile()
    if profile.status is False:
        print(f"Не удалось получить профиль: {profile}")
    print(f"Profile: {profile}")
    await mpets.close()
    

if __name__ == '__main__':
    name = ""
    password = ""
    rucaptcha_api = ""
    asyncio.run(main(name=name,
                     password=password,
                     rucaptcha_api=rucaptcha_api))
```

## Авторы

👦 **Ильдар**

* Telegram: [@wilidon](https://t.me/wilidon) 
* Github: [@wilidon](https://github.com/wilidon)