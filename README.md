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

To find and delete empty folders:

```sh
find . -type d -empty -print
find . -type d -empty -delete
```

## To Do

- [x] Handle cases where cities doesn't have Census data;
- [x] Fix IndexError exception;
- [x] Fix KeyboardInterrupt exception;
- [X] Create .py file from notebook;
- [X] Log end message just once;
- [ ] Implement sys.argv for state code as parameter;
- [ ] Fix the exception counter;
- [ ] Implement the logging library;
- [ ] Create script to save city codes into respective files;
- [ ] Reprocess cities with no data (double check);
