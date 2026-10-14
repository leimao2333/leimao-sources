# -*- coding: utf-8 -*-
"""
磊毛阅读 聚合源 · 生成脚本

用法：
    python tools/gen.py <leimao-backup-YYYYMMDD-HHMMSS.json>

从「磊毛阅读」的云备份 JSON 里抽出全部源，生成可直接一键导入的聚合包：

    整合版（3 条链接覆盖全部源）
        legado-all.json      小说 + 漫画（legado 书源，80）
        video-all.json       影视 · 含成人（MoonTV 配置，64）
        venera/index.json    漫画（Venera 源索引，25，同目录 .js 为源码）

    细分版（按类型 / 是否成人拆开）
        novel.json           小说（69）
        comic-legado.json    漫画 · legado（11）
        video.json           影视（36）
        video-18.json        影视 · 成人（28）

    辅助
        manifest.json        包清单（供工具读取）
        README.md / index.html  自动生成的说明与索引页

为什么不能只给「1 条链接」：App 的导入是「下载 → 按内容识别格式 → 导入」，
一次只认一种格式（legado 数组 / MoonTV 配置 / Venera 索引），三种格式无法共存于一个文件。
legado 的小说与漫画可以合并（靠 bookSourceType 区分类型），影视两个包也是同格式可合并，
但 Venera 是独立 JS 运行时、只能单独一条 —— 所以 3 条是当前 App 的下限。

备份文件结构：{"app":"leimao-reader","sources":[{"type","format","name","rawContent",...}]}
"""
import html
import json
import os
import re
import sys

RAW_BASE = "https://raw.githubusercontent.com/leimao2333/leimao-sources/main"
PAGES_BASE = "https://leimao2333.github.io/leimao-sources"
REPO = "https://github.com/leimao2333/leimao-sources"
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

def build_legado(srcs, kinds):
    """legado 书源数组。剥离本地校验标记，统一开启，显式写死内容类型（0 小说 / 2 漫画）。"""
    out = []
    for x in srcs:
        if x["format"] != "legado" or x["type"] not in kinds:
            continue
        o = json.loads(x["rawContent"])
        o = {k: v for k, v in o.items() if not k.startswith("_")}
        o["enabled"] = True
        o["enabledExplore"] = True
        o["bookSourceType"] = 2 if x["type"] == "comic" else 0
        out.append(o)
    return out


def build_moontv(srcs, adult):
    """MoonTV 配置：{"api_site": {key: {name, api, detail}}}，一处导入全部展开。

    adult=True 只取成人源，False 只取普通源，None 全都要。
    """
    sites = {}
    for x in srcs:
        if x["format"] != "moontv":
            continue
        if adult is not None and ("🔞" in x["name"]) != adult:
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

def md_table(pkgs):
    out = ["| 文件 | 内容 | 数量 | 一键导入链接 |", "| --- | --- | ---: | --- |"]
    for p in pkgs:
        out.append(
            f"| `{p['file']}` | {p['title']} · {p['fmt']} | **{p['count']}** | "
            f"`{RAW_BASE}/{p['file']}` |"
        )
    return "\n".join(out)


def details(title, items):
    """items: [(名称, 备注)] → Markdown 折叠块"""
    body = "\n".join(f"- {t}" + (f" —— <sub>{s}</sub>" if s else "") for t, s in items)
    return f"<details>\n<summary><b>{title}</b></summary>\n\n{body}\n\n</details>"


