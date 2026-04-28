---
name: mount-smb-share
description: Mount SMB/CIFS shared folders on Linux. Covers mounting Windows/Samba shares, NAS drives, and adding to fstab for persistent mounts.
tags: [smb, cifs, mount, nas, network-storage, samba]
---

# Mount SMB/CIFS Shared Folder

Mount a Windows/Samba/NAS shared folder on Linux. Requires `cifs-utils` package.

## Prerequisites

```bash
# Install cifs-utils
sudo apt install -y cifs-utils

# For macOS (uses built-in smbfs, no install needed)
```

## One-Time Mount

### With credentials file (recommended — password not in history)

```bash
# Create credentials file
sudo nano ~/.smbcredentials
```

Write:
```
username=YOUR_USERNAME
password=YOUR_PASSWORD
domain=WORKGROUP
```

Secure it:
```bash
chmod 600 ~/.smbcredentials
```

### Mount command

```bash
# Create mount point
sudo mkdir -p /mnt/nas

# Mount
sudo mount -t cifs //SERVER_IP/SHARE_NAME /mnt/nas -o credentials=~/.smbcredentials,iocharset=utf8,file_mode=0755,dir_mode=0755

# Verify
ls /mnt/nas
df -h /mnt/nas
```

### Common mount options

```bash
# All options explained:
sudo mount -t cifs //192.168.1.100/share /mnt/nas -o credentials=~/.smbcredentials,iocharset=utf8,file_mode=0755,dir_mode=0755,noperm,vers=3.0

# vers=3.0    → SMB protocol version (3.0 for modern, 2.0 for older, 1.0 for legacy)
# noperm      → client doesn't enforce permissions (relies on server)
# uid=1000    → map files to local user ID
# gid=1000    → map files to local group ID
# nounix      → disable UNIX extensions for Windows shares
# sec=ntlmssp → authentication method (ntlmssp for modern Windows)
```

## Persistent Mount (fstab)

```bash
# Edit fstab
sudo nano /etc/fstab
```

Add line:
```
//192.168.1.100/share  /mnt/nas  cifs  credentials=/home/YOUR_USER/.smbcredentials,iocharset=utf8,file_mode=0755,dir_mode=0755,noperm,x-systemd.automount,noauto,users  0  0
```

Key fstab options:
- `x-systemd.automount` — mount on access (no boot delay if server is down)
- `noauto` — don't mount automatically at boot (combined with automount = lazy mount)
- `users` — allow any user to mount/unmount
- `_netdev` — wait for network before mounting (for fstab without automount)

Test fstab entry:
```bash
# Test mounting
sudo mount /mnt/nas

# Check
ls /mnt/nas

# Unmount
sudo umount /mnt/nas
```

## Unmount

```bash
sudo umount /mnt/nas

# If "target is busy":
sudo umount -l /mnt/nas   # lazy unmount
# or find what's using it:
lsof /mnt/nas
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `mount error(13): Permission denied` | Wrong username/password, or SMB protocol mismatch. Try `vers=2.0` or `sec=ntlmssp` |
| `mount error(112): Host is down` | Server unreachable or SMB port 445 blocked. Check `ping SERVER_IP` and `nmap -p 445 SERVER_IP` |
| `mount error(2): No such file or directory` | Share name doesn't exist. List shares with `smbclient -L //SERVER_IP -U USER` |
| `mount error(95): Operation not supported` | SMB version mismatch. Try `vers=1.0`, `vers=2.0`, or `vers=3.0` |
| Slow transfers | Add `,rsize=1048576,wsize=1048576` to mount options |
| Can't write files | Check `file_mode=0755,dir_mode=0755,noperm` options |
| Chinese filenames garbled | Add `,iocharset=utf8` |
| Need to reconnect after sleep | Create systemd service or use `sudo mount -a` in cron |

## Quick Reference

```bash
# List available shares on a server
smbclient -L //192.168.1.100 -U USERNAME

# Quick mount (all-in-one)
sudo mount -t cifs //192.168.1.100/share /mnt/nas -o username=USER,password=PASS,vers=3.0

# Check mounted SMB shares
mount | grep cifs

# Check SMB protocol version in use
dmesg | grep CIFS
```
