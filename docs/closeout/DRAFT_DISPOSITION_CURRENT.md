# Draft 逐条处置账（当前 HEAD 自动重算）

HEAD：`abbbf876ec4eed0bb9ac1030254aba01878de7a5`
draft 总数：**13963**

本文件由 `tools/build-draft-disposition.py` 生成，可随时重跑；每一条 draft 都有独立行记录源 ID、证据路径与分类依据。
**分类不等于结案**：`catalog_metadata` 依 schema 保留 draft 属正常去向，`verifiable_text`、`figure_or_lacuna`、`edition_variant`、`illegible` 仍是真实待办。

## 分类计数

| 分类 | 条数 | 含义 |
| --- | ---: | --- |
| `verifiable_text` | 7107 | 可核实正文：电子原文完整可读，尚待完整语义对读 |
| `catalog_metadata` | 4544 | 目录/元数据：章题、卷端题署、版记或现代恢复说明，按 schema 保留 draft 状态 |
| `figure_or_lacuna` | 2018 | 图文缺失：含缺字、图像占位或残表标记 |
| `edition_variant` | 293 | 版本异文：note 记录异文或版本差异问题 |
| `illegible` | 1 | 原件仍不可辨：残句无正向可读证据 |

## 按书分布（draft 条数）

| 书 | draft |
| --- | ---: |
| huangji-jingshi | 3103 |
| wuxing-jingji | 1350 |
| qimen-dunjia-tongzhi | 1289 |
| yuanhai-ziping | 1266 |
| zengshan-buyi | 1158 |
| yuqia-ji | 873 |
| minghai-quanbian | 804 |
| daliuren-daquan | 767 |
| bushi-zhengzong | 447 |
| ziwei-doushu-quanshu | 440 |
| xingli-kaoyuan | 429 |
| taiyi-shenshu | 407 |
| xuexin-fu | 289 |
| zhouyi-zhezhong | 238 |
| mayi-shenxiang | 215 |
| mingli-yueyan | 162 |
| shenxiang-quanbian | 152 |
| liuren-miben | 118 |
| shenshi-xuankong-xue | 104 |
| xingming-suyuan | 102 |
| hanlong-jing | 78 |
| sanming-tonghui | 62 |
| li-xuzhong-mingshu | 42 |
| zangshu | 30 |
| tianyu-jing | 21 |
| qingnang-xu | 8 |
| dili-bianzheng | 4 |
| yuzhao-shenying | 2 |
| xingxue-dacheng | 2 |
| luoluzi-sanming | 1 |

逐条明细见 `DRAFT_DISPOSITION_LEDGER.json`。
