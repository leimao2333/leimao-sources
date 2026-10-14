# 磊毛阅读 聚合源

[磊毛阅读](https://github.com/leimao2333/leimao-reader)（NovelReader）的开箱即用**聚合源**：
共 **169** 个源（小说 69 / 漫画 36 / 影视 64）。

在线索引页（带一键复制）：**https://leimao2333.github.io/leimao-sources/**

## 一键导入

把链接粘进 App 的 **源管理 → 右上角 + → 源导入**，点「下载并导入」，
会先列出解析出的全部源让你勾选，确认后逐个入库。

### 整合版 · 3 条链接覆盖全部 169 个源

| 文件 | 内容 | 数量 | 一键导入链接 |
| --- | --- | ---: | --- |
| `legado-all.json` | 小说 + 漫画 · legado 书源 | **80** | `https://raw.githubusercontent.com/leimao2333/leimao-sources/main/legado-all.json` |
| `video-all.json` | 影视 · 含 🔞 · MoonTV 采集源 | **64** | `https://raw.githubusercontent.com/leimao2333/leimao-sources/main/video-all.json` |
| `venera/index.json` | 漫画 · Venera 源 | **25** | `https://raw.githubusercontent.com/leimao2333/leimao-sources/main/venera/index.json` |

**为什么不是 1 条？** App 的导入是「下载 → 按内容识别格式 → 导入」，**一次只认一种格式**：
legado 书源数组 / MoonTV 采集配置 / Venera 源索引，三种结构互不兼容，塞不进同一个文件。
其中 legado 的小说与漫画能合并（靠 `bookSourceType` 区分内容类型）、影视两个包也是同格式能合并，
但 **Venera 是独立 JS 运行时源，格式无法与其它两种共存** —— 所以 3 条是当前 App 的下限。

### 细分版 · 按类型 / 是否成人拆开

| 文件 | 内容 | 数量 | 一键导入链接 |
| --- | --- | ---: | --- |
| `novel.json` | 小说 · legado 书源 | **69** | `https://raw.githubusercontent.com/leimao2333/leimao-sources/main/novel.json` |
| `comic-legado.json` | 漫画 · legado 书源 | **11** | `https://raw.githubusercontent.com/leimao2333/leimao-sources/main/comic-legado.json` |
| `venera/index.json` | 漫画 · Venera 源 | **25** | `https://raw.githubusercontent.com/leimao2333/leimao-sources/main/venera/index.json` |
| `video.json` | 影视 · MoonTV 采集源 | **36** | `https://raw.githubusercontent.com/leimao2333/leimao-sources/main/video.json` |
| `video-18.json` | 影视 · 🔞 · MoonTV 采集源 | **28** | `https://raw.githubusercontent.com/leimao2333/leimao-sources/main/video-18.json` |

> `venera/index.json` 需要同目录下的 25 个 `.js`，GitHub 直链可直接导入，不用手动下载。
> `video.json` 是干净的 36 个普通源；`video-18.json` 与整合版 `video-all.json` 含成人源，自行决定是否导入。

## 包内容

<details>
<summary><b>小说 · 69 个（legado 书源）</b></summary>

- 中文书城 —— <sub>备用</sub>
- 笔趣阁 —— <sub>备用</sub>
- 梧桐中文 —— <sub>标准</sub>
- 黑岩小说 —— <sub>备用</sub>
- 若初文学 —— <sub>备用</sub>
- 第一版主 —— <sub>备用</sub>
- 企鹅阅读 —— <sub>精选</sub>
- Xnxx —— <sub>备用</sub>
- 画本阅读 —— <sub>标准</sub>
- 红叶书斋 —— <sub>备用</sub>
- 心轻小说 —— <sub>标准</sub>
- 米读小说 —— <sub>标准</sub>
- 殓师灵异 —— <sub>标准</sub>
- 躺着看小说 —— <sub>备用</sub>
- 企鹅阅读 —— <sub>精选</sub>
- 晋江文学 —— <sub>备用</sub>
- 爱发电网 —— <sub>精选</sub>
- 去读书啊 —— <sub>备用</sub>
- 顶点小说 —— <sub>备用</sub>
- 爱久久网 —— <sub>备用</sub>
- 飞卢小说 —— <sub>备用</sub>
- 海马读书 —— <sub>备用</sub>
- 书包小说网 —— <sub>备用</sub>
- 猫九小说 —— <sub>备用</sub>
- 笔趣阁 —— <sub>备用</sub>
- 笔趣阁 —— <sub>备用</sub>
- 搜书网 —— <sub>备用</sub>
- 米读看书 —— <sub>标准</sub>
- 神话之后 —— <sub>备用</sub>
- 大唐小说 —— <sub>备用</sub>
- 古龙武侠 —— <sub>精选</sub>
- 废纸文学 —— <sub>备用</sub>
- 肉书屋 —— <sub>标准</sub>
- 何以生肖 —— <sub>标准</sub>
- 话本小说 —— <sub>标准</sub>
- 安轻小说 —— <sub>标准</sub>
- 中意文学 —— <sub>标准</sub>
- 笔趣阁 —— <sub>备用</sub>
- 52PO小说 —— <sub>备用</sub>
- 第一版主 —— <sub>备用</sub>
- 轻菠萝包 —— <sub>标准</sub>
- 海棠书屋 —— <sub>备用</sub>
- 中文万维 —— <sub>标准</sub>
- 晋江文学 —— <sub>精选</sub>
- 废文网 —— <sub>备用</sub>
- 繁星四月 —— <sub>备用</sub>
- 笔趣阁 —— <sub>备用</sub>
- 霸王街机 —— <sub>备用</sub>
- 红薯阅读 —— <sub>备用</sub>
- 企鹅阅读 —— <sub>精选</sub>
- 安稳小说 —— <sub>备用</sub>
- 贝壳读书 —— <sub>备用</sub>
- 米读小说 —— <sub>标准</sub>
- 365book —— <sub>备用</sub>
- 飞卢小说 —— <sub>标准</sub>
- 海词精选 —— <sub>精选</sub>
- 栀子欢网 —— <sub>备用</sub>
- 猫眼看书 —— <sub>备用</sub>
- 爱下电子 —— <sub>精选</sub>
- 星星小说 —— <sub>备用</sub>
- 飞卢小说 —— <sub>标准</sub>
- 天地中文 —— <sub>备用</sub>
- 爱下电子书 —— <sub>备用</sub>
- 晋江详榜 —— <sub>备用</sub>
- 商店小说 —— <sub>备用</sub>
- 奇异网 —— <sub>备用</sub>
- 笔迷读 —— <sub>标准</sub>
- 阅友小说 —— <sub>http://m.suixkan.com</sub>
- 独步小说网 —— <sub>搜索暂不可用</sub>

</details>

<details>
<summary><b>漫画 · 11 个（legado 书源）</b></summary>

- 酸奶漫画 —— <sub>漫画 书源</sub>
- 酝酿漫画（魔法） —— <sub>漫画 书源</sub>
- 点外漫画（英文） —— <sub>漫画 书源</sub>
- 酸奶漫画 —— <sub>漫画 书源</sub>
- 包子漫画（魔法） —— <sub>漫画 书源</sub>
- 漫画小屋（优） —— <sub>漫画 书源</sub>
- 铅笔漫画（优） —— <sub>漫画 书源</sub>
- 漫画小屋（优） —— <sub>漫画 书源</sub>
- 蛮歌漫画（优） —— <sub>漫画 书源</sub>
- 星际漫画（优） —— <sub>漫画 书源</sub>
- 追更漫画（优+） —— <sub>漫画 书源</sub>

</details>

<details>
<summary><b>漫画 · 25 个（Venera 源）</b></summary>

- 包子漫画 —— <sub>baozi.js</sub>
- CCC追漫台 —— <sub>ccc.js</sub>
- 拷贝漫画 —— <sub>copy_manga.js</sub>
- 拷贝漫画M —— <sub>copy_manga_multi_accounts.js</sub>
- ehentai —— <sub>ehentai.js</sub>
- GoDa漫画 —— <sub>goda.js</sub>
- 嗨皮漫画 —— <sub>happy.js</sub>
- H-Comic —— <sub>hcomic.js</sub>
- hitomi.la —— <sub>hitomi.js</sub>
- 热辣漫画 —— <sub>hot_manga.js</sub>
- 爱看漫 —— <sub>ikmmh.js</sub>
- jcomic.net —— <sub>jcomic.js</sub>
- 禁漫天堂 —— <sub>jm.js</sub>
- Kavita —— <sub>kavita.js</sub>
- Komiic —— <sub>komiic.js</sub>
- MangaDex —— <sub>manga_dex.js</sub>
- 漫画人 —— <sub>manhuaren.js</sub>
- 漫画1234 —— <sub>mh1234.js</sub>
- 18漫画 —— <sub>mh18.js</sub>
- 漫小肆 —— <sub>mxs.js</sub>
- MYCOMIC —— <sub>mycomic.js</sub>
- nhentai —— <sub>nhentai.js</sub>
- Picacg —— <sub>picacg.js</sub>
- 少年ジャンプ＋ —— <sub>shonen_jump_plus.js</sub>
- 紳士漫畫 —— <sub>wnacg.js</sub>

</details>

<details>
<summary><b>影视 · 36 个（MoonTV 采集源）</b></summary>

- 🎬艾旦影视 —— <sub>pz.v88.qzz.io</sub>
- 🎬百度云zy —— <sub>pz.v88.qzz.io</sub>
- 🎬豪华资源 —— <sub>hhzyapi.com</sub>
- 🎬如意资源 —— <sub>cj.rycjapi.com</sub>
- 🎬魔都动漫 —— <sub>caiji.moduapi.cc</sub>
- 🎬红牛资源 —— <sub>www.hongniuzy2.com</sub>
- 🎬光速资源 —— <sub>api.guangsuapi.com</sub>
- 🎬U酷影视 —— <sub>api.ukuapi88.com</sub>
- 🎬飘零资源 —— <sub>p2100.net</sub>
- 🎬金鹰点播 —— <sub>jyzyapi.com</sub>
- 🎬速播资源 —— <sub>subocaiji.com</sub>
- 🎬新浪资源 —— <sub>api.xinlangapi.com</sub>
- 🎬无尽资源 —— <sub>api.wujinapi.me</sub>
- 🎬最大资源 —— <sub>api.zuidapi.com</sub>
- 🎬暴风资源 —— <sub>bfzyapi.com</sub>
- 🎬非凡资源 —— <sub>api.ffzyapi.com</sub>
- 🎬魔都资源 —— <sub>www.mdzyapi.com</sub>
- 🎬极速资源 —— <sub>jszyapi.com</sub>
- 🎬360 资源 —— <sub>360zyzz.com</sub>
- 🎬量子资源 —— <sub>cj.lzcaiji.com</sub>
- 🎬猫眼资源 —— <sub>api.maoyanapi.top</sub>
- 🎬电影天堂 —— <sub>caiji.dyttzyapi.com</sub>
- 🎬iKun资源 —— <sub>ikunzyapi.com</sub>
- 🎬茅台资源 —— <sub>caiji.maotaizy.cc</sub>
- 🎬豆瓣资源 —— <sub>caiji.dbzy5.com</sub>
- 🎬-爱奇艺- —— <sub>iqiyizyapi.com</sub>
- 🎬樱花资源 —— <sub>m3u8.apiyhzy.com</sub>
- 🎬闪电资源 —— <sub>xsd.sdzyapi.com</sub>
- 🎬快车资源 —— <sub>caiji.kuaichezy.org</sub>
- 🎬索尼资源 —— <sub>suoniapi.com</sub>
- 🎬鸭鸭资源 —— <sub>cj.yayazy.net</sub>
- 🎬虎牙资源 —— <sub>www.huyaapi.com</sub>
- 🎬优质资源 —— <sub>api.yzzy-api.com</sub>
- 🎬无尽影视 —— <sub>api.wujinapi.com</sub>
- 🎬最大点播 —— <sub>zuidazy.me</sub>
- 🎬量子影视 —— <sub>cj.lziapi.com</sub>

</details>

<details>
<summary><b>影视 · 🔞 · 28 个（MoonTV 采集源）</b></summary>

- 🔞souavZY —— <sub>api.souavzyw.net</sub>
- 🔞精品资源 —— <sub>www.jingpinx.com</sub>
- 🔞桃花资源 —— <sub>thzy1.me</sub>
- 🔞黑料资源 —— <sub>www.heiliaozyapi.com</sub>
- 🔞滴滴资源 —— <sub>api.ddapi.cc</sub>
- 🔞鲨鱼资源 —— <sub>shayuapi.com</sub>
- 🔞辣椒资源 —— <sub>apilj.com</sub>
- 🔞森林资源 —— <sub>beiyong.slapibf.com</sub>
- 🔞奶香资源 —— <sub>Naixxzy.com</sub>
- 🔞乐播资源 —— <sub>lbapi9.com</sub>
- 🔞jkun资源 —— <sub>jkunzyapi.com</sub>
- 🔞-大奶子- —— <sub>apidanaizi.com</sub>
- 🔞黄色仓库 —— <sub>hsckzy.xyz</sub>
- 🔞小鸡资源 —— <sub>api.xiaojizy.live</sub>
- 🔞-老色逼- —— <sub>apilsbzy1.com</sub>
- 🔞番号资源 —— <sub>fhapi9.com</sub>
- 🔞玉兔资源 —— <sub>apiyutu.com</sub>
- 🔞155-资源 —— <sub>155api.com</sub>
- 🔞麻豆视频 —— <sub>91md.me</sub>
- 🔞-奥斯卡- —— <sub>aosikazy.com</sub>
- 🔞色猫资源 —— <sub>caiji.semaozy.net</sub>
- 🔞大地资源 —— <sub>dadiapi.com</sub>
- 🔞杏吧资源 —— <sub>xingba222.com</sub>
- 🔞白嫖资源 —— <sub>www.kxgav.com</sub>
- 🔞-黄AVZY —— <sub>www.pgxdy.com</sub>
- 🔞-美少女- —— <sub>www.msnii.com</sub>
- 🔞 CK-资源 —— <sub>ckzy.me</sub>
- 🔞豆豆资源 —— <sub>api.douapi.cc</sub>

</details>

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
