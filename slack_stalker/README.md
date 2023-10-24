# Slack Toolbox [1.0]


This repository is a set of tools meant leverage Azure features.


## Slack Stalker WIP
This tool is designed to alert the user of any new posts made by one or more persons of interest.

It leverages Slack Events API and Event Grid to react to messages posted on Slack.

It uses Azure Queue Storage to create and store a message that contains information about the posted file.

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
- If it doesn't, it attempts to create it.