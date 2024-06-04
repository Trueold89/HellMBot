# HellMBot

### Discord bot that will wake your friends up from full mute by putting them through 9 circles of hell 🔥

![](https://cdn.orudo.ru/.work/trueold89/git/hellm/Header.svg)

## 🔗 Links:
[<img src="https://cdn.orudo.ru/.work/trueold89/git/hellm/ORUDO.svg" alt="SVG Image" width="300" height="102" style="padding-right: 10px">](https://git.orudo.ru/trueold89/HellMBot)
[<img src="https://cdn.orudo.ru/.work/trueold89/git/hellm/GitHub.svg" alt="SVG Image" width="300" height="102" style="padding-right: 10px">](https://github.com/Trueold89/HellMBot)
[<img src="https://cdn.orudo.ru/.work/trueold89/git/hellm/GitLab.svg" alt="SVG Image" width="300" height="102" style="padding-right: 10px">](https://gitlab.com/Trueold89/hellmbot)
[<img src="https://cdn.orudo.ru/.work/trueold89/git/hellm/Discord.svg" alt="SVG Image" width="300" height="102" style="padding-right: 10px">](https://discord.com/oauth2/authorize?client_id=1247176574969577514)

***

## ⁉️ Usage:

![](https://cdn.orudo.ru/.work/trueold89/git/hellm/faq.svg)

---

- **Add bot to your server**
- **Update the bot's permissions to prevent unnecessary people from using its commands (optional)**
- **Type /create in any text chat you want**
- **Write `/create` in whatever text chat you want**
- **Move any user (or yourself, if you're a masochist) to any of the channels in the group created by bot**
- **Have fun!**

## 📦 Deploy:

***

### Python venv:


![](https://cdn.orudo.ru/.work/trueold89/git/hellm/python.svg)

- **Install python package from [git.orudo.ru](https://git.orudo.ru/trueold89/HellMBot/packages)**:
```shell
pip install pip install --extra-index-url https://git.orudo.ru/api/packages/trueold89/pypi/simple/ HellMBot 
```

- **Or build your own package from sources**:

*Clone source code repo:*
```shell
git clone https://git.orudo.ru/trueold89/HellMBot.git && cd HellMBot
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

- **Set [system environment variables](#available-system-environment-variables): (Linux bash example)**
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

- **Pull image from [git.orudo.ru](https://git.orudo.ru/trueold89/HellMBot/packages)**:
```shell
docker pull git.orudo.ru/trueold89/hellmbot:latest
```

- **Or build your own image:**

*Clone source code repo:*
```shell
git clone https://git.orudo.ru/trueold89/HellMBot.git && cd HellMBot/docker
```

*Edit the Dockerfile with your changes (Optional)*

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
 -d git.orudo.ru/trueold89/hellmbot:latest
```

- **Or using docker-compose:**

```yml
services:
  hellm_bot:
    image: git.orudo.ru/trueold89/hellmbot:latest
    container_name: HellMBot 
    volumes:
      - hellm_db:/etc/hellmbot
    restart: 'unless-stopped'
    environment:
      BOT_TOKEN: "insertyourbottokenhere"
      CLIENT_ID: "insertyourclientidhere"
volumes:
    hellm_db:
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
