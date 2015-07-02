#!/bin/bash
mkdir $HOME/rct $HOME/rct/bin $HOME/rct/lib
COL_DISP_DIR=$(pwd)
sudo pip install -e git+git://github.com/Turbo87/utm.git#egg=master --src $HOME/rct/lib/
cp ${COL_DISP_DIR}/display_data.py $HOME/rct/bin/
chmod u+x $HOME/rct/bin/display_data.py
if [ ! -e "$HOME/.bashrc" ] ; then
	echo '#!/bin/bash' >> $HOME/.bashrc
fi
echo 'export PATH=$PATH:$HOME/rct/bin' >> $HOME/.bashrc
source $HOME/.bashrc
