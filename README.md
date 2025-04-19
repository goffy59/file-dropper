
---

```text

 _____ _ _        ____                                  
|  ___(_) | ___  |  _ \ _ __ ___  _ __  _ __   ___ _ __ 
| |_  | | |/ _ \ | | | | '__/ _ \| '_ \| '_ \ / _ \ '__|
|  _| | | |  __/ | |_| | | | (_) | |_) | |_) |  __/ |   
|_|   |_|_|\___| |____/|_|  \___/| .__/| .__/ \___|_|   
                                 |_|   |_|              

                                                                         
```  

> “I built this for the ones who don’t ask permission.  
> For sysadmins who live like ghosts.  
> For devs who never trusted the cloud.  
> For rebels, refugees, and the radiant few.  
> May your files move in silence. May your machines whisper only to you.”  
> — *Kateryna Sofiya Chernenko*

---

## 🗂️ file-dropper

A minimalist, Dockerized file upload service you can self-host and trust **for simple use cases**.

**file-dropper** is a lightweight, web-based file dropbox built for devs, sysadmins, and everyday folks who just need an easy way to send or receive files—without relying on cloud storage, weird clients, or bloated services.

---

### 🚀 Features

- 🐳 **Docker-native**: Spins up in seconds via `docker run` or `compose`
- 🌐 **Web UI**: Clean interface for uploading and downloading files
- 📁 **Direct-to-disk**: Uploaded files land right in your shared volume
- 🤝 **Works great locally**: Drop files between machines, VMs, or containers
- ⚙️ **Customizable**: Modify templates, change storage paths, tweak limits

---

### 🧠 Why It Exists

Because sometimes you just need a simple way to move a file from one machine to another.  
No signup. No login. No cloud drama.  
Just a clean dropzone in your browser that writes to disk.

Perfect for:

- Transferring logs, configs, or patches across systems
- Sending someone a file without emailing it
- Temporary local LAN setups, VM communication, or airgap bridge work

---

### 🔐 Threat Model

> _This is not Zero Trust. This is Zero Bullshit._

file-dropper is designed for **controlled environments** where you already trust the network and the people on it. Think: your LAN, your homelab, or your airgapped edge device. If you're running this exposed on the open internet without protections, you’re building a zipline over a volcano.

Security assumptions:

- No auth, no encryption, no access controls—**by design**
- Anyone who can reach the web UI can upload/download
- Files are stored **on disk**, unencrypted, in the open
- It’s Flask behind the curtain—respect the stack

If you need auth, HTTPS, or sandboxing, wrap it in:
- A reverse proxy like Nginx or Traefik
- A container firewall or MAC policy
- Physical or network segmentation

Bottom line: **use only where you already trust the channel.** Don’t treat this like a vault. Treat it like a courier that doesn’t ask questions.

### 📦 Installation:
'''bash
git clone https://github.com/goffy59/file-dropper.git

cd file-dropper

docker build -t file-dropper .
'''

---

## 💻 Usage Examples

### 📦 Example 1: Docker CLI (w/ lsio swag network and reverse proxy)

```bash
docker run -d \
  -e TZ=Etc/UTC \
  --net=lsio \
  --label "swag=enable" \
  -e UID=1000 \
  -e GID=1000 \
  -e FLASK_MAX_CONTENT_LENGTH=8796093022208 \
  -v /home/docker/file-dropper/app/uploads:/app/uploads \
  --name file-dropper \
  --restart always \
  --label com.centurylinklabs.watchtower.enable=false \
  file-dropper
```

---

### 🔧 Example 2: Minimal Docker CLI

```bash
docker run -d \
  -e FLASK_MAX_CONTENT_LENGTH=8796093022208 \
  -v /home/docker/file-dropper/app/uploads:/app/uploads \
  --name file-dropper \
  --restart always \
  file-dropper
```

---

### 🧱 Example 3: Docker Compose

```yaml
name: file-dropper
services:
  file-dropper:
    environment:
      - FLASK_MAX_CONTENT_LENGTH=8796093022208
    volumes:
      - /home/docker/file-dropper/app/uploads:/app/uploads
    container_name: file-dropper
    restart: always
    image: file-dropper
```

---

### 📬 Questions?

If you're confused, broken, or just vibing in your lab—feel free to reach out.  
Happy home-labbing in the boring fascist dystopian future nightmare.  
**Delete the cloud. Embrace self-hosting.**

---
