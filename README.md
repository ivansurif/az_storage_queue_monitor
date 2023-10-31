# Azure Storage Queue Monitor
This repo is intended to showcase the use of Azure Storage SDK in conjunction with an external app, a [CDF Function](https://docs.cognite.com/cdf/functions/). Azure Storage Queue messages are extracted by the CDF Function for processing.

Processing use cases could be many, particularly if used together with an IaC repo that creates the data pipelines in Azure, such as [this one](https://github.com/ivansurif/azure-terraform-data-pipeline). For example:
- alerting the user that a person of interest posted a message in a public channel.
- producing statistics about topics discussed and activity.
- analyzing messages using LLM to automatically propose updates to documentation, detecting hot topics and matters of interest to the user.

#### Data Object
The function expects a data object which stores and makes available to the function the configuration parameters necessary for it to run. The parameters are the below:

- queue_name: name of the Azure Queue to read from. The queue belongs to a Storage Account, is obtained from the `Connection String`, which needs to be made available as an env variable.

#### Environment Variables

- Connection String: String used to authenticate and authorize writing to a given message queue.

#### Azure Queue Storage message structure:
Not defined or enforced.

#### Dynamics
- The function receives the name of the queue to write to as a parameter in the `data` object.
- It checks if the queue exists.