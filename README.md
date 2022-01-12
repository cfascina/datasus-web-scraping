To copy remote files to local machine:
gcloud compute scp --recurse vm-name:/remote/data/path/ ~/local/path/

To rename VM instances:
gcloud beta compute instances set-name vm-current-name --new-name=vm-new-name
