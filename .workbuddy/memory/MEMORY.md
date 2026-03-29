# Long-term Memory

## 用户环境

- **Python 安装路径**: `D:\Anaconda`（Anaconda 发行版，装在 D 盘）
  - 运行 Python 时应使用 `D:\Anaconda\python.exe` 或先将其加入 PATH
  - `python` / `python3` 命令在 PowerShell 中默认不可用，需指定完整路径或使用 Anaconda Prompt
- **服务器启动权限**: 用户已授权，可以直接启动 HTTP 服务器

## 项目信息

- **daywise.html** 位于 `C:\Users\49592\WorkBuddy\20260320231952\daywise.html`
  - 单文件日记/打卡应用，使用 localStorage 存储数据
  - 必须通过本地服务器访问（`D:\Anaconda\python.exe -m http.server 8080`）
  - 直接用 file:// 打开会导致 localStorage 不稳定，数据无法持久保存
  - 访问地址：http://localhost:8080/daywise.html

## 关键词提取算法

- 使用滑动窗口提取2-4字的中文词语（不是短语或句子）
- 排除停用词（200+个常见无意义词）、纯数字、过长的英文词
- 排除包含"的""了""和""是"等连接词的词组
- 分类展示：情绪💭、工作💼、学习📚、健康🏃、生活🏠、行动🎯 六类
- 每类显示 Top 5 关键词

## 2025-03-29 更新

- 优化"本周事件类型分布"图表：尺寸从120px放大到180px，中心文字放大
- 将数据来源说明移到图表下方，字号调小（0.7rem/0.65rem）
- 增加分类点击查看功能：点击图例中的分类可查看该分类下的具体条目（仅显示前5条）
- AI分析prompt增加categorizedEntries字段，返回每条记录的分类
