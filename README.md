# HellMBot

### Discord bot that will wake your friends up from deafen by putting them through 9 circles of hell 🔥

![](https://cdn.orudo.ru/.work/trueold89/git/hellm/Header.svg)

## 🔗 Links:
[<img src="https://cdn.orudo.ru/.work/trueold89/git/hellm/Discord.svg" alt="SVG Image" width="300" height="102" style="padding-right: 10px">](https://discord.com/oauth2/authorize?client_id=1247176574969577514)

***

## ⁉️ Usage:

![](https://cdn.orudo.ru/.work/trueold89/git/hellm/faq.svg)

---

- **Add bot to your server**
- **Update the bot's permissions to prevent unnecessary people from using its commands (optional)**
- **Write `/create` in whatever text chat you want**
- **Move any user (or yourself, if you're a masochist) to any of the channels in the group created by bot**
- **Have fun!**

## 📦 Deploy:



### Python venv:


![](https://cdn.orudo.ru/.work/trueold89/git/hellm/python.svg)

### Build package from source:
---

*Clone source code repo:*
```shell
git clone https://github.com/Trueold89/HellMBot.git && cd HellMBot
```
*Install build deps:*
```shell
pip install setuptools
```
*Build package:*
```shell
python3 setup.py sdist
```

*Install built package:*
```shell
pip install dist/*
```

---

- **Set [system environment variables](#available-system-environment-variables):**
```bash
export BOT_TOKEN=insertyourbottokenhere
```
```bash
export CLIENT_ID=insertyourclientidhere
```

---

- **Start bot:**
```shell
heelm
```

***

### Docker:

![](https://cdn.orudo.ru/.work/trueold89/git/hellm/docker.svg)

- **Pull image from [DockerHub](https://hub.docker.com/r/trueold89/hellm)**:
```shell
docker pull trueold89/hellm:latest
```

- **Or build your own image:**

*Clone source code repo:*
```shell
git clone https://github.com/Trueold89/HellMBot.git
```

*Build image:*
```shell
docker build -t hellmbot .
```

---

- **Create docker volume that will use to store DataBase:**
```shell
docker volume create hellm_db
```

---

- **Deploy using docker-cli:**
```shell
docker run \
 --name HellMBot\
 --restart=unless-stopped \
 -v hellm_db:/etc/hellmbot/
 -e BOT_TOKEN="insertyourbottokenhere" \
 -e CLIENT_ID="insertyourclientidhere" \
 -d trueold89/hellm:latest
```

- **Or using docker-compose:**

```yaml
services:
  hellm_bot:
    image: trueold89/hellm:latest
    container_name: HellMBot 
    environment:
      BOT_TOKEN: "insertyourbottokenhere"
      CLIENT_ID: "insertyourclientidhere"
      DB_PATH: "/etc/hellmbot/database.sqlite"
      CIRCLES_COUNT: 9
    volumes:
      - hellm:/etc/hellmbot
    restart: 'unless-stopped'

volumes:
  hellm:
```

```shell
docker compose up -d
```

***

## 📋 Available system environment variables

***

- `BOT_TOKEN` - **Discord Bot TOKEN** *[(How to get)](https://discordjs.guide/preparations/setting-up-a-bot-application.html#creating-your-bot)*
- `CLIENT_ID` - **Discord Application ID** *[(How to get)](https://docs.discordadvertising.com/getting-your-application-id)*
- `DB_PATH` - **Path to SQLite DataBase file** *(Optional | Highly recommended to change when running bot on Windows systems) (Default Value: "/etc/hellmbot/database.sqlite")*
- `CIRCLES_COUNT` - **Number of channels the bot creates when the "/create" command is activated.** *(Optional)* *(Default value: 9)*

## Other:

**[Design file (Figma Community)](https://www.figma.com/community/file/1380949720890295687/hellm-bot)**

[![](https://i.imgur.com/SFpy2G2.png)](https://www.figma.com/community/file/1380949720890295687/hellm-bot)