def build_readme(pkgs, total):
    merged = [p for p in pkgs if p["group"] == "整合"]
    split = [p for p in pkgs if p["group"] == "细分"]
    by = {p["file"]: p for p in pkgs}

    content = "\n\n".join(
        details(f"{p['title']} · {p['count']} 个（{p['fmt']}）", p["names"])
        # 整合包的内容 = 下面细分包的并集（legado-all = novel + comic-legado，
        # video-all = video + video-18），不再重复罗列
        for p in [by[f] for f in ("novel.json", "comic-legado.json", "venera/index.json",
                                  "video.json", "video-18.json")]
    )

    return f"""# 磊毛阅读 聚合源

[磊毛阅读](https://github.com/leimao2333/leimao-reader)（NovelReader）的开箱即用**聚合源**：
共 **{total}** 个源（小说 {by['novel.json']['count']} / 漫画 {by['comic-legado.json']['count'] + by['venera/index.json']['count']} / 影视 {by['video.json']['count'] + by['video-18.json']['count']}）。

在线索引页（带一键复制）：**{PAGES_BASE}/**

## 一键导入

把链接粘进 App 的 **源管理 → 右上角 + → 源导入**，点「下载并导入」，
会先列出解析出的全部源让你勾选，确认后逐个入库。

### 整合版 · 3 条链接覆盖全部 {total} 个源

{md_table(merged)}

**为什么不是 1 条？** App 的导入是「下载 → 按内容识别格式 → 导入」，**一次只认一种格式**：
legado 书源数组 / MoonTV 采集配置 / Venera 源索引，三种结构互不兼容，塞不进同一个文件。
其中 legado 的小说与漫画能合并（靠 `bookSourceType` 区分内容类型）、影视两个包也是同格式能合并，
但 **Venera 是独立 JS 运行时源，格式无法与其它两种共存** —— 所以 3 条是当前 App 的下限。

### 细分版 · 按类型 / 是否成人拆开

{md_table(split)}

> `venera/index.json` 需要同目录下的 25 个 `.js`，GitHub 直链可直接导入，不用手动下载。
> `video.json` 是干净的 36 个普通源；`video-18.json` 与整合版 `video-all.json` 含成人源，自行决定是否导入。

## 包内容

{content}

## 关于源 id（重复导入会不会堆垃圾）

- **影视源**：id 由站点域名推导（`moontv_<域名>`），**重复导入原地更新**，不会累积。
- **小说 / 漫画（legado）**：id 由「导入链接 + 条目序号」推导，同一个链接重复导入会原地更新；
  但如果本地已有一份**从别处**导入的同名源，会并存为两条。
- **Venera 源**：id 由 `.js` 文件名推导（`venera_<文件名>`），重复导入原地更新。
- 整合版与细分版是**不同文件、不同链接** → id 前缀不同，两份都导入会各存一份。选一种就好。

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
- 含 🔞 标记的包为成人内容源，仅供成年人自行决定是否导入。
- 仅供个人学习与自用，请勿用于商业用途；使用前请确认符合你所在地的法律法规。
"""


