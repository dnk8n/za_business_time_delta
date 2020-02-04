# ZA Business Time Delta

Note: Please see GitHub issues for outstanding bugs and features.

**Description:**
An API end point that will calculate the total number of South African business seconds between two ISO 8601 formatted
time strings.

**Brief:**
Provide an API end point that will calculate the total number of business seconds between two given times. A business
second is defined as any whole second that elapses after 08:00 and before 17:00 during a weekday (Monday - Friday) that
is not a public holiday in the Republic of South Africa. The end point must support only list GET requests and must take
two parameters: start_time and end_time. Parameter values will be in ISO-8601 format. You are guaranteed that start_time
will be before end_time. The end point must respond with only a single integer value for successful requests or a
suitable error message string for failed requests.

**Development installation steps:**
1. Clone this repo to a directory of your choosing
1. cd into the root of the checked out repo directory
1. Create and/or activate the Python 3.6 virtual environment you wish to use (Python 3.6 is supported because it aligns
   with the Python runtime supported by Now)
1. Run command: `pip install -r requirements.txt`

**Run development server**
1. cd into the root of the checked out repo directory
1. To run outside now framework, run command: `./runserver.sh`
1. Alternatively, run command: `now dev` ([Install and setup now if necessary](https://zeit.co/download))
   This will deploy to a non-production server at a private IP
1. Click on URL provided in terminal output

**Non-production deployment**
1. cd into the root of the checked out repo directory
1. Run command: `now` ([Install and setup now if necessary](https://zeit.co/download))
   This will deploy to a non-production server at an auto-generated public URL

**Production auto-deployment**
1. Never push to master directly (Todo: Disable this option)
1. Cut a new branch
1. Add your feature / bug-fixes
1. Run tests
1. Create a PR from new branch to master (Todo: tests should be run automatically at this stage)
1. Review PR and ensure tests pass
1. Merge to master (upon which automated deploy will proceed)

**Production deployment**
- Seldom necessary due to auto-deployments as changes are made to master branch. Only continue if you are sure you need to
1. cd into the root of the checked out repo directory
1. Run command: `now --prod` ([Install and setup now if necessary](https://zeit.co/download))
   This will deploy to a production server at the project's configured public URL (see now documentation on how to link to your own domain)

**Contributing to tests**
- Python's standard library, doctest is used. [Please view their documentation](https://docs.python.org/3.6/library/doctest.html)

**Run tests**
1. In activated Python 3.6 virtual environment, run command: `PYTHONPATH=$(pwd) ./tests/test_za_business_time_delta.py`

**API endpoints**

A helper form exists at: https://za-business-time.dnk8n.dev

Simply enter two ISO 8601 compliant time strings and submit.

The default example performs a GET request directly to the /time_delta endpoint, e.g

- https://za-business-time.dnk8n.dev/time_delta?start_time=2019-01-01T00%3A00%3A00&end_time=2021-01-01T00%3A00%3A00
where:
 - **https://za-business-time.dnk8n.dev** is the base URL
 - **/time_delta** is the endpoint that accepts GET requests
 - **start_time** is 2019-01-01T00%3A00%3A00
 - **end_time** is 2021-01-01T00%3A00%3A00
or without url codes:
- https://za-business-time.dnk8n.dev/time_delta?start_time=2019-01-01T00:00:00&end_time=2021-01-01T00:00:00
where similar to above but:
 - **start_time** is 2019-01-01T00:00:00
 - **end_time** is 2021-01-01T00:00:00


Other compatible ISO 8601 compliant formats are also accepted,

e.g.
https://za-business-time.dnk8n.dev/time_delta?start_time=1985-102T10:15Z&end_time=1985-103T10:15Z

and

https://za-business-time.dnk8n.dev/time_delta?start_time=1985-W15-5T10:15+04&end_time=1985-W15-5T10:11+03

An example of an error:
https://za-business-time.dnk8n.dev/time_delta?start_time=ERROR&end_time=ON_PURPOSE

If you just visit the URL directly without entering eny parameters, you also receive error:
https://za-business-time.dnk8n.dev/time_delta

To prevent time ranges of greater than 40,000 days (to protect server from becoming non-responsive due to excessive load due to sub-optimal algorithm).

e.g. for Error message: https://za-business-time.dnk8n.dev/time_delta?start_time=1890-6-25T00%3A00%3A00&end_time=2000-01-01T00%3A00%3A00

A reimplementation of core logic will make the above unnecessary
