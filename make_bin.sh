REPO_DIR=$(pwd)
if [ ! -d "$HOME/rct/bin/" ] ; then
	mkdir -p $HOME/rct/bin/
fi
cd $(REPO_DIR)/CurrentCode/PostProcessC/
chmod +x build*
./build-spectrumAnalysis

cd $(REPO_DIR)
cp $(REPO_DIR)/collarDetect/altFilter.py $HOME/rct/bin/
cp $(REPO_DIR)/CurrentCode/PostProcessC/spectrumAnalysis $HOME/rct/bin/
cp $(REPO_DIR)/CLI_GUI/cas.sh $HOME/rct/bin/
cp $(REPO_DIR)/CLI_GUI/get_run_num.py $HOME/rct/bin/
chmod +x $HOME/rct/bin/*
