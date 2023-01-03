# Roboswag

- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Limitations](#limitations)

## Introduction

:robot: Roboswag is a tool that automatically generates Python libraries out of your Swagger (OpenAPI specification
file). These libraries can be used to create tests with various payload content and its validation. It also supports
response validation against schema and verification of different status codes.

> **Note**
>
> The tool is in the ***Alpha*** state, which means it may be unstable and should be used at your own risk. Some
> features may be broken and there are still many things to be developed. Happy testing!

The OpenAPI Specification (OAS) defines a standard, language-agnostic interface to RESTful APIs.
Click [here for v3 documentation](https://swagger.io/specification/) and
[here for v2 documentation](https://swagger.io/specification/v2).

> Hosted on [GitHub](https://github.com/MarketSquare/roboswag). :medal_military:

## Installation

You can install Roboswag simply by running::

    pip install roboswag

## Usage

Roboswag can be easily run from command line. To check if it's installed, run this to see the current version:

```commandline
roboswag --version
```

To execute Roboswag with its full capabilities, run it with provided path to the Swagger (OpenAPI specification) file:

```commandline
roboswag generate -s <path_to_swagger>
```

> You can try out the tool using the example of a swagger file (OAS 2.0) located in `swaggers/petstore_swagger.json` and an openapi files (OAS 3.x) located in `swaggers/petstore_openapi.json`

Successful execution should result in printing the information about generated files and a whole new directory (named
by the value of `info.title` from your Swagger file) consisting of:
- `endpoints` directory with files representing each `tag` as a class with methods representing its endpoints,
- `models` directory with API models represented as Python classes,
- `schemas` directory with every possible schema from your API as JSON file used for validating payload and responses.

Now you can just create a test file, import desired endpoint and start automating the testing!

## Limitations

The tool is already able to generate libraries but...
- Not all fields from the swagger specification may be supported. This means that a specific file may break the tool
  and flood the terminal with stack trace (we will be really grateful to receive bug issues in our Github project!)
- Authorization to access the API is not yet fully covered
- There is not much to be configured here - it always works the same
- There is no real documentation apart from this file

Please be forgiving and submit an issue, if you struggle with something or just contact us on our
[Slack channel](https://robotframework.slack.com/archives/C035KMZ2FGA). It's more than welcome also to support us by
code contribution! :keyboard:
