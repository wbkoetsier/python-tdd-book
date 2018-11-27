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
`python manage.py test functional_tests`

`python manage.py test lists`

## Staging server
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

- Go to hamburger menu -> Compute Engine. Click Create (blue button).
- Name: I'm using the default name.
- Region/Zone: the default S-Carolina offers the f1-micro instance that is within the always free limits.
- For always free, change the Machine type to f1 micro. It should be enough for trying the ToDo-app.
- At this point, no container image.
- Boot disk: 
  - OS image: the Ubuntu 18.04 will do. The [minimal](https://wiki.ubuntu.com/Minimal) is more suitable for a fully 
  automated deployment where cli usage isn't really needed.
  - Always free includes a standard persistant disk (as opposed to SSD) with 30 GB-months storage (30 GB 
  stored for one month). Some storage room is needed for the database but Ubuntu Server isn't that big. I'm going with 
  20GB.
- Google IAM is actually quite complex. A server requires a 
[service account](https://cloud.google.com/compute/docs/access/service-accounts#the_default_service_account) when 
connecting to Google APIs, such as Storage or Stack Driver. I'd like to see if I can use stackdriver for logging so I'll 
select the default access service account.
- For the staging site, allow HTTP traffic.
- Ignore "Management, security, disks, networking, sole tenancy".

TODO - use gcloud to create an instance

- https://cloud.google.com/sdk/gcloud/reference/compute/
- https://cloud.google.com/sdk/docs/quickstart-debian-ubuntu

### Accessing the server
The Compute Engine menu on the left has an item 'VM instances'. Click the 'SSH'-button next to the created instance. 
This will open a console in the browser (new window), with the user logged in and at `~`. Accessing the server using a 
different SSH client requires additional setup., which I haven't tried.

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
different one than configured now. That would mean also changing the IP address in the registrar. To request a static 
IP (takes imediate effect), go to the hamburger menu -> VPC Network -> External IP addresses, and change the type of the 
IP address in use by the VM instance.

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
[an article](https://plusbryan.com/my-first-5-minutes-on-a-server-or-essential-security-for-linux-servers), but these 2 
things:
- Edit the SSH conf to disable root login (also, _Never_ set a root password on Ubuntu)
- Install fail2ban (at the very least, in it's default state it scans SSH usage, perhaps configure it to scan the Nginx 
access log as well)

TODO: it's best practice to close off any unused ports - look into that.
