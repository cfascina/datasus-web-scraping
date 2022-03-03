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

The folder ``codes`` must store a file for each state, with all the existing city codes on the platform. Run:
  
```sh
get_codes.py
```

Run ``main.py`` with the state code as a parameter. For the state of São Paulo, for example, the command would be the following:

```sh
python3 main.py 35
```

## GCP  Useful Commands

I you're going to use GCP VMs, here are some useful commands:

To copy remote files:

```sh
gcloud compute scp --recurse vm-name:/remote/path/ ~/local/path/
```

To rename VM instances:

```sh
gcloud beta compute instances set-name vm-current-name --new-name=vm-new-name
```

To find and delete empty folders:

```sh
find . -type d -empty -print
find . -type d -empty -delete
```
