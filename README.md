# 🤖 AmiLab Discord Bot

A powerful Discord bot that integrates with the **Ambient Laboratory of UAM (AmiLab) API** to provide real-time information from available IoT devices. Built with **YOLOv11**, this bot is designed to allow users to request access to the AmiLab laboratory for a specfic number of people, triggering responses depending on the current state of the room.

---

## 🚀 Features

- **Snapshot Retrieval**: Capture real-time snapshots from the AmiLab camera.
- **People Detection**: Use YOLOv11 to count the number of people in a room.
- **Smart Automation**: Request access for a specific number of people.
- **API Interaction**: Interact directly with the API using Discord messages.

---

## 🛠️ Commands

| Command                  | Description                                                                                     |
|--------------------------|-------------------------------------------------------------------------------------------------|
| `+help`                 | Displays a list of available commands.                                                         |
| `+snapshot`             | Sends a snapshot from the AmiLab camera.                                                       |
| `+get_state <entity_id>`| Retrieves the state of a specified entity.                                                     |
| `+post_service <...>`   | Sends a service command to control an entity.                                                  |
| `+count_people`         | Counts the number of people in the AmiLab camera image and shares the annotated image.         |
| `+request_access_to <n>`| Requests access for a specific number of people and automates smart device responses.          |
| `+mock`                 | Toggles mock mode for testing purposes.                                                        |

---

## 🏗️ Project Structure
```
src/
├── AmiLab/
│   └── AmiLab.py          # Encapsulates HTTP requests to the AmiLab API
├── Bot/
│   └── DiscordBot.py      # Implements the Discord bot functionality
├── Model/
│   ├── YoloModel.py       # YOLOv11-based people detection model
│   └── utils/
│       └── yolo_test.py   # YOLO model testing script
└── main.py                # Entry point for the bot
utils/
└── mock.jpg               # Mock image for testing
```

## 🛠️ Setup and Installation

### Prerequisites

- Python 3.10+
- Docker (optional, for containerized deployment)

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/oigresgar/IOT_Project.git
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Set up your `.env` file:
    ```
    DISCORD_TOKEN=your_discord_bot_token
    AMI_LAB_URL=https://url-to-api
    AMI_LAB_TOKEN=api-token
    ```
4. Run the bot:
    ```bash
    python src/main.py
    ```

## 🐋 Docker
The project also contains a Dockerfile ready to containarize your own bot simply by using:
```bash
docker build --tag amilabbot .
docker run amilabbot
```

## ✍️ Created by Sergio Garea and Enrique Ortega for the IoT subject, Master's Degree in Computer Engineering
