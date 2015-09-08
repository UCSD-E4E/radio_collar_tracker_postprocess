#!/bin/bash
# Remove extraneous packages
sudo apt-get remove apache2 openbox xscreensaver mesa-common-dev aspell gksu gnome-keyring gsettings-desktop-schemas hicolor-icon-theme hunspell-en-us javascript-common leafpad lxde-common lxmenu-data lxpanel lxsession lxterminal whiptail --purge -y

# Update and upgrad existing software
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get dist-upgrade -y
sudo apt-get clean -y
sudo apt-get autoremove -y

# Install dependencies
sudo apt-get install build-essential -y
sudo apt-get install cpufrequtils -y
sudo apt-get install sysfsutils -y
sudo apt-get install gtk+-2.0 -y
sudo apt-get install libgtk2.0-dev -y
sudo apt-get install libcairo2-dev -y
sudo apt-get install git -y
sudo apt-get install cmake -y
sudo apt-get install libusb-1.0-0-dev -y
sudo apt-get install lightdm -y

# Set CPU governor
sudo mv /etc/init.d/cpufrequtils /etc/init.d/cpufrequtils.old
sudo chmod -x /etc/init.d/cpufrequtils.old
sudo cat /etc/init.d/cpufrequtils.old | sed 's_^GOVERNOR=\"[a-zA-Z]*\"$_GOVERNOR=\"performance\"_' > /etc/init.d/cpufrequtils

sudo echo blacklist dvb_usb_rtl28xxu > /etc/modprobe.d/rtlsdr.conf

cd ~
git clone https://github.com/steve-m/librtlsdr
mkdir ~/librtlsdr/build
cd ~/librtlsdr/build
cmake ../ -DINSTALL_UDEV_RULES=ON
make
make install
ldconfig
cd ~
rm -rf ~/librtlsdr

mkdir /media/RAW_DATA

echo "sudo mount /dev/mmcblk0p1 /media/RAW_DATA -o dmask=000,fmask=111" >> /etc/rc.local

cd /home/debian
git clone https://github.com/UCSD-E4E/radio_collar_tracker
cp -r radio_collar_tracker/CurrentCode/BBB/gpio/ .
cp -r radio_collar_tracker/CurrentCode/BBB/xcode/ .
chmod +x gpio/build
cd gpio
./build
cd ../xcode
chmod +x build
rm *.o
make
chmod +x run

