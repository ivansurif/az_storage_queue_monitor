# Slack Toolbox [1.0]


This repository is a set of tools meant to showcase the use of Azure resources.


## [Slack] Stalker
This is an agnostic tool designed to monitor and process activity in messaging systems such as Slack, or any other messaging platform that offers an events API.

It leverages Azure Event Grid custom topics to receive message events, which are stored in Azure Queue Storage. From that point, an Azure Function takes on and processes the messages.

The repo does not get into Slack-specific API connection. It is a general purpose design which accepts a message payload in an Event Grid custom topic, queues it, and processes it.

Processing use cases could be many:
- alerting the user that a person of interest posted a message in a public channel.
- producing statistics about topics discussed and activity.
- analyzing messages using LLM to automatically propose updates to documentation, detecting hot topics and matters of interest to the user.

#### Data Object
The function expects a data object which stores and makes available to the function the configuration parameters necessary for it to run. The parameters are the below:

- queue_name: name of the Azure Queue to write to. The queue belongs to a Storage Account, is obtained from the `Connection String`, which needs to be made available as an env variable.

#### Environment Variables

- Connection String: String used to authenticate and authorize writing to a given message queue.

#### Azure Queue Storage message structure:
(it needs to store the original message, the name of the author and a link to the message in Slack)

#### Dynamics
- The function receives the name of the queue to write to as a parameter in the `data` object.
- It checks if the queue exists.