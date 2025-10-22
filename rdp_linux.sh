#!/bin/bash
set -e

echo "Updating packages..."
sudo apt update
sudo apt upgrade -y

echo "Installing GUI (Xfce) and necessary goodies..."
sudo apt install -y xfce4 xfce4-goodies

echo "Installing xRDP..."
sudo apt install -y xrdp

echo "Adding xrdp user to ssl-cert group (so xrdp can access certificates)..."
sudo adduser xrdp ssl-cert

echo "Setting Xfce as default session for RDP users..."
# For current user (you can adapt for other users)
echo "xfce4-session" > ~/.xsession

echo "Editing /etc/xrdp/startwm.sh so that Xfce launches correctly..."
sudo cp /etc/xrdp/startwm.sh /etc/xrdp/startwm.sh.bak
sudo tee /etc/xrdp/startwm.sh > /dev/null << 'EOF'
#!/bin/sh
if [ -r /etc/default/locale ]; then
  . /etc/default/locale
  export LANG LANGUAGE
fi
# launch Xfce
startxfce4
EOF
sudo chmod 755 /etc/xrdp/startwm.sh

echo "Enabling and starting xRDP service..."
sudo systemctl enable xrdp
sudo systemctl restart xrdp

echo "Opening firewall port 3389 for RDP (via UFW)..."
sudo ufw allow 3389/tcp
sudo ufw reload

echo "Installation complete. Please reboot now."
sudo reboot
