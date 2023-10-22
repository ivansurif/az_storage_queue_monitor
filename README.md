# Slack Toolbox [1.0]


This repository is a set of tools meant to customize and enhance the Slack user experience.

It is meant to be deployed as Cognite Functions.

## Slack Stalker WIP
This tool is meant to alert the user of any messages posted by one or more persons in his slack account.

It leverages Azure Queue Storage to keep a copy of the messages posted by the targeted individual(s).

Messages are written to the Azure Storage Queue. Only the new version of a message is written. If a message is posted and then edited, only the original version is stored in Azure Storage.

#### Azure Queue Storage message structure:
(it needs to store the original message, the name of the author and a link to the message in Slack)

#### Dynamic
The function receives the name of the queue to write to as a parameter in the `data` object. The `Storage Account` name is obtained from the `Connection String`, which needs to be made available as an env variable.