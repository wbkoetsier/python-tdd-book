# Test-driven development with Python
Following the book in print (5th edition) and [online](https://www.obeythetestinggoat.com/).

## Requirements
Python: 3.6+

`pip freeze`:
```
Django==1.11.16
pkg-resources==0.0.0
pytz==2018.7
selenium==3.141.0
urllib3==1.24.1
```

Geckodriver: 0.23.0 (anywhere on the path) with Firefox 63.0. Or visit https://github.com/mozilla/geckodriver/releases.

[(Vanilla) Bootstrap 3.3.4](https://github.com/twbs/bootstrap/releases/download/v3.3.4/bootstrap-3.3.4-dist.zip).

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

### Creating a server using the web interface
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

### Creating a server using cli
TODO - use gcloud to create an instance
 
The interface allows a preview of the REST or cli equivalent of the above choices. Actually, using 
[`gcloud`](https://cloud.google.com/sdk/gcloud/reference/compute/) is a very good alternative to using the web 
interface. I installed gcloud using [this quickstart](https://cloud.google.com/sdk/docs/quickstart-debian-ubuntu). The 
automatically generated gcloud command line (I've replaced my project and instance names with a placeholder):

```bash
gcloud beta compute --project=<project ID> instances create <instance name> 
  --zone=us-east1-b 
  --machine-type=f1-micro 
  --subnet=default 
  --network-tier=PREMIUM 
  --maintenance-policy=MIGRATE 
  --no-service-account 
  --no-scopes 
  --tags=http-server 
  --image=ubuntu-1804-bionic-v20181120 
  --image-project=ubuntu-os-cloud 
  --boot-disk-size=20GB 
  --boot-disk-type=pd-standard 
  --boot-disk-device-name=instance-1

gcloud compute --project=<project ID> firewall-rules create default-allow-http 
  --direction=INGRESS 
  --priority=1000 
  --network=default 
  --action=ALLOW 
  --rules=tcp:80 
  --source-ranges=0.0.0.0/0 
  --target-tags=http-server
```

### Accessing the server
The Compute Engine menu on the left has an item 'VM instances'. Click the 'SSH'-button next to the created instance. 
This will open a console in the browser (new window). The server is ready to pick up chapter 9 of the course.

