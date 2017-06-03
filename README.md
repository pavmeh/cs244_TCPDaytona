# cs244_TCPDaytona
Provision an n1-standard-2 (2 vCPUs, 7.5 GB memory) Google Cloud instance
running Ubuntu 16.04. Allow for HTTP and HTTPS traffic.

Install git if needed:
sudo apt-get update
sudo apt-get install git

clone repo:
```
git clone https://github.com/pavmeh/cs244_TCPDaytona/
```
Use ``` ./setup.sh ``` to install all the dependencies. Press Y if prompted.
If this breaks, run the commands in the script individually in the terminal.
This only needs to be run only once per VM instance.

Run ```./run_experiments.sh``` to run the experiment. It will take
approximately 30 seconds to run. An http server automatically create that can
used to view the data files created (.png) by clicking on the external IP link
in the cloud platform manager for the VM istance. Note, you must change the
link to:

```
http://&lt;external IP&gt;/&lt;name of file&gt;
```
so that it uses http instead of https. Then, you can simply type in the name of
the png file you wish to view after the slash, as shown above.

If you wish to run the experiment agian, run ```./cleanup.sh``` first. This
deletes the previous data files.
