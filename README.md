# Telegram Bot for Notification Formulas

## Features
- Users can select a notification frequency: **Yearly, Twice a Year, Quarterly, or Monthly**.
- The bot calculates and provides an Excel formula based on user input.
- Uses **pyTelegramBotAPI** to interact with Telegram.
- Logs actions to the console.

## Installation
### Prerequisites
- Python 3.8+
- Telegram bot token (get it from [BotFather](https://t.me/BotFather))

### Setup
```sh
# Clone the repository
git clone https://github.com/your-username/your-repo.git
cd your-repo

# Install dependencies
pip install -r requirements.txt

# Set your Telegram bot token as an environment variable
export TELEGRAM_BOT_TOKEN=your_token_here  # Linux/macOS
set TELEGRAM_BOT_TOKEN=your_token_here  # Windows
```

## Running the Bot
```sh
python bot.py
```
The bot will continuously run and respond to messages in Telegram.

## Deployment to Railway.app
1. Push your code to a **GitHub repository**.
2. Create a new project on [Railway.app](https://railway.app/).
3. Deploy your GitHub repository.
4. Add an environment variable:
   ```sh
   # Add your bot token in Railway
   TELEGRAM_BOT_TOKEN=your_token_here
   ```
5. Add a file named Procfile in the root of the project with the following content:
   ```sh
   # Procfile
   worker: python bot.py
   ```
This tells Railway how to start your bot.
6. Deploy the project, and your bot will run 24/7!

## Logging
The bot logs all actions to the **console**, which can be viewed in Railway's **Logs tab**.

## Example Usage
1. Start the bot by sending `/start`.
2. Select **Get formula**.
3. Choose the frequency, month, and day.
4. The bot calculates and sends an Excel formula.

## Technologies Used
- **Python** (3.8+)
- **pyTelegramBotAPI** (for Telegram bot)
- **Logging module** (for monitoring actions)

## Contributing
Feel free to submit pull requests or report issues!

## License
This project is open-source and available under the **MIT License**.
