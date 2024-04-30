# Practical Encryption

## Ubuntu Instance

```bash
# Install multipass
multipass launch -n ubuntuserver --cloud-init cloud-config.yaml
multipass list
ssh ubuntuserver@IPAddressFromList

multipass help
multipass stop ubuntuserver
multipass delete
multipass purge 
```

## GNU Privacy Guard - GPG

```bash
sudo apt update && sudo apt upgrade gnupg

### BobPC

gpg --gen-key
>>> Name: bob
>>> Email: bob@pc.com

gpg --list-keys

gpg --export --armor bob@pc.com
gpg --export --armor bob@pc.com > bobpublickey.asc

sudo cp bobpublickey.asc  /home/alice

### AlicePC

gpg bobpublickey.asc
>>> Bob <bob@pc.com>

gpg --import bobpublickey.asc
gpg --list-keys

# Change key trust level
gpg --edit-key bob@pc.com
    gpg> trust 
            4
    gpg> q

gpg --list-keys

# Sign key for trustness
gpg --sign-key bob@pc.com
```

### Example - Private Share

```bash
### Alice PC
echo "This is Test1" > sec.txt
gpg -e -r bob@pc.com sec.txt  # e: encrypt , r: recipient
cat sec.txt.gpg
sudo cp sec.txt.gpg /home/bob

### BobPC
cat sec.txt.gpg
gpg -d sec.txt.gpg  # d: decrypt
gpg -d sec.txt.gpg  > secfile.txt
```

### Example - Signing & Verifying

```bash
### Alice PC
cat syslog  # test file

# Sign
gpg --output syslog.sig --sign syslog   # Asks Alice's PrivateKey

sudo cp syslog.sig /home/bob

### Bob PC
#   gpg --sign-key alice@pc.com

# Verify
gpg --verify syslog.sig

# Decrypt
gpg -d syslog.sig

### Alice PC

# Get signature and file seperately
gpg --output syslog.dsig --detach-sign syslog   # need to send both 2 files

# Without compression Original doc
gpg --clearsign --output syslogOrg syslog

```
