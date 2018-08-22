#this file pulls down everything needed to get the project working from a fresh install
#just make sure to update and upgrade your packages at least once first

echo -e "\e[33msudo apt-get install -y python3-dev python3-pip python3-tk libopenblas-dev libfftw3-dev libsuitesparse-dev make\e[39m"
sudo apt-get install -y python3-dev python3-pip python3-tk libopenblas-dev libfftw3-dev libsuitesparse-dev make

echo -e "\e[33mpip3 install numpy scipy matplotlib termcolor shapely\e[39m"
pip3 install numpy scipy matplotlib termcolor shapely

  
echo -e "\e[33mgit clone https://github.com/phoebe-p/S4\e[39m"
git clone https://github.com/phoebe-p/S4
 
echo -e "\e[33mcd S4; make S4_pyext\e[39m"
cd S4; make S4_pyext
echo -e "\\e[91;1mDO NOT UPDATE PIP, EVEN IF IT ASKS\\e[39;0m"

echo -e "\e[33mcd ..; rm -rf S4\e[39m"
cd ..; rm -rf S4
