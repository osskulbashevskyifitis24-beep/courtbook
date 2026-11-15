# CourtBook

CourtBook — веб-сервіс онлайн-бронювання спортивних майданчиків (тенісні корти,
міні-футбольні поля, баскетбольні майданчики). Гравці бачать вільні слоти та
бронюють їх онлайн, а адміністратори спорткомплексів керують розкладом і цінами.

## Документація
Проєктні документи знаходяться в каталозі `docs/`.

## Architecture
- [Use Case Diagram](docs/diagrams/use_case.png)
- [Class Diagram](docs/diagrams/class.png)
- [Sequence Diagram: бронювання слоту](docs/diagrams/sequence_booking.png)

## Як запустити тести
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest --cov=courtbook
```
