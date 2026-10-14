# -*- coding: utf-8 -*-
"""
磊毛阅读 聚合源 · 生成脚本

用法：
    python tools/gen.py <lexxx-backup-YYYYMMDD-HHMMSS.json>

从「磊毛阅读」的云备份 JSON 里抽出全部源，生成可直接一键导入的聚合包：

    novel.json           legado 书源数组（小说）
    comic-legado.json    legado 书源数组（漫画）
    video.json           MoonTV 配置（影视）
    video-18.json        MoonTV 配置（影视 · 成人）
    venera/index.json    Venera 源索引（同目录 .js 为源码）
    venera/<key>.js      Venera 源源码
    manifest.json        包清单（供工具读取）
    README.md / index.html  自动生成的说明与索引页

备份文件结构：{"app":"leimao-reader","sources":[{"type","format","name","rawContent",...}]}
"""
import html
import json
import os
import re
import sys

RAW_BASE = "https://raw.githubusercontent.com/leimao2333/leimao-sources/main"
PAGES_BASE = "https://leimao2333.github.io/leimao-sources"
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_backup(path):
    d = json.load(open(path, encoding="utf-8"))
    if d.get("app") != "leimao-reader":
        raise SystemExit("不是磊毛阅读的备份文件：app=%r" % d.get("app"))
    return d


def dump(obj, rel, indent=2):
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p) or OUT, exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, ensure_ascii=False, indent=indent)
        f.write("\n")


# ---------------------------------------------------------------- 各包构建

def build_legado(srcs, kind):
    """legado 书源数组。剥离本地校验标记，统一开启，显式写死内容类型。"""
    out = []
    for x in srcs:
        if x["format"] != "legado" or x["type"] != kind:
            continue
        o = json.loads(x["rawContent"])
        o = {k: v for k, v in o.items() if not k.startswith("_")}
        o["enabled"] = True
        o["enabledExplore"] = True
        o["bookSourceType"] = 2 if kind == "comic" else 0
        out.append(o)
    return out


def build_moontv(srcs, adult):
    """MoonTV 配置：{"api_site": {key: {name, api, detail}}}，一处导入全部展开。"""
    sites = {}
    for x in srcs:
        if x["format"] != "moontv":
            continue
        if ("🔞" in x["name"]) != adult:
            continue
        o = json.loads(x["rawContent"])
        key = (o.get("key") or x["id"].replace("moontv_", "", 1)).strip()
        if not key or key in sites:
            continue
        sites[key] = {
            "name": o.get("name") or key,
            "api": o["api"],
            "detail": o.get("detail", ""),
        }
    return {"cache_time": 7200, "api_site": sites}


def build_venera(srcs):
    """Venera 源：索引用 fileName 定位，fileName 必须由源 id 推导（key 会重复）。"""
    entries, files = [], {}
    for x in srcs:
        if x["format"] != "venera":
            continue
        code = x["rawContent"]
        key = (x.get("author") or "").strip() or x["id"].replace("venera_", "", 1)
        fname = x["id"].replace("venera_", "", 1) + ".js"
        m = re.search(r'^\s*name\s*=\s*["\'`]([^"\'`]*)["\'`]', code, re.M)
        name = (m.group(1).strip() if m else "") or x["name"] or key
        entries.append({
            "name": name,
            "fileName": fname,
            "key": key,
            "version": (x.get("version") or "").strip(),
        })
        files[fname] = code
    entries.sort(key=lambda e: e["fileName"])
    return entries, files


# ---------------------------------------------------------------- 文档

PKG_META = [
    ("novel.json", "小说", "legado 书源", "novel"),
    ("comic-legado.json", "漫画", "legado 书源", "comic-legado"),
    ("venera/index.json", "漫画", "Venera 源", "venera"),
    ("video.json", "影视", "MoonTV 采集源", "video"),
    ("video-18.json", "影视 · 🔞", "MoonTV 采集源", "video-18"),
]


