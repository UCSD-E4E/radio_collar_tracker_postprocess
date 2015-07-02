#!/bin/bash
mkdir $HOME/rct $HOME/rct/bin $HOME/rct/lib
sudo pip install -e git+git://github.com/Turbo87/utm.git#egg=master --src $HOME/rct/lib/
cp ./display_data.py $HOME/rct/bin/
chmod u+x $HOME/rct/bin/display_data.py
echo 'export PATH=$PATH:$HOME/rct/bin' >> $HOME/.bashrc
source $HOME/.bashrc
