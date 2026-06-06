#!/usr/bin/env python3
"""
Modified build_html.py — v2 with layout changes:
- Rating block moved above profile sections
- No static scale labels (1 / 10)
- No comment block
- All sections except КРАТКОЕ РЕЗЮМЕ ЛИЧНОСТИ collapsed by default
- Key: reveal-button hides content until clicked
- Key: no "Логика формирования вариантов"
- Key: cleaned up "Итог" text
"""

import os
import json
import sys

SECTION_HEADERS = [
    "КРАТКОЕ РЕЗЮМЕ ЛИЧНОСТИ",
    "ПСИХОЛОГИЧЕСКАЯ СФЕРА",
    "ФИЗИОЛОГИЯ И СПОРТ",
    "ПРОФЕССИОНАЛЬНАЯ РЕАЛИЗАЦИЯ",
    "ИНТЕРЕСЫ И ХОББИ",
    "СЕМЬЯ И ОТНОШЕНИЯ",
]


def read_txt(folder, name):
    path = os.path.join(folder, name + ".txt")
    with open(path, encoding="utf-8") as f:
        return f.read()


def txt_to_html_sections(raw):
    lines = raw.split("\n")
    sections = []
    current_section = None
    current_items = []

    for line in lines:
        stripped = line.strip()
        if stripped in SECTION_HEADERS:
            if current_section is not None:
                sections.append((current_section, "\n".join(current_items)))
            current_section = stripped
            current_items = []
        elif current_section is not None:
            current_items.append(line)

    if current_section is not None:
        sections.append((current_section, "\n".join(current_items)))

    html = ""
    for sec_title, sec_body in sections:
        body_html = ""
        for para in sec_body.split("\n\n"):
            para = para.strip()
            if not para:
                continue
            if ("." in para[:70] and para[0].isupper()
                    and not para.startswith("—") and len(para.split(".")[0].split()) <= 4):
                dot_idx = para.index(".")
                label = para[:dot_idx].strip()
                rest = para[dot_idx + 1:].strip()
                body_html += f'<p><strong>{label}.</strong> {rest}</p>\n'
            else:
                body_html += f'<p>{para}</p>\n'

        # Only КРАТКОЕ РЕЗЮМЕ ЛИЧНОСТИ is open by default
        is_open = " open" if sec_title == "КРАТКОЕ РЕЗЮМЕ ЛИЧНОСТИ" else ""

        html += f'''
        <details class="section-block"{is_open}>
            <summary class="section-title">{sec_title}</summary>
            <div class="section-body">{body_html}</div>
        </details>'''

    return html