def md_table(rows):
    out = ["| 文件 | 内容 | 数量 | 一键导入链接 |", "| --- | --- | ---: | --- |"]
    for f, kind, fmt, n, importable, note in rows:
        link = "—" if not importable else f"`{RAW_BASE}/{f}`"
        out.append(f"| `{f}` | {kind} · {fmt}{note} | **{n}** | {link} |")
    return "\n".join(out)


def details(title, items):
    """items: [(名称, 备注)] → Markdown 折叠块"""
    body = "\n".join(
        f"- {t}" + (f" —— <sub>{s}</sub>" if s else "") for t, s in items
    )
    return (
        f"<details>\n<summary><b>{title}</b></summary>\n\n{body}\n\n</details>"
    )


def build_readme(counts, names):
    n_novel = counts["novel.json"]
    n_comic_l = counts["comic-legado.json"]
    n_video = counts["video.json"]
    n_video18 = counts["video-18.json"]
    n_venera = counts["venera/index.json"]
    total = n_novel + n_comic_l + n_video + n_video18 + n_venera

    rows = [
        ("novel.json", "小说", "legado 书源", n_novel, True, ""),
        ("comic-legado.json", "漫画", "legado 书源", n_comic_l, True, ""),
        ("venera/index.json", "漫画", "Venera 源", n_venera, True,
         "（需同目录 `.js`，GitHub 直链可直接导入）"),
        ("video.json", "影视", "MoonTV 采集源", n_video, True, ""),
        ("video-18.json", "影视 · 🔞", "MoonTV 采集源", n_video18, True, ""),
    ]

    head = f"""# 磊毛阅读 聚合源

[磊毛阅读](https://github.com/leimao2333/leimao-reader)（NovelReader）的开箱即用**聚合源**：
共 **{total}** 个源，按小说 / 漫画 / 影视分好包，每条链接都能在 App 里「一次导入一整包」。

在线索引页：**{PAGES_BASE}/**

## 一键导入

把下面任意一条链接粘进 App 的 **源管理 → 右上角 + → 源导入**，点「下载并导入」，
会先列出解析出的全部源让你勾选，确认后逐个入库。

{md_table(rows)}

> 说明：`comic-legado.json` 与 `venera/index.json` 都是漫画源，前者是 legado 规则、后者是 Venera 运行时源，可以同时导入。
> `video.json` / `video-18.json` 是两个独立文件，互不重叠，想用成人源再单独导入 `video-18.json`。

## 包内容

{details(f"小说 · {n_novel} 个（legado）", names["novel.json"])}

{details(f"漫画 · {n_comic_l} 个（legado）", names["comic-legado.json"])}

{details(f"漫画 · {n_venera} 个（Venera）", names["venera/index.json"])}

{details(f"影视 · {n_video} 个（MoonTV）", names["video.json"])}

{details(f"影视 · {n_video18} 个（MoonTV · 🔞）", names["video-18.json"])}

## 关于源 id（重复导入会不会堆垃圾）

- **影视源**：id 由站点域名推导（`moontv_<域名>`），**重复导入原地更新**，不会累积。
- **小说 / 漫画（legado）**：id 由「导入链接 + 条目序号」推导，同一个链接重复导入会原地更新；
  但如果本地已有一份**从别处**导入的同名源，会并存为两条。
- **Venera 源**：id 由 `.js` 文件名推导（`venera_<文件名>`），重复导入原地更新。

## 更新方式

```bash
# 用 App 导出一份新的备份 JSON，然后：
python tools/gen.py /path/to/leimao-backup-YYYYMMDD-HHMMSS.json
# → 重新生成全部包 + manifest.json + README.md + index.html
```

## 说明与免责

- 本仓库只是**源的集合与分发**，不托管任何小说 / 漫画 / 影视内容，所有数据均来自第三方站点。
- 源由脚本从个人使用备份中导出，**未做逐条可用性校验**；第三方站点随时可能改版或失效，
  失效源可自行在 App 内编辑或删除（`源管理 → 一键删除失效源`）。
- `video-18.json` 内含成人内容源，仅供成年人自行决定是否导入。
- 仅供个人学习与自用，请勿用于商业用途；使用前请确认符合你所在地的法律法规。
"""
    return head


