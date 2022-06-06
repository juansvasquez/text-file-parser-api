# text-file-parser-api
An application to parse text files and expose an HTTP API to serve the files.

The Microsoft tutorial for Docker in Visual Studio Code was invaluable for me to learn how
to use Docker with Flask and Python: https://docs.microsoft.com/en-us/visualstudio/docker/tutorials/docker-tutorial

The general path my project took was:
-First, I created a simple API to accept JSON via POST requests
-I then expanded this to return JSON, adding checks for some base/edge cases.
-Next I created a function to create the body JSON we would eventually be returning
-Inside this function I made sure to validate that the filenames being passed existed
    as well as making sure the dates were in the correct format
-Finally I made sure to keep in mind writing the application with constant 
    memory consumption regardless of file size. We run through the file line by line, instead
    of consuming the entire file at once.

Things I could have done better/expand upon if I wanted to upgrade the project:

-Better error handling, such as in case the POST JSON has more keys than the required filename/from/to
-Checking that the ISO date can exist eg february 29th
-Accounting for ISO date + timezones
-There's always more edge cases I didn't think of!


## Overview

A company has a business process that requires processing of text files from external
customers. Some information about the text file:

- Each line of the text file is an individual record and can be processed independently of the other records in the text file
- The size of the file can range from a few KB to a few GB
- The file will be ordered by iso8601 time ascending

Here is the format of each line:

```
[Date in YYYY-MM-DDThh:mm:ssZ Format][space][Email Address][space][Session Id in GUID format]
```

For example:

```
2020-12-04T11:14:23Z jane.doe@email.com 2f31eb2c-a735-4c91-a122-b3851bc87355
```

## Requirements

Please write an application to parse the text files above and expose an HTTP API to serve the files.

### Input

The application *must* follow the following standard *exactly*.

 - The program must run on port 8279
 - The program must expose an HTTP POST route on the `/` path
 - The from/to options must support iso8601 UTC timestamps *only*
 - The program must accept the POST body as defined below
 - The files must be loaded from `/app/test-files`

```bash
curl -XPOST -d '{"filename":"sample1.txt", "from":"2020-07-06T23:00:00Z", "to": "2022-07-066T23:00:00Z"}' -H 'Content-Type: application/json' localhost:8279/
```

### Output

Your output must be parsed entries within the date time range *inclusively*, in JSON
format.

A successful response should return content-type `application/json`, an HTTP status
code of 200, and a response body of the following format:

```JSON
[
  {
    "eventTime":"2000-01-01T03:05:58Z",
    "email":"test123@test.com",
    "sessionId":"97994694-ea5c-4da7-a4bb-d6423321ccd0"
  },
  {
    "eventTime":"2000-01-01T04:05:58Z",
    "email":"test456@test.com",
    "sessionId":"97994694-ea5c-4da7-a4bb-d6423321ccd1"
  }
]
```
- The array *must* be ordered by eventTime from earliest to latest
- The ordering of the keys within the JSON objects does not matter

If the input is invalid, or there are no valid entries, your application should return
a 200 HTTP status response code, a content-type of `application/json`, and the following
response body:

```JSON
[]
```

### Building and Running the Application

Included in this project is a `Dockerfile`, a `build.sh`, and a `run.sh`.

The test harness will call these scripts from their current location (`./scripts`).
_Do not move them and ensure they remain executable._

The application will start an HTTP server on port 8279.
The `run.sh` script will expose this on the host machine.

Each script will be run once in order.

The first argument to `run.sh` will always be the absolute path of the folder containing
the test files on the host machine. This folder will be mounted into your container.
Files in this folder will be past to your program _by filename only_.

The `run.sh` script mounts the given filepath onto `/app/test-files`. This folder must exist
for the mount to work.