CSS = """
  :root {
    --bg:#f5f4f0; --card:#fff; --accent:#3a5a8c; --accent-light:#e8eef6;
    --text:#1a1a1a; --muted:#666; --border:#ddd; --radius:10px;
    --shadow:0 2px 12px rgba(0,0,0,.08);
  }
  *{box-sizing:border-box;margin:0;padding:0}
  body{font-family:Georgia,serif;background:var(--bg);color:var(--text);line-height:1.75}
  header{background:var(--accent);color:#fff;padding:2rem 1.5rem;text-align:center}
  header h1{font-size:1.6rem;font-weight:normal;letter-spacing:.02em}
  header p{margin-top:.5rem;opacity:.8;font-size:.95rem}
  .container{max-width:860px;margin:0 auto;padding:2rem 1rem}
  .toc-card{background:var(--card);border-radius:var(--radius);box-shadow:var(--shadow);padding:1.5rem 2rem;margin-bottom:2rem}
  .toc-card h2{color:var(--accent);font-size:1.1rem;margin-bottom:1rem;border-bottom:1px solid var(--border);padding-bottom:.5rem}
  .toc-card ol{padding-left:1.5rem}
  .toc-card li{margin:.4rem 0}
  .toc-card a{color:var(--accent);text-decoration:none}
  .toc-card a:hover{text-decoration:underline}
  .intro-card{background:var(--accent-light);border-left:4px solid var(--accent);border-radius:var(--radius);padding:1.25rem 1.5rem;margin-bottom:2rem;font-size:.95rem;color:#2a3a50}
  .profile-card{background:var(--card);border-radius:var(--radius);box-shadow:var(--shadow);margin-bottom:2.5rem;overflow:hidden}
  .profile-header{background:var(--accent);color:#fff;padding:1.25rem 2rem}
  .profile-header h2{font-size:1.3rem;font-weight:normal;letter-spacing:.05em}
  .profile-content{padding:1.5rem 2rem}
  details.section-block{border-bottom:1px solid var(--border)}
  details.section-block:last-of-type{border-bottom:none}
  summary.section-title{font-size:.85rem;font-weight:bold;letter-spacing:.1em;text-transform:uppercase;color:var(--accent);padding:1rem 0;cursor:pointer;list-style:none;display:flex;align-items:center;gap:.5rem}
  summary.section-title::before{content:"▶";font-size:.65rem;transition:transform .2s}
  details[open] summary.section-title::before{transform:rotate(90deg)}
  summary::-webkit-details-marker{display:none}
  .section-body{padding-bottom:1.25rem}
  .section-body p{margin-bottom:.85rem;font-size:.97rem}
  .section-body p:last-child{margin-bottom:0}
  .rating-form{background:#f9f8f5;border-bottom:2px solid var(--accent-light);padding:1.25rem 2rem}
  .rating-title{color:var(--accent);font-size:.95rem;font-weight:bold;margin-bottom:1rem}
  .rating-item label{display:block;font-size:.9rem;margin-bottom:.6rem;color:var(--muted)}
  .scale-inputs{display:flex;gap:.3rem;flex-wrap:wrap;margin-bottom:1rem}
  .scale-btn{display:flex;flex-direction:column;align-items:center;cursor:pointer}
  .scale-btn input{display:none}
  .scale-btn span{width:2rem;height:2rem;border-radius:50%;border:2px solid var(--border);display:flex;align-items:center;justify-content:center;font-size:.8rem;transition:all .15s;background:#fff}
  .scale-btn input:checked + span{background:var(--accent);border-color:var(--accent);color:#fff;font-weight:bold}
  .scale-btn:hover span{border-color:var(--accent)}
  .checkbox-block{margin-top:.25rem}
  .exact-label{display:inline-flex;align-items:center;gap:.6rem;cursor:pointer;user-select:none}
  .exact-label input{display:none}
  .exact-box{display:inline-flex;align-items:center;gap:.5rem;padding:.5rem 1rem;border:2px solid var(--border);border-radius:8px;font-size:.95rem;background:#fff;transition:all .2s}
  .exact-box::before{content:"☐";font-size:1.1rem}
  .exact-label input:checked ~ .exact-box{background:#e8f4e8;border-color:#4a8c4a;color:#2a5a2a;font-weight:bold}
  .exact-label input:checked ~ .exact-box::before{content:"☑"}
  .download-section{text-align:center;padding:2rem 0 1rem}
  #download-btn{background:var(--accent);color:#fff;border:none;padding:.9rem 2.5rem;font-size:1rem;font-family:inherit;border-radius:8px;cursor:pointer;letter-spacing:.02em;transition:background .2s}
  #download-btn:hover{background:#2a4a7c}
  #download-btn::before{content:"↓  "}
  .back-link{text-align:center;margin:.5rem 0 2rem}
  .back-link a{color:var(--accent);font-size:.9rem;text-decoration:none}
  .back-link a:hover{text-decoration:underline}
  @media(max-width:600px){
    .profile-content,.rating-form{padding:1.25rem}
    .scale-inputs{gap:.2rem}
    .scale-btn span{width:1.75rem;height:1.75rem;font-size:.75rem}
  }
  /* Key section embedded in test */
  .key-section{margin-top:3rem;padding-top:2rem;border-top:3px solid var(--accent-light)}
  .key-section .warning{background:#fff3cd;border:1px solid #ffc107;border-radius:6px;padding:1rem 1.25rem;font-size:.9rem;color:#5a4000;margin-bottom:1.5rem}
  .reveal-section{text-align:center;padding:1.5rem 0}
  #reveal-btn{background:var(--accent);color:#fff;border:none;padding:1rem 3rem;font-size:1.05rem;font-family:inherit;border-radius:8px;cursor:pointer;letter-spacing:.02em;transition:background .2s;box-shadow:0 4px 16px rgba(58,90,140,.2)}
  #reveal-btn:hover{background:#2a4a7c}
  #key-content{display:none}
  .key-card{background:var(--card);border-radius:var(--radius);box-shadow:var(--shadow);padding:2rem;margin-bottom:1.75rem}
  .key-card h2{color:var(--accent);font-size:1.1rem;border-bottom:1px solid var(--border);padding-bottom:.6rem;margin-bottom:1rem}
  .key-card p{font-size:.97rem;margin-bottom:.75rem}
  .key-card p:last-child{margin-bottom:0}
  .bd-highlight{background:var(--accent-light);border-left:4px solid var(--accent);padding:.75rem 1rem;border-radius:6px;font-size:1.1rem;font-weight:bold}
  .key-table{width:100%;border-collapse:collapse;font-size:.95rem}
  .key-table th{background:var(--accent);color:#fff;padding:.75rem 1rem;text-align:left;font-weight:normal}
  .key-table td{padding:.75rem 1rem;border-bottom:1px solid var(--border)}
  .key-table tr:last-child td{border-bottom:none}
  .key-table td.cell-label{font-weight:bold;color:var(--accent)}
  .key-table td.highlight{background:#fff3cd;font-weight:bold}
"""

