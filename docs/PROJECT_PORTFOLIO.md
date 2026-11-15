# Project Portfolio: CourtBook

## Команда
| Учасник | Роль |
|---------|------|
| Скульбашевський Олександр | Project Lead / Analyst / Developer |

## Репозиторій
- GitHub: https://github.com/osskulbashevskyifitis24-beep/courtbook
- CI Status: ![CI](https://github.com/osskulbashevskyifitis24-beep/courtbook/actions/workflows/ci.yml/badge.svg)

## Артефакти за лабораторними роботами
| ЛР | Тема | Документи/Артефакти | Посилання |
|----|------|---------------------|-----------|
| ЛР1 | Ідея та середовище | Бриф, Бачення, Специфікація v0.1 | docs/ |
| ЛР2 | Вимоги (SRS) | SRS.docx, User Stories, GitHub Issues | docs/, Issues |
| ЛР3 | Планування (Agile) | Kanban, Roadmap, project_plan.docx | Projects tab |
| ЛР4 | BPMN | booking_process.drawio / .png | docs/diagrams/ |
| ЛР5 | Архітектура (UML) | use_case, class, sequence_booking | docs/diagrams/ |
| ЛР6 | Розробка (Git) | PR #13 (US-001), commit history | PRs tab |
| ЛР7 | Метрики та рефакторинг | CC 16 -> 2, PR refactor | docs/, PRs tab |
| ЛР8 | Тестування | test_plan.docx, 26 unit-тестів | docs/, tests/ |
| ЛР9 | CI/CD | ci.yml, CI badge | .github/workflows/ |

## Ключові рішення проєкту
- Python 3.11 + Flask: простий стек для MVP одного розробника
- GitHub Flow: короткі feature-гілки, Squash and merge
- Dependency Injection репозиторію -> тести без реальної БД
- Блокування слоту в транзакції для захисту від подвійного бронювання
- Оплата віднесена до Should Have, щоб не блокувати MVP

## Використання ШІ у проєкті
- ЛР1: Claude – генерація та оцінка ідей
- ЛР2: Claude – User Stories, GWT, перевірка повноти вимог
- ЛР3: Claude – MoSCoW, Story Points, ризики
- ЛР4: Claude – сценарій процесу, перевірка BPMN
- ЛР5: Claude – генерація PlantUML (Use Case, Class, Sequence)
- ЛР6: GitHub Copilot – код; Copilot Code Review + Claude – рев'ю
- ЛР7: Claude + SonarLint – метрики, SOLID, рефакторинг
- ЛР8: Copilot /tests + Claude – генерація тестів
- ЛР9: Claude – генерація workflow CI
