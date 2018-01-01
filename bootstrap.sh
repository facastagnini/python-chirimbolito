#/usr/bin/env bash -eux
# Bootstrap a Raspberry Pi to run the Bitcoin address monitoring tool

# update the APT references
sudo apt-get update

# upgrade the OS
sudo apt-get dist-upgrade -y

# install necessary tools
sudo apt-get install build-essential python-dev python-smbus python-pip git i2c-tools
sudo pip install --upgrade pip
sudo pip install RPi.GPIO
sudo pip install ballpark coverage
sudo pip install future   # remove after https://github.com/debrouwere/python-ballpark/pull/5
sudo pip install pandas   # remove after https://github.com/debrouwere/python-ballpark/pull/6

# Clone this repo if missing
cd ~
test ! -d rpi-lcd-bitcoin-monitor && git clone https://github.com/facastagnini/rpi-lcd-bitcoin-monitor.git
cd rpi-lcd-bitcoin-monitor
git pull

# place a sample config file 
test ! -f configuration.json-sample && cp configuration.json-sample configuration.json

# cleanup apt packages in the local cache
apt-get clean

cat <<EOF 
Setup completed.
The monitoring script should be working with the sample configuration, the LCD should be diplaying information about the bitcoin network and the balance of Satoshi's address.
You can modify configuration.json and replace Satoshi's address with yours, then reboot to apply the changes.
Enjoy!
EOF