KEY_CSS = """
  :root {
    --bg:#f5f4f0; --card:#fff; --accent:#5a3a8c; --accent-light:#f0eaf8;
    --text:#1a1a1a; --border:#ddd; --radius:10px; --shadow:0 2px 12px rgba(0,0,0,.08);
  }
  *{box-sizing:border-box;margin:0;padding:0}
  body{font-family:Georgia,serif;background:var(--bg);color:var(--text);line-height:1.75}
  header{background:var(--accent);color:#fff;padding:2rem 1.5rem;text-align:center}
  header h1{font-size:1.5rem;font-weight:normal}
  header p{margin-top:.4rem;opacity:.8;font-size:.9rem}
  .container{max-width:760px;margin:0 auto;padding:2rem 1rem}
  .card{background:var(--card);border-radius:var(--radius);box-shadow:var(--shadow);padding:2rem;margin-bottom:1.75rem}
  .card h2{color:var(--accent);font-size:1.1rem;border-bottom:1px solid var(--border);padding-bottom:.6rem;margin-bottom:1rem}
  .card p{font-size:.97rem;margin-bottom:.75rem}
  .card p:last-child{margin-bottom:0}
  .bd-highlight{background:var(--accent-light);border-left:4px solid var(--accent);padding:.75rem 1rem;border-radius:6px;font-size:1.1rem;font-weight:bold;letter-spacing:.03em}
  table{width:100%;border-collapse:collapse;font-size:.95rem}
  th{background:var(--accent);color:#fff;padding:.75rem 1rem;text-align:left;font-weight:normal}
  td{padding:.75rem 1rem;border-bottom:1px solid var(--border)}
  tr:last-child td{border-bottom:none}
  td.cell-label{font-weight:bold;color:var(--accent)}
  td.highlight{background:#fff3cd;font-weight:bold}
  tr:hover td{background:#faf9f7}
  .warning{background:#fff3cd;border:1px solid #ffc107;border-radius:6px;padding:1rem 1.25rem;font-size:.9rem;color:#5a4000}
  .reveal-section{text-align:center;padding:2rem 0}
  #reveal-btn{background:var(--accent);color:#fff;border:none;padding:1rem 3rem;font-size:1.05rem;font-family:inherit;border-radius:8px;cursor:pointer;letter-spacing:.02em;transition:background .2s;box-shadow:0 4px 16px rgba(90,58,140,.25)}
  #reveal-btn:hover{background:#4a2a7c}
  #key-content{display:none}
"""