def build_index(counts, names):
    counts = dict(counts)
    cards = []
    for f, kind, fmt, n, importable, note in [
        ("novel.json", "小说", "legado 书源", counts["novel.json"], True, ""),
        ("comic-legado.json", "漫画", "legado 书源", counts["comic-legado.json"], True, ""),
        ("venera/index.json", "漫画", "Venera 源", counts["venera/index.json"], True, ""),
        ("video.json", "影视", "MoonTV 采集源", counts["video.json"], True, ""),
        ("video-18.json", "影视 · 🔞", "MoonTV 采集源", counts["video-18.json"], True, ""),
    ]:
        rows = "".join(
            f'<li><span class="nm">{html.escape(t)}</span><span class="ex">{html.escape(s)}</span></li>'
            for t, s in names[f]
        )
        cards.append(f"""  <section class="card">
    <header>
      <div>
        <h2>{html.escape(kind)}<span class="badge">{html.escape(fmt)}</span></h2>
        <p class="file">{f}</p>
      </div>
      <div class="count">{n}<small>个源</small></div>
    </header>
    <div class="url"><code id="u{f}">{RAW_BASE}/{f}</code>
      <button onclick="cp('u{f}', this)">复制</button></div>
    <details><summary>展开源列表（{n}）</summary><ul>{rows}</ul></details>
  </section>""")

    total = sum(counts.values())
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>磊毛阅读 · 聚合源</title>
<style>
  :root {{ color-scheme: light; }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; padding: 28px 18px 64px; background: #f6f7f9; color: #1f2328;
         font: 15px/1.6 -apple-system, "Segoe UI", "Microsoft YaHei", sans-serif; }}
  .wrap {{ max-width: 820px; margin: 0 auto; }}
  h1 {{ margin: 0 0 6px; font-size: 26px; }}
  .sub {{ margin: 0 0 26px; color: #59636e; }}
  .total {{ font-weight: 600; color: #1f2328; }}
  .card {{ background: #fff; border: 1px solid #d8dee4; border-radius: 10px;
           padding: 16px 18px; margin-bottom: 14px; }}
  .card header {{ display: flex; align-items: flex-start; justify-content: space-between; gap: 12px; }}
  h2 {{ margin: 0; font-size: 17px; }}
  .badge {{ margin-left: 8px; padding: 1px 8px; border-radius: 999px; background: #eef1f4;
            color: #59636e; font-size: 12px; font-weight: 500; vertical-align: 2px; }}
  .file {{ margin: 3px 0 0; color: #6e7781; font-size: 12.5px; font-family: ui-monospace, Consolas, monospace; }}
  .count {{ font-size: 22px; font-weight: 700; color: #d1242f; white-space: nowrap; }}
  .count small {{ margin-left: 3px; font-size: 12px; font-weight: 400; color: #6e7781; }}
  .url {{ display: flex; gap: 8px; margin-top: 12px; }}
  .url code {{ flex: 1; min-width: 0; overflow-x: auto; white-space: nowrap; padding: 7px 10px;
               background: #f6f8fa; border: 1px solid #d8dee4; border-radius: 6px;
               font: 12.5px/1.5 ui-monospace, Consolas, monospace; }}
  button {{ padding: 7px 14px; border: 1px solid #d0d7de; border-radius: 6px; background: #f6f8fa;
            cursor: pointer; font-size: 13px; color: #1f2328; }}
  button:hover {{ background: #eef1f4; }}
  details {{ margin-top: 12px; }}
  summary {{ cursor: pointer; color: #0969da; font-size: 13.5px; }}
  ul {{ margin: 10px 0 0; padding: 0; list-style: none; columns: 2; column-gap: 22px; }}
  li {{ padding: 3px 0; font-size: 13px; break-inside: avoid; }}
  .nm {{ margin-right: 6px; }}
  .ex {{ color: #6e7781; font-size: 12px; }}
  footer {{ margin-top: 26px; color: #6e7781; font-size: 12.5px; }}
  footer p {{ margin: 5px 0; }}
  @media (max-width: 620px) {{ ul {{ columns: 1; }} }}
</style>
</head>
<body>
<div class="wrap">
  <h1>磊毛阅读 · 聚合源</h1>
  <p class="sub">共 <span class="total">{total}</span> 个源，按小说 / 漫画 / 影视分好包，粘进 App 一次导入一整包。</p>
{chr(10).join(cards)}
  <footer>
    <p>导入方式：App → 源管理 → 右上角 + → 粘贴上面任意一条链接 → 下载并导入 → 勾选要添加的源。</p>
    <p>本页仅分发源的集合，不托管任何内容；第三方站点随时可能失效，失效源可在 App 内删除。</p>
  </footer>
</div>
<script>
function cp(id, btn) {{
  var t = document.getElementById(id).textContent, o = btn.textContent;
  (navigator.clipboard ? navigator.clipboard.writeText(t) : Promise.reject())
    .then(function () {{ btn.textContent = '已复制'; }})
    .catch(function () {{
      var r = document.createRange(); r.selectNodeContents(document.getElementById(id));
      var s = getSelection(); s.removeAllRanges(); s.addRange(r);
      document.execCommand('copy'); s.removeAllRanges(); btn.textContent = '已复制';
    }})
    .then(function () {{ setTimeout(function () {{ btn.textContent = o; }}, 1500); }});
}}
</script>
</body>
</html>
"""


def main():
    if len(sys.argv) < 2:
        raise SystemExit("用法：python tools/gen.py <lexxx-backup-xxx.json>")
    srcs = load_backup(sys.argv[1])["sources"]

    legado_novel = build_legado(srcs, "novel")
    legado_comic = build_legado(srcs, "comic")
    moontv_normal = build_moontv(srcs, False)
    moontv_adult = build_moontv(srcs, True)
    venera_entries, venera_files = build_venera(srcs)

    dump(legado_novel, "novel.json")
    dump(legado_comic, "comic-legado.json")
    dump(moontv_normal, "video.json")
    dump(moontv_adult, "video-18.json")
    dump(venera_entries, "venera/index.json")
    for fname, code in venera_files.items():
        p = os.path.join(OUT, "venera", fname)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write(code if code.endswith("\n") else code + "\n")

    counts = {
        "novel.json": len(legado_novel),
        "comic-legado.json": len(legado_comic),
        "venera/index.json": len(venera_entries),
        "video.json": len(moontv_normal["api_site"]),
        "video-18.json": len(moontv_adult["api_site"]),
    }

    def ml(items):
        return [(t, s) for t, s in items]

    names = {
        "novel.json": ml([(o["bookSourceName"], o.get("bookSourceGroup") or o["bookSourceUrl"])
                          for o in legado_novel]),
        "comic-legado.json": ml([(o["bookSourceName"], o.get("bookSourceGroup") or o["bookSourceUrl"])
                                 for o in legado_comic]),
        "venera/index.json": ml([(e["name"], e["fileName"]) for e in venera_entries]),
        "video.json": ml([(v["name"], v["api"].split("/")[2]) for v in moontv_normal["api_site"].values()]),
        "video-18.json": ml([(v["name"], v["api"].split("/")[2]) for v in moontv_adult["api_site"].values()]),
    }

    dump({
        "name": "磊毛阅读 聚合源",
        "app": "leimao-reader",
        "formatVersion": 1,
        "generatedFrom": os.path.basename(sys.argv[1]),
        "rawBase": RAW_BASE,
        "packages": [
            {"file": f, "kind": k, "format": fm, "count": counts[f],
             "files": len(venera_files) + 1 if f == "venera/index.json" else 1,
             **({"adult": True} if f == "video-18.json" else {})}
            for f, k, fm, _ in [
                ("novel.json", "小说", "legado", None),
                ("comic-legado.json", "漫画", "legado", None),
                ("venera/index.json", "漫画", "venera", None),
                ("video.json", "影视", "moontv", None),
                ("video-18.json", "影视", "moontv", None),
            ]
        ],
    }, "manifest.json")

    with open(os.path.join(OUT, "README.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write(build_readme(counts, names))
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(build_index(counts, names))

    print("源清单：")
    for k, v in counts.items():
        print(f"  {k:22s} {v}")
    print(f"  合计 {sum(counts.values())}")


if __name__ == "__main__":
    main()
