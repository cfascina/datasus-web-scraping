# DataSUS Web Scraping
This script was developed to collect data about resident population through the [DataSUS TabNet](http://tabnet.datasus.gov.br/cgi/deftohtm.exe?popsvs/cnv/popbr.def) platform.

#### Useful commands
To copy remote files:
```sh
gcloud compute scp --recurse vm-name:/remote/path/ ~/local/path/
```

To rename VM instances:
```sh
gcloud beta compute instances set-name vm-current-name --new-name=vm-new-name
```

#### To Do
- [x] Handle cases where cities doesn't have Census data;
- [ ] Create a .py file, pasing the UF code as parameter;
- [ ] Fix the exception counter;
- [ ] Implement the logging library;