def make_key_section_html(label_map, labels, date_info, birth_info):
    """Возвращает HTML блока ключа для встраивания в test-файл."""
    bd_label = next(l for l, f in label_map.items() if f.endswith("_BD"))
    birth_date = birth_info.get("date", "—")
    birth_time = birth_info.get("time", "—")
    birth_place = birth_info.get("place", "—")

    rows = ""
    for label in labels:
        fname = label_map[label]
        suffix = fname.replace("west_", "").replace("djo_", "")
        dates_fmt = birth_info.get("dates_formatted", {})
        if suffix in dates_fmt:
            date_str = dates_fmt[suffix].get("date", "—")
            date_type = dates_fmt[suffix].get("type", suffix)
        else:
            info = date_info.get(suffix, {})
            date_str = info.get("date", "—")
            date_type = info.get("type", suffix)
        highlight = ' class="highlight"' if date_type == "Истинная дата" else ""
        rows += f"""
        <tr>
          <td class="cell-label">Профиль {label}</td>
          <td>{date_str}</td>
          <td{highlight}>{date_type}</td>
        </tr>"""

    return f"""
  <div class="key-section">
    <div class="warning">⚠️ Ключ к эксперименту — открывать только после завершения оценки всех профилей.</div>
    <div class="reveal-section">
      <button id="reveal-btn">Посмотреть ключ</button>
    </div>
    <div id="key-content">
      <div class="key-card">
        <h2>Ключ профиля</h2>
        <p>Истинной дате рождения соответствует <strong>Профиль {bd_label}</strong>.</p>
      </div>
      <div class="key-card">
        <h2>Истинная дата рождения</h2>
        <div class="bd-highlight">{birth_date}</div>
        <p style="margin-top:.75rem;font-size:.9rem;color:#666">{birth_time} · {birth_place}</p>
      </div>
      <div class="key-card">
        <h2>Соответствие профилей</h2>
        <table class="key-table">
          <thead><tr><th>Профиль</th><th>Использованная дата</th><th>Тип варианта</th></tr></thead>
          <tbody>{rows}</tbody>
        </table>
      </div>
      <div class="key-card">
        <h2>Итог</h2>
        <p>Верная дата рождения соответствует профилю <strong>{bd_label}</strong>.
        Если вы поставили ему наиболее высокую оценку «Насколько это похоже на меня»,
        то эксперимент что-то да подтверждает в отношении астрологического метода описания личности.</p>
      </div>
    </div>
  </div>"""


def make_test_html(folder, label_map, labels, school_name, school_key, birth_info, date_info=None):
    toc_items = "".join(
        f'<li><a href="#profile-{l}">Профиль {l}</a></li>\n' for l in labels
    )
    profiles_html = ""

    for label in labels:
        fname = label_map[label]
        raw = read_txt(folder, fname)
        sections_html = txt_to_html_sections(raw)

        # Scale buttons — no static labels
        scale_btns = "".join(
            f'<label class="scale-btn"><input type="radio" name="sim_{label}" value="{i}"><span>{i}</span></label>'
            for i in range(1, 11)
        )

        # Rating block (moved above content, no comment)
        rating_html = f"""
      <div class="rating-form">
        <div class="rating-title">Оценка профиля {label}</div>
        <div class="rating-item">
          <label>Насколько это похоже на меня</label>
          <div class="scale-inputs">{scale_btns}</div>
        </div>
        <div class="checkbox-block">
          <label class="exact-label">
            <input type="checkbox" id="exact-{label}" name="exact_{label}">
            <span class="exact-box">Это точно про меня!</span>
          </label>
        </div>
      </div>"""

        profiles_html += f"""
    <section class="profile-card" id="profile-{label}">
      <div class="profile-header"><h2>Профиль {label}</h2></div>
      {rating_html}
      <div class="profile-content">{sections_html}</div>
    </section>"""

    key_section = make_key_section_html(label_map, labels, date_info or {}, birth_info)

    # Истинная дата рождения → YYYYMMDD для имени файла (birth_info.date = "DD-MM-YYYY")
    raw_date = birth_info.get("date", "00000000")
    parts = raw_date.split("-")
    birth_yyyymmdd = (parts[2] + parts[1] + parts[0]) if len(parts) == 3 else raw_date.replace("-", "")

    js_labels = str(labels).replace("'", '"')
    js = f"""
    document.getElementById("reveal-btn").addEventListener("click", function() {{
      document.getElementById("key-content").style.display = "block";
      this.closest(".reveal-section").style.display = "none";
    }});
    document.getElementById("download-btn").addEventListener("click", function() {{
      const labels = {js_labels};
      const results = {{
        school: "{school_key}",
        timestamp: new Date().toISOString(),
        profiles: {{}}
      }};
      labels.forEach(l => {{
        const sim = document.querySelector(`input[name="sim_${{l}}"]:checked`);
        results.profiles[l] = {{
          similarity: sim ? parseInt(sim.value) : null,
          exactlyMe: document.getElementById(`exact-${{l}}`).checked
        }};
      }});
      const blob = new Blob([JSON.stringify(results, null, 2)], {{type: "application/json"}});
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      const _now = new Date();
      const _ts = _now.getFullYear().toString() +
                  String(_now.getMonth()+1).padStart(2,"0") +
                  String(_now.getDate()).padStart(2,"0") +
                  String(_now.getHours()).padStart(2,"0") +
                  String(_now.getMinutes()).padStart(2,"0");
      a.download = "{birth_yyyymmdd}_{school_key}_" + _ts + ".json";
      a.click();
      URL.revokeObjectURL(url);
    }});"""

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Астрологический эксперимент — {school_name}</title>
<style>{CSS}</style>
</head>
<body>
<header>
  <h1>Астрологический эксперимент</h1>
  <p>{school_name}</p>