def build_index(pkgs, total):
    def cards(items, highlight=False):
        out = []
        for p in items:
            rows = "".join(
                f'<li><span class="nm">{html.escape(t)}</span><span class="ex">{html.escape(s)}</span></li>'
                for t, s in p["names"]
            )
            sid = p["file"].replace("/", "-").replace(".", "-")
            out.append(f"""  <section class="card{(' hi' if highlight else '')}">
    <header>
      <div>
        <h2>{html.escape(p['title'])}<span class="badge">{html.escape(p['fmt'])}</span></h2>
        <p class="file">{p['file']}</p>
      </div>
      <div class="count">{p['count']}<small>个源</small></div>
    </header>
    <div class="url"><code id="u{sid}">{RAW_BASE}/{p['file']}</code>
      <button onclick="cp('u{sid}', this)">复制</button></div>
    <details><summary>展开源列表（{p['count']}）</summary><ul>{rows}</ul></details>
  </section>""")
        return "\n".join(out)

    merged = [p for p in pkgs if p["group"] == "整合"]
    split = [p for p in pkgs if p["group"] == "细分"]

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
  .sub {{ margin: 0 0 24px; color: #59636e; }}
  .total {{ font-weight: 600; color: #1f2328; }}
  h2.sec {{ margin: 30px 0 12px; font-size: 15px; color: #59636e; font-weight: 600; }}
  h2.sec span {{ font-weight: 400; }}
  .card {{ background: #fff; border: 1px solid #d8dee4; border-radius: 10px;
           padding: 16px 18px; margin-bottom: 14px; }}
  .card.hi {{ border-color: #9dc0ee; box-shadow: 0 0 0 3px #eaf2fd; }}
  .card header {{ display: flex; align-items: flex-start; justify-content: space-between; gap: 12px; }}
  .card h2 {{ margin: 0; font-size: 17px; }}
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
  .note {{ background: #fff8e5; border: 1px solid #f0d9a0; border-radius: 8px;
           padding: 12px 14px; margin: 14px 0 4px; font-size: 13px; color: #4d3c12; }}
  .note b {{ color: #1f2328; }}
  footer {{ margin-top: 30px; color: #6e7781; font-size: 12.5px; }}
  footer p {{ margin: 5px 0; }}
  @media (max-width: 620px) {{ ul {{ columns: 1; }} }}
</style>
</head>
<body>
<div class="wrap">
  <h1>磊毛阅读 · 聚合源</h1>
  <p class="sub">共 <span class="total">{total}</span> 个源。整合版 <b>3 条链接</b>即可全部导入，也可按类型挑细分包。</p>

  <h2 class="sec">整合版 <span>· 3 条链接覆盖全部 {total} 个源</span></h2>
{cards(merged, highlight=True)}
  <div class="note">
    <b>为什么不是 1 条链接？</b> App 的导入是「下载 → 按内容识别格式 → 导入」，一次只认一种格式
    （legado 书源数组 / MoonTV 采集配置 / Venera 源索引），三种结构互不兼容，塞不进同一个文件。
    legado 的小说与漫画能合并、影视两个包也是同格式能合并，但 Venera 是独立 JS 运行时源，
    无法与其它两种共存 —— 所以 3 条是当前 App 的下限。
  </div>

  <h2 class="sec">细分版 <span>· 按类型 / 是否成人拆开</span></h2>
{cards(split)}

  <footer>
    <p>导入方式：App → 源管理 → 右上角 + → 粘贴上面任意一条链接 → 下载并导入 → 勾选要添加的源。</p>
    <p>整合版与细分版是不同文件、不同链接，两份都导入会各存一份，选一种就好。</p>
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
        raise SystemExit("用法：python tools/gen.py <leimao-backup-xxx.json>")
    backup = sys.argv[1]
    srcs = load_backup(backup)["sources"]

    legado_novel = build_legado(srcs, ("novel",))
    legado_comic = build_legado(srcs, ("comic",))
    legado_all = build_legado(srcs, ("novel", "comic"))
    moontv_normal = build_moontv(srcs, False)
    moontv_adult = build_moontv(srcs, True)
    moontv_all = build_moontv(srcs, None)
    venera_entries, venera_files = build_venera(srcs)

    dump(legado_all, "legado-all.json")
    dump(legado_novel, "novel.json")
    dump(legado_comic, "comic-legado.json")
    dump(moontv_all, "video-all.json")
    dump(moontv_normal, "video.json")
    dump(moontv_adult, "video-18.json")
    dump(venera_entries, "venera/index.json")
    for fname, code in venera_files.items():
        p = os.path.join(OUT, "venera", fname)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write(code if code.endswith("\n") else code + "\n")

    def legado_names(items):
        return [(o["bookSourceName"], o.get("bookSourceGroup") or o["bookSourceUrl"]) for o in items]

    def site_names(cfg):
        return [(v["name"], v["api"].split("/")[2]) for v in cfg["api_site"].values()]

    venera_names = [(e["name"], e["fileName"]) for e in venera_entries]

    pkgs = [
        # ---- 整合版：3 条 ----
        {"file": "legado-all.json", "title": "小说 + 漫画", "fmt": "legado 书源",
         "count": len(legado_all), "names": legado_names(legado_all), "group": "整合"},
        {"file": "video-all.json", "title": "影视 · 含 🔞", "fmt": "MoonTV 采集源",
         "count": len(moontv_all["api_site"]), "names": site_names(moontv_all), "group": "整合"},
        {"file": "venera/index.json", "title": "漫画", "fmt": "Venera 源",
         "count": len(venera_entries), "names": venera_names, "group": "整合"},
        # ---- 细分版 ----
        {"file": "novel.json", "title": "小说", "fmt": "legado 书源",
         "count": len(legado_novel), "names": legado_names(legado_novel), "group": "细分"},
        {"file": "comic-legado.json", "title": "漫画", "fmt": "legado 书源",
         "count": len(legado_comic), "names": legado_names(legado_comic), "group": "细分"},
        {"file": "venera/index.json", "title": "漫画", "fmt": "Venera 源",
         "count": len(venera_entries), "names": venera_names, "group": "细分"},
        {"file": "video.json", "title": "影视", "fmt": "MoonTV 采集源",
         "count": len(moontv_normal["api_site"]), "names": site_names(moontv_normal), "group": "细分"},
        {"file": "video-18.json", "title": "影视 · 🔞", "fmt": "MoonTV 采集源",
         "count": len(moontv_adult["api_site"]), "names": site_names(moontv_adult), "group": "细分"},
    ]

    total = len(legado_all) + len(moontv_all["api_site"]) + len(venera_entries)

    dump({
        "name": "磊毛阅读 聚合源",
        "app": "leimao-reader",
        "formatVersion": 1,
        "generatedFrom": os.path.basename(backup),
        "rawBase": RAW_BASE,
        "total": total,
        "packages": [
            {"file": p["file"], "title": p["title"], "format": p["fmt"],
             "count": p["count"], "group": p["group"],
             "files": len(venera_files) + 1 if p["file"] == "venera/index.json" else 1}
            for p in pkgs
        ],
    }, "manifest.json")

    with open(os.path.join(OUT, "README.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write(build_readme(pkgs, total))
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(build_index(pkgs, total))

    print("整合版（3 条覆盖全部）：")
    for p in pkgs:
        if p["group"] == "整合":
            print(f"  {p['file']:22s} {p['count']:4d}  {p['title']}")
    print("细分版：")
    for p in pkgs:
        if p["group"] == "细分":
            print(f"  {p['file']:22s} {p['count']:4d}  {p['title']}")
    print(f"合计 {total}")


if __name__ == "__main__":
    main()
