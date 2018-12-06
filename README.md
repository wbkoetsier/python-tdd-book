# Test-driven development with Python
Following the book in print (5th edition) and [online](https://www.obeythetestinggoat.com/).

## Requirements
Python: 3.6+

`pip freeze` locally:
```
Django==1.11.16
pkg-resources==0.0.0
pytz==2018.7
selenium==3.141.0
urllib3==1.24.1
```

Geckodriver: 0.23.0 (anywhere on the path) with Firefox 63.0. Or visit https://github.com/mozilla/geckodriver/releases.

[(Vanilla) Bootstrap 3.3.4](https://github.com/twbs/bootstrap/releases/download/v3.3.4/bootstrap-3.3.4-dist.zip).


`pip freeze` on server:
```
Django==1.11.16
gunicorn==19.9.0
pkg-resources==0.0.0
pytz==2018.7
```

## Run
`python manage.py runserver`

## Test
`python manage.py test functional_tests[ --failfast]`

To run the test in a headless browser, see https://stackoverflow.com/a/23447450/4703154.

`python manage.py test lists`

## Servers
### Choice of server
In chapter 9 "Testing Deployment Using a Staging Site" the author invites the readers to use an actual server rather 
than a local VM. There are free and paid options to set up a server. I decided to go with the paid option, this course 
benefits my career and the maximum cost for a server would be lower than 10 euros p/m - and can be terminated after 
that.

For me, there were several viable options:
- Get a VPS with one of the many Dutch hosting companies.
- Get a DigitalOcean Droplet.
- Get a VM in one of the big clouds.

The benefits of cloud is that being able to work with Azure, AWS or GCP is a recurring item in job openings. I also wish 
to learn how to use Kubernetes, which is possible with all three. I chose Google because I already have some experience 
there, and on top of a [free trial](https://cloud.google.com/free/docs/gcp-free-tier) (which consists of $300 worth of 
credits) they offer certain [always free](https://cloud.google.com/free/docs/always-free-usage-limits) services as well.

### Signing up to GCP
Requires a credit card, but actual charging will only commence after the user's explicit consent. Start 
[here](https://cloud.google.com/free/).

Signing up will automatically create a project 'My First Project'. To change the name, go to hamburger menu (top left in 
the blue bar) -> IAM & admin -> Settings. I'm leaving it as-is.

### Creating a server
GCP has many products to offer and it can be hard to decide which you actually need. For the purpose of this course, 
Compute Engine is a good choice.

To use the web interface to create an instance, go to hamburger menu -> Compute Engine. Click Create (blue button).
- Region/Zone: the default S-Carolina (us-east1-b) offers the f1-micro instance that is within the always free limits.
- For always free, change the Machine type to f1 micro. It should be enough for trying the ToDo-app.
- Boot disk: 
  - OS image: the Ubuntu 18.04 will do. The [minimal](https://wiki.ubuntu.com/Minimal) is more suitable for a fully 
  automated deployment where cli usage isn't really needed.
  - Always free includes a standard persistant disk (as opposed to SSD) with 30 GB-months storage (30 GB 
  stored for one month). Some storage room is needed for the database but Ubuntu Server isn't that big. I'm going with 
  20GB.
- Allow HTTP traffic.

I used the `gcloud` commands to create a server:

```
$ gcloud auth login                                  # opens a browser window to log in to a Google account
$ gcloud projects list                               # discover your PROJECT_ID
$ gcloud config set project <PROJECT_ID>
$ gcloud beta compute instances create superlists \  # instance name
    --image-family ubuntu-1804-lts \                 # image family
    --image-project ubuntu-os-cloud \                # image project
    --tags=http-server \                             # set network tag to allow HTTP traffic 
    --zone=us-east1-b \                              # S. Carolina
    --machine-type=f1-micro \                        # the always free machine type (provided it's in the correct zone)
    --boot-disk-size=20GB \                          # well below the 30GB/month max in the always free
```

Output:

```
WARNING: You have selected a disk size of under [200GB]. This may result in poor I/O performance. For more information, see: https://developers.google.com/compute/docs/disks#performance.
Created [https://www.googleapis.com/compute/beta/projects/<PROJECT_ID>/zones/us-east1-b/instances/superlists].
NAME        ZONE        MACHINE_TYPE  PREEMPTIBLE  INTERNAL_IP  EXTERNAL_IP      STATUS
superlists  us-east1-b  f1-micro                   xx.xx.xx.xx  xx.xx.xx.xx  RUNNING
```

References:
- [Compute Engine docs - Creating and Starting a VM Instance](https://cloud.google.com/compute/docs/instances/create-start-instance)
- [Cloud SDK docs - Quickstart for Debian and Ubuntu](https://cloud.google.com/sdk/docs/quickstart-debian-ubuntu)
- [Cloud SDK docs - gcloud compute](https://cloud.google.com/sdk/gcloud/reference/compute/), also check the 
[beta](https://cloud.google.com/sdk/gcloud/reference/beta/compute/) variant

### Accessing the server
The Compute Engine menu on the left has an item 'VM instances'. Click the 'SSH'-button next to the created instance. 
This will open a console in the browser (new window), with the user logged in and at `~`. The username should be the
username part of your gmail address.

Accessing the server using a different SSH client requires enabling OS Login: go to hamburger menu -> Compute Engine -> 
Metadata. Either click Edit or Add Metadata. Add a new key-value pair, where key is `enable-oslogin` and value is 
`TRUE`. Click Save. Note that this creates a new Ubuntu user: `username_gmail_com` instead of `username`.

This method also requires 
[some IAM roles to be configured](https://cloud.google.com/compute/docs/instances/managing-instance-access#configure_users).
Go to hamburger menu -> IAM & admin -> IAM (Permissions for project "Project name"), find your email address in the list
of members and click the edit pencil next to it. I have added 'Compute OS Admin Login' (Compute) and 'Service Account 
Admin' (IAM). 

Add an SSH key to the Compute project metadata: 

`$ gcloud compute os-login ssh-keys add --key-file path/to/relevant/key.pub --ttl 0`

Where the path is most likely `~/.ssh/id_rsa.pub`. The output can be printed again by:

`$ gcloud compute os-login describe-profile`

To access the VM instance using this key:

`$ ssh username_gmail_com@external.ip`

Note that since the SSH keys are now managed project-wide by OS Login, you don't need to add a key for each new 
instance.

References:
- [Compute Engine docs - Connecting to Instances Using Advanced Methods](https://cloud.google.com/compute/docs/instances/connecting-advanced)
  - "SSH keys are created and managed for you whenever you 
  [connect using Compute Engine tools](https://cloud.google.com/compute/docs/instances/connecting-to-instance)." By this
  they mean when you use the web interface or the `gcloud compute ssh` command (which will ask to create a key).
  - Compute offers 3 ways of providing public SSH keys to instances:
    - [Use IAM roles and OS Login](https://cloud.google.com/compute/docs/instances/managing-instance-access). This is 
    the method I described above.
    - [Manually add SSH keys to metadata (advanced)](https://cloud.google.com/compute/docs/instances/adding-removing-ssh-keys).
    - Have someone else manage your keys.

### Domain name
I bought a domain name with a Dutch company for just a couple of euros. It's in a parked state (it refers to an IP 
address of that company, showing a standard message about the domain being parked) and needs to direct to my new server 
instead.

My Google VM instance also shows it's public IP address. I can log in to my dashboard with the registrar and change my 
DNS settings - replace the registrar's IP address with my Google one. I chose to enter a couple of subdomains for this 
project but I'm also allowed to use a wildcard. I didn't edit the TTL, 24h (my regisrar's default) is fine. It takes a 
couple hours at least for these changes to propagate.

Note that the external IP address is an ephemeral one, which means it will be returned to Googles IP pool when the VM 
instance shuts down. When spinning up a new server, it will be assigned an IP address from that pool, which may be a 
different one than configured now. That would mean also changing the IP address in the registrar.
- To request a static IP (takes imediate effect): go to the hamburger menu -> VPC Network -> External IP addresses, and 
change the type of the IP address in use by the VM instance.
- To attach an existing external IP: change the static address to point to your new instance.

### Port and firewall
The author initially let's us run the server on port 8000. That port is closed by the GCP default firewall rules, so we 
have to add a new rule to allow traffic coming in on port 8000. Go to hamburger menu -> VPC Network -> 
[Firewall rules](https://cloud.google.com/vpc/docs/firewalls).

Click Create a firewall rule.
- name: something like `allow-http-8000`.
- priority: I'm keeping the default 1000. The lower the number, the higher the priority.
- Direction of traffic: ingress (incoming).
- Action: allow.
- Target: I guess it's ok to to specify 'all instances in the network' but I'll try to specify a target (specified 
target tags). A newly created VM by default has the network tag 'http-server', so you can enter that as target tag. I 
suppose the name of the VM should work too, but I haven't tried that. It's also possible to create new tags for your VM, 
but I haven't tried that either.
- Source target: IP ranges, `0.0.0.0/0`.
- Protocols and ports: pick specified protocols and ports, TCP, enter 8000.

Click create. Firewall rules can be set using gcloud (or the REST API) as well.

Later on in the chapter, we switch to the combination Nginx+Gunicorn and port 8000 can be closed off again. Either 
disable the firewall rule (click the rule, click Edit, unfold 'Disable', disable and save) or delete it alltogether 
(also in the Details view of the rule, next to the Edit button).

### Additional security
The author has also mentioned it by linking to 
[an article](https://plusbryan.com/my-first-5-minutes-on-a-server-or-essential-security-for-linux-servers), but these 3 
things:
- Keep Ubuntu updated (`sudo apt update` and `sudo apt upgrade`).
- Edit the SSH conf to disable root login (also, _Never_ set a root password on Ubuntu), specifically: set 
`PermitRootLogin no`.
- Install fail2ban (at the very least, in it's default state it scans SSH usage, perhaps configure it to scan the Nginx 
access log as well).

TODO: it's best practice to close off any unused ports - look into that.

### Provisioning
I find that to run the fabfile from chapter 11, I need to:

- Manually add to the default Python 3.6 on the VM:

```
sudo apt install python3-pip python3-setuptools python3.6-venv
```

I haven't tested adding this to the fabfile instead, that would be a useful exercise when I created a new VM.

- Use dotenv to get Django to use the `.env` file. See the changes in commit #20c02d9.

Install Nginx:

```
$ sudo apt update && sudo apt install nginx
```
As per chapter 11, the manual steps on the VM to get Nginx and Gunicorn up and running are:

```
$ export SITENAME=superlists.example.com
$ cat /home/$USER/sites/$SITENAME/deploy_tools/nginx.template.conf \
    | sed "s/DOMAIN/"$SITENAME"/g;s/USER/"$USER"/g" \
    | sudo tee /etc/nginx/sites-available/$SITENAME

$ sudo ln -s /etc/nginx/sites-available/$SITENAME \
    /etc/nginx/sites-enabled/$SITENAME

$ cat /home/$USER/sites/$SITENAME/deploy_tools/gunicorn-systemd.template.service \
    | sed "s/DOMAIN/"$SITENAME"/g;s/USER/"$USER"/g" \
    | sudo tee /etc/systemd/system/gunicorn-$SITENAME.service

$ sudo systemctl daemon-reload
$ sudo systemctl reload nginx
$ sudo systemctl enable gunicorn-$SITENAME
$ sudo systemctl start gunicorn-$SITENAME
$ unset SITENAME
```

Note that I included `USER` in the Nginx and Gunciorn templates.

### Deploy new code
To deploy new code, I find that (ahead of chapter 17) besides running the fabfile I have to (on the server):

```
$ sudo systemctl restart gunicorn-superlists-staging.example.com
```
