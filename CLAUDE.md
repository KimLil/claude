# Astro Experiments — инструкции для Claude Code

## Главный skill

При запросе на проведение слепого астрологического эксперимента — читать и выполнять:
`skills/astro-blind-experiment/SKILL.md`

Триггерные фразы: "слепой эксперимент", "астрологический профиль",
"blind astrology test", "натальная карта профиль личности".

## Структура проекта

```
astro-experiments/
├── CLAUDE.md                          ← этот файл
├── skills/
│   └── astro-blind-experiment/
│       ├── SKILL.md                   ← основной skill
│       ├── scripts/
│       │   ├── randomize.py           ← рандомизация профилей
│       │   └── build_html.py          ← сборка HTML-файлов
│       └── references/
│           ├── western_archetypes.md  ← архетипы западной астрологии
│           └── jyotish_archetypes.md  ← архетипы Джйотиш
└── experiments/                       ← сюда генерируются результаты
    └── bd_YYYYMMDD_HHMM/             ← папка каждого эксперимента
```

## Публикация на GitHub Pages

После завершения каждого эксперимента выполнить:

```bash
git add experiments/
git commit -m "experiment: bd_YYYYMMDD_HHMM"
git push origin main
```

Страница появится по адресу:
`https://<username>.github.io/<repo>/experiments/<папка>/`

## Важно

- Все результаты сохранять в папку `experiments/`
- Никогда не коммитить в корень репозитория
- Python-скрипты запускать из корня проекта