</header>
<div class="container">
  <div class="intro-card">
    Перед вами четыре психологических описания личности. Прочитайте каждое внимательно и оцените,
    насколько оно точно описывает вас. Секции можно сворачивать и разворачивать.
    По завершении нажмите кнопку внизу страницы, чтобы скачать результаты.
  </div>
  <nav class="toc-card">
    <h2>Оглавление</h2>
    <ol>{toc_items}</ol>
  </nav>
  {profiles_html}
  <div class="download-section">
    <button id="download-btn">Скачать результаты (JSON)</button>
  </div>
  {key_section}
  <div class="back-link"><a href="#">↑ Наверх</a></div>
</div>
<script>{js}</script>
</body>
</html>"""


def make_key_html(label_map, labels, school_name, test_filename, date_info, birth_info):
    # Find which label maps to BD
    bd_label = next(l for l, f in label_map.items() if f.endswith("_BD"))

    birth_date = birth_info.get("date", "—")
    birth_time = birth_info.get("time", "—")
    birth_place = birth_info.get("place", "—")

    rows = ""
    for label in labels:
        fname = label_map[label]
        suffix = fname.replace("west_", "").replace("djo_", "")

        # Try to get date from birth_info.dates_formatted first
        dates_fmt = birth_info.get("dates_formatted", {})
        if suffix in dates_fmt:
            date_str = dates_fmt[suffix].get("date", "—")
            date_type = dates_fmt[suffix].get("type", suffix)
        else:
            info = date_info.get(suffix, {})
            date_str = info.get("date", "—")
            date_type = info.get("type", suffix)

        highlight = ' class="highlight"' if date_type == "Истинная дата" else ""
        rows += f"""
        <tr>
          <td class="cell-label">Профиль {label}</td>
          <td>{date_str}</td>
          <td{highlight}>{date_type}</td>
        </tr>"""

    # Hidden key content (revealed on button click)
    key_content_html = f"""
  <div class="card">
    <h2>Ключ профиля</h2>
    <p>Истинной дате рождения соответствует <strong>Профиль {bd_label}</strong>.</p>
  </div>
  <div class="card">
    <h2>Истинная дата рождения</h2>
    <div class="bd-highlight">{birth_date}</div>
    <p style="margin-top:.75rem;font-size:.9rem;color:#666">{birth_time} · {birth_place}</p>
  </div>
  <div class="card">
    <h2>Соответствие профилей</h2>
    <table>
      <thead>
        <tr><th>Профиль</th><th>Использованная дата</th><th>Тип варианта</th></tr>
      </thead>
      <tbody>{rows}</tbody>
    </table>
  </div>
  <div class="card">
    <h2>Итог</h2>
    <p>Профиль <strong>{bd_label}</strong> соответствует истинной дате рождения.
    Если испытуемый поставил ему наиболее высокую оценку «Насколько это похоже на меня»,
    эксперимент подтверждает способность астрологической интерпретации точно описывать личность.</p>
  </div>"""

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Ключ — {school_name}</title>
<style>{KEY_CSS}</style>
</head>
<body>
<header>
  <h1>Ключ к эксперименту</h1>
  <p>{school_name} · {test_filename}</p>
</header>
<div class="container">
  <div class="card warning">
    ⚠️ Этот документ содержит ключ к слепому тесту. Открывать только после завершения оценки всех профилей.
  </div>
  <div class="reveal-section">
    <button id="reveal-btn">Посмотреть ключ</button>
  </div>
  <div id="key-content">
    {key_content_html}
  </div>
</div>
<script>
  document.getElementById("reveal-btn").addEventListener("click", function() {{
    document.getElementById("key-content").style.display = "block";
    this.closest(".reveal-section").style.display = "none";
  }});
</script>
</body>
</html>"""


