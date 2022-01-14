# DataSUS Web Scraping

This script was developed to collect data about resident population through the [DataSUS TabNet](http://tabnet.datasus.gov.br/cgi/deftohtm.exe?popsvs/cnv/popbr.def) platform.

## Useful commands

To copy remote files:

```sh
gcloud compute scp --recurse vm-name:/remote/path/ ~/local/path/
```

To rename VM instances:

```sh
gcloud beta compute instances set-name vm-current-name --new-name=vm-new-name
```

## To Do

- [x] Handle cases where cities doesn't have Census data;
- [x] Fix IndexError exception;
- [ ] Create a .py file, pasing the UF code as parameter;
- [ ] Fix the exception counter;
- [ ] Implement the logging library;
- [ ] Log end message just once;
- [ ] Create script to save city codes into respective files;
- [ ] Reprocess the cities:
  - [ ] 150475;
  - [ ] 320225;
  - [ ] 330285;
