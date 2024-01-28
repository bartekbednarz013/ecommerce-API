# Aplikacja e-commerce
Baza zawiera jedną kategorię produktów, cztery przykładowe produkty i trzech użytkowników:
- klient - login: client, hasło: client
- sprzedawca - login: seller, hasło: seller
- administrator - login: admin, hasło: admin

## Endpoints
| Metoda | Endpoint | Dane wejściowe | Dostęp | Działanie |
| :-: | - | - | :-: | --- |
| POST | /api/order | JSON:<br>-„client_name” - imię i nazwisko klienta [str]<br>-„delivery_address” - adres [str]<br>-„products_list” - lista obiektów {„id” - id produktu [int], „quantity” - ilość [int/float]} [JSON] | grupa "Clients" | składanie zamówienia |
| GET | /api/product/ |  | wszyscy | wyświetlanie wszystkich produktów |
| GET | /api/product/<product_id>/ |  | wszyscy | wyświetlenie szczegółów wskazanego produktu |
| POST | /api/product/ | JSON:<br>-„name” - nazwa [str]<br>-„description” - opis [str]<br>-„price” - cena [float]<br>-„category” - id kategorii [int]<br>-„image” - zdjęcie produktu | grupa "Sellers" | dodawanie produktu |
| PUT, PATCH | /api/product/<product_id>/ | JSON: wybrane pola jak wyżej | grupa "Sellers" | edytowanie wskazanego produktu |
| DELETE | /api/product/<product_id>/ |  | grupa "Sellers" | usuwanie wskazanego produktu |
| GET | /api/statistics | Query params:<br>-„from_date” - data w formacie rrrr-mm-dd<br>-„to_date” - data w formacie rrrr-mm-dd<br>-„count” - liczba produktów [int] | grupa "Sellers" | wyświetlenie statystyki najczęściej zamawianych produktów |

<br>Panel administracyjny dostępny pod adresem: ```http://127.0.0.1:8080/admin/```. 
<br><br>
## Uruchomienie
Wymagany Docker.
<br><br>
**1. Sklonuj repozytorium.**
```
git clone https://github.com/bartekbednarz013/ecommerce-API.git
```
**2. Przejdź do katalogu ecommerce-API.**
```
cd ecommerce-API
```
**3. Zbuduj kontener.**
```
docker compose build
```
**4. Uruchom kontener.**
```
docker compose up
```
**5. Otwórz** ```http://127.0.0.1:8080/swagger/``` **w przeglądarce by wygodnie skorzystać z API.**
