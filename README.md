# HTTP C2-Server
## Overview

#### This is a POC C2 Server project for my personal experience and knowledge to deepen my understanding of the Command and Control Framework

This C2 involves 3 parts, the Teamserver, Client (Agent Handler), and Agent. However, this was developed without any opsec and stealth in mind, it is purely for my understanding and knowledge (plz don't roast the code/architecture)

Straightforward setup process:
1. Run teamserver.py
2. Run agent.py on a remote machine
3. Run client.py

Currently, the commands of the C2 Server involves only the very core functionalities that you may find in every C2 server.

## Just to briefly go through how data will be read/stored when using the C2:

Once the setup is complete, you can start using the Client to send tasks for the agent to execute. For example, let's say you send a "ls | grep txt" over to the agent, it will be stored as `tasks.json` first, and once executed, the `tasks.json` file will be deleted, results will be returned and stored as `results.json` for viewing in `/data/agents/<agent_name>`. You can use `view_results <agent_name>` to view the latest results yielded by a specific agent.

Everytime a task is executed / new result is yielded, the `results.json` file will be updated with only the latest information to prevent cluttering (WIP, I will try to update it so that the data stored will be organized neatly, making life a lot easier when documenting down gathered information).

So now, how do I kill an agent / what happens when I kill an agent?
1. To kill an agent, simply do `send_task <agent_name> command terminate`
2. When you kill an agent, the agent.py process on the `remote machine` will be killed, stopping all communication between the `remote machine` and the C2 server. After that, a message will be sent back to the Teamserver, telling the Teamserver that the agent has been successfully terminated and the respective agent's folder will be automatically removed.

# Commands

You may enter `help` to view all commands

![image](https://github.com/yuuuu7/C2-Server/assets/107798032/1feaa9e9-4e12-4282-95c6-1933f6e9d275)

You can also enter `help <topic>` to view the usage of the respective commands

![image](https://github.com/yuuuu7/C2-Server/assets/107798032/516a3b1f-a385-40fb-a692-91dd282a1eb8)

# Detection

![image](https://github.com/yuuuu7/C2-Server/assets/107798032/fd81f4f7-29c6-4a8b-835c-2285506db4a9)

No evasion was done





