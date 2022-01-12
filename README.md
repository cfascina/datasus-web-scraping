# DataSUS Web Scraping
This script was developed to collect data about resident population through the [DataSUS TabNet](http://tabnet.datasus.gov.br/cgi/deftohtm.exe?popsvs/cnv/popbr.def) platform.

#### Useful commands
To copy remote files:
`gcloud compute scp --recurse vm-name:/remote/path/ ~/local/path/`

To rename VM instances:
`gcloud beta compute instances set-name vm-current-name --new-name=vm-new-name`

#### To Do
[ ] Handle cases where cities doesn't have Census data;
[ ] Pass UF code as parameter to the main script;
[ ] Fix the exception counter;
[ ] Implement the logging library;