def build(folder):
    from datetime import datetime
    now = datetime.now()
    build_ts = now.strftime("%Y%m%d%H%M")

    mapping_path = os.path.join(folder, "mapping.json")
    if not os.path.exists(mapping_path):
        raise FileNotFoundError(f"mapping.json not found in {folder}")

    with open(mapping_path, encoding="utf-8") as f:
        mapping = json.load(f)

    west_map = mapping["west"]
    djo_map  = mapping["djo"]

    birth_info_path = os.path.join(folder, "birth_info.json")
    if os.path.exists(birth_info_path):
        with open(birth_info_path, encoding="utf-8") as f:
            birth_info = json.load(f)
    else:
        birth_info = {"date": "—", "time": "—", "place": "—"}

    raw_date = birth_info.get("date", "00000000")
    parts = raw_date.split("-")
    bd_yyyymmdd = (parts[2] + parts[1] + parts[0]) if len(parts) == 3 else raw_date.replace("-", "")

    date_info = mapping.get("date_info", {
        "BD":    {"label": "BD",    "type": "Истинная дата"},
        "BD+90": {"label": "BD+90", "type": "BD + 90 дней"},
        "BD-90": {"label": "BD-90", "type": "BD − 90 дней"},
        "BD+180":{"label": "BD+180","type": "BD + 180 дней"},
    })

    fname_west = f"{bd_yyyymmdd}_west_{build_ts}.html"
    fname_ind  = f"{bd_yyyymmdd}_ind_{build_ts}.html"

    outputs = [
        (fname_west,
         lambda: make_test_html(folder, west_map, ["A","B","C","D"],
                                "Западная астрология", "west", birth_info, date_info)),
        ("astrology_key_wes.html",
         lambda: make_key_html(west_map, ["A","B","C","D"],
                               "Западная астрология", fname_west,
                               date_info, birth_info)),
        (fname_ind,
         lambda: make_test_html(folder, djo_map, ["K","L","M","N"],
                                "Джйотиш (ведическая астрология)", "ind", birth_info, date_info)),
        ("astrology_key_djo.html",
         lambda: make_key_html(djo_map, ["K","L","M","N"],
                               "Джйотиш (ведическая астрология)", fname_ind,
                               date_info, birth_info)),
    ]

    for fname, builder in outputs:
        html = builder()
        out_path = os.path.join(folder, fname)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        size = os.path.getsize(out_path)
        print(f"✓ {fname}  ({size:,} bytes)")

    print(f"\nВсе файлы сохранены в: {folder}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python build_html_v2.py /path/to/output/folder")
        sys.exit(1)
    folder = sys.argv[1]
    if not os.path.isdir(folder):
        print(f"Error: folder not found: {folder}")
        sys.exit(1)
    build(folder)
