---

## 🗂️ file-dropper

A minimalist, Dockerized file upload service you can self-host and trust **for simple use cases**.

**file-dropper** is a lightweight, web-based file dropbox built for devs, sysadmins, and everyday folks who just need an easy way to send or receive files—without relying on cloud storage, weird clients, or bloated services.

### 🚀 Features

- 🐳 **Docker-native**: Spins up in seconds via `docker run` or `compose`
- 🌐 **Web UI**: Clean drag-and-drop interface for uploading files
- 📁 **Direct-to-disk**: Uploaded files land right in your shared volume
- 🤝 **Works great locally**: Drop files between machines, VMs, or containers
- 🔐 **Optional HTTP basic auth** if you want a light gate
- ⚙️ **Customizable**: Modify templates, change storage paths, tweak limits

### 🧠 Why it exists

Because sometimes you just need a simple way to move a file from one machine to another. No signup, no login, no cloud drama—just a clean dropzone in your browser that writes to disk.

file-dropper is perfect for:
- Transferring logs, configs, or patches across systems
- Sending someone a file without emailing it
- Temporary local LAN setups, VM communication, or airgap bridge work

🛑 **Note:** This is *not* a hardened or security-audited tool. It’s built for **convenience** in **controlled environments**. Use with care if exposed to the wider internet.

---

Let me know if you have any questions. Happy home-labbing in the fascist dystopian future. Delete the cloud and embrace self hosting.
