# Flood extent tool

# EC2 deployment

Setup the EC2 instance, add an inbound rule in security groups 'Custom TCP with port range 8501, ipv4', connect via SSH and run:

```
sudo apt-get update

wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh

bash ~/miniconda.sh -b -p ~/miniconda

echo "PATH=$PATH:$HOME/miniconda/bin" >> ~/.bashrc

source ~/.bashrc

pip install streamlit

pip install plotly_express

sudo apt-get install tmux

tmux new -s streamlit-app-session

streamlit run streamlit_app.py

#Ctrl+B and then D

```

If reconenction to streamlit-app-session is required run: 

```
tmux attach -t streamlit-app-session
```

