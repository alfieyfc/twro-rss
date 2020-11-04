# TWRO 官方網站公告 Line 推播

Quickstart
===

### Clone repo
```sh
git clone https://github.com/alfieyfc/twro-rss.git
cd twro-rss/
```
```sh
touch news_record.txt
python main.py
```

Run with Docker
===

```sh
docker run -v `pwd`/news_record.txt:/data/news_record.txt alfieyfc/twro-rss
```

Build your own with Docker
===

You may change Timezone of your workload if that's what you want
```dockerfile
# Dockefile
# Change timezone ENV if needed
ENV TZ=Asia/Taipei
```
```sh
docker build -t <IMAGE_NAME>[:TAG] .
docker run -v `pwd`/news_record.txt:/data/news_record.txt IMAGE_NAME:TAG
```

Set up a crontab
===
You may want to set up a crontab to check for news to feed every few minutes or so. I'm using Kubernetes CronJob for this. You should adjust to your own needs.

Set up a CronJob with Kubernetes
---

Edit `cronjob.yaml` with your Line Notify token:
```yaml
          - env:
            - name: LINE_TOKEN
              value: __YOUR_TOKEN__
```

Edit cron schedule to your needs:
```yaml
  # Every 1, 6, 11, 16, 21, 26, 31, 36, 41, 46, 51 and 56th minute past every hour
  schedule: 1/5 * * * * 
```

### Create CronJob
```sh
kubectl apply -f cronjob.yaml
```

### Create PV
If directly using the YAML file from this repo, you will have to create your own Persistent Volume and bound `pvc/twro-rss-pvc` to the PV. See [docs](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) for more info.