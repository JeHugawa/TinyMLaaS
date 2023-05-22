# Client meeting 15.5.2023

## Communication
	- Discord
	- Roberto will be the main contact person

## Overview
	- TinyML on IoT devices that are very resource constrained
	- Seamless (fully automated) lifecyce management
	- Models are trained on the cloud and customized to fit on client device
	- Inference is done on the local device
	- Edge computing is dependent on connectivity, TinyML is not 

## Tech stack and its situation
	- nbdev (generates code and documentation from Jupyter Notebooks)
	- Streamlit (UI)
	- Tensorflow and Tensorflow Lite (machine learning)
	- Python (pandas, sklearn etc.)
	- Github Actions (CI/CD)
	- Acceptance Test Driven Development (Robot Framework)
	- Currently the app runs locally, not set up for cloud
	- Docker / Docker Compose (FaaS, Function as a Service)
	- Modularity -> one container for one purpose

## Goals for this project run
	- Separate UI and backend (REST), FastAPI? OpenAPI?
	- CLI tool for UI
	- Up for discussion: TBD for Sprint 1

## Ideas for further development
	- Better web UI
	- Fuller automation for backend
	- Allow integration to existing frontends for potential client organizations
	- Another Microcontroller client

- See https://origami-tinyml.github.io/tflm_hello_world/docs/software-project-summer-kick-off.html

- Next meeting
	- Monday 22nd, 10:00 with Roberto

## AP
- Get organized
- Get acquainted with project
- Propose WoW
- What kind of support do we need?
