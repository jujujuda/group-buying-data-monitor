# 部署文档

## 环境要求

- Python 3.8+
- OpenClaw Gateway

## 安装

### 1. 克隆项目
```bash
git clone https://github.com/your-repo/group-buying-data-monitor.git
cd group-buying-data-monitor
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

依赖包括：
- requests
- pyyaml
- beautifulsoup4

### 3. 配置

编辑 `config/platforms.yaml`：

```yaml
feishu:
  webhook_url: "你的飞书Webhook地址"

platforms:
  - name: dianping
    shop_id: "店铺ID"
```

获取飞书Webhook：
1. 打开飞书群设置
2. 添加机器人 -> 自定义机器人
3. 复制Webhook地址

### 4. 运行

```bash
# 手动运行
python -m skills.data_monitor.scripts.fetcher

# 定时运行 (使用cron)
*/30 * * * * /usr/bin/python3 /path/to/fetcher.py
```

## OpenClaw Skills 集成

将 `skills/data-monitor` 复制到 OpenClaw 的 skills 目录：

```bash
cp -r skills/data-monitor ~/.openclaw/skills/
```

然后可以在 OpenClaw 中使用该 Skill 进行数据监测。

## Docker 部署 (可选)

```dockerfile
FROM python:3.8-slim

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

CMD ["python", "-m", "skills.data_monitor.scripts.fetcher"]
```

构建运行：
```bash
docker build -t data-monitor .
docker run -d --name data-monitor data-monitor
```

## 监控

- 检查日志输出
- 监控飞书消息推送
- 定期检查数据准确性

## 常见问题

Q: 数据抓取失败
A: 检查网络连接，确保目标平台可访问

Q: 飞书消息收不到
A: 验证Webhook URL是否正确，检查机器人是否在群里
