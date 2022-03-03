# DataSUS Web Scraping

This script was developed to collect data about resident population through the [DataSUS TabNet](http://tabnet.datasus.gov.br/cgi/deftohtm.exe?popsvs/cnv/popbr.def) platform.

## How to Use

Create and activate a virtual environment:

```sh
virutalenv .venv
source .venv/bin/activate
```

Install the dependencies:

```sh
pip install -r requirements.txt
```

Create a folder named ``codes`` in the root directory (it will be used throughout the scripts).

The folder ``codes`` will store a file for each state. Each one of them will contain all their city codes that exists on the platform. Run:
  
```sh
get_codes.py
```

Run ``main.py`` with the state code as a parameter. For the state of São Paulo, for example, the command would be the following:

```sh
python3 main.py 35
```

In some scenarios, the platform returns empty data when it actually exists. To check in which cases this happened (city and year), and download the missing ones, run:

```sh
python3 get_missing.py
```

## GCP Commands

I you're going to use GCP VMs, here are some useful commands:

To copy files from remote to your local machine:

```sh
gcloud compute scp --recurse vm-name:/remote/path/ ~/local/path/
```

To rename VM instances:

```sh
gcloud beta compute instances set-name vm-current-name --new-name=vm-new-name
```
