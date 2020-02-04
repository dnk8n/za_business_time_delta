# ZA Business Time Delta

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
   This will deploy to a non-production server at an auto-generated private URL
1. Click on URL provided in terminal output

**Non-production deployment**
1. cd into the root of the checked out repo directory
1. Run command: `now` ([Install and setup now if necessary](https://zeit.co/download))
   This will deploy to a non-production server at an auto-generated public URL

**Production auto-deployment**
1. Never push to master directly
1. Cut a new branch
1. Add your feature / bug-fixes
1. Run tests
1. Create a PR from new branch to master (Todo: tests should be run automatically at this stage)
1. Review PR and ensure tests pass
1. Merge to master (upon which automated deploy will proceed)

**Production deployment**
Seldom necessary due to auto-deployments as changes are made to master branch. Only continue if you are sure you need to
1. cd into the root of the checked out repo directory
1. Run command: `now --prod` ([Install and setup now if necessary](https://zeit.co/download))
   This will deploy to a production server at the project's configured public URL (see now documentation on how to link to your own domain)

**Contributing to tests**
1. Python's standard library, doctest is used. [Please view their documentation](https://docs.python.org/3.6/library/doctest.html)
