# GCC_Agent
A General Computer Control Agent. This is a small project of mine to learn about AI agents and the various frameworks/languages used to build them. I greatly appreciate pull requests to fix any errors spotted.


## Features
- Browser control via Stagehand/ Playwright
- System level control (recommended to do so via the terminal commands)
- An isolated dockerized desktop environment
   - (Note: the agent still runs on your local computer, I just provide a container for the agent to execute its actions on. It is wholly possible for the agent to manipulate your local machine if you allow some imports like os)

## Some rough examples (Sped up to save time, tasks take a while in reality (to improve))
### 1) Computer agent uses the browser to answer queries. 
Example: Who is the author of the Neurips 2024 best paper? What is the controversy surrounding him?



https://github.com/user-attachments/assets/1a7e8c16-20ec-4957-96da-a41cb5e24654



### 2) Computer agent uses terminal to complete tasks
Example: Create a folder named "Hello world" in the Desktop. Afterwards delete it.



https://github.com/user-attachments/assets/75b01628-11a5-44a0-86a4-4ddbb37f2b05


## Multiagent architecture
```
                        +---------------------+
                        |     CodeAgent       |
                        |   (Manager Agent)   |
                        |     Python Code     |
                        +----------+----------+
                             |            |
             +---------------+            +---------------+
             |                                            |
             ▼                                            ▼
   +--------------------+                   +----------------------+
   | WebBrowser Agent   |                   | OS Control Agent     |
   | (outputs JSON)     |                   | (outputs JSON)       |
   +---------+----------+                   +----------+-----------+
             |                                         |
             ▼                                         ▼
   +--------------------+                   +----------------------+
   |   Browser API      |                   |   Operating System   |
   | (e.g. Chrome via   |                   |   Shell / System API |
   |    Stagehand, etc.)|                   |                      |
   +--------------------+                   +----------------------+
```

## Tools
View in agent/tools folder. Divided into Stagehand tools, Chromium tools, Firefox tools, Windows tools, additional tools.

## Made mainly with
- smolagents (Python)
- Stagehand (Typescript)
- Express (Javascript)
- Playwright (Python)
- Docker (Docker)

## FAQ
Q) How is the interface between Python code and Typescript/ Javascript tools implemented? <br/>
A) A controller Javascript/Typescript server is set up with Express where requests are POSTed   

# (TODO)
- Finish writing readme.
  - Write some documentation
- Add more browser control
- Add more general computer control
- Make GUI app better (low priority since gradio web server already exists)
## Setup 
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/GCC_Agent.git 
2. To build the container, open the terminal and run:
   ```docker-compose up --build``` <br/>
   To close the container, simply use ``` docker-compose down ```

3. To open the agent interface and run the agent, open a second terminal window and run ```python -m agent.computer_agent```
   
