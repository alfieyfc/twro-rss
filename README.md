# TWRO 官方網站公告 Line 推播

![](https://scontent.ftpe7-2.fna.fbcdn.net/v/t1.0-9/122853984_681930529135887_8742212903482088781_o.jpg?_nc_cat=104&ccb=2&_nc_sid=730e14&_nc_ohc=_IFSSL1x52EAX9IJ45q&_nc_ht=scontent.ftpe7-2.fna&oh=91ec9301b06f8bc6b3285efaacdcf1d4&oe=5FC655EB)

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
