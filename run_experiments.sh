
sudo python mininetTopo.py --client="normal" --server="linux"
sudo python mininetTopo.py --client="splitACK" --server="linux"
sudo python mininetTopo.py --client="dupACK" --server="linux"
sudo python mininetTopo.py --client="opACK" --server="linux"

python plot.py
sudo python -m SimpleHTTPServer 80
