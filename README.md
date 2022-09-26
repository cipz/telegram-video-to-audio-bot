# Telegram bot: YouTube to MP3 converter

Very simplistic implementation of a Telegram bot that, given a message containing a link to a YouTube video, it downloads the video and sends it back to the sender.

Given that the current implementation is not very scalable, the bot will only answer to the people whose chat ID contained in the `ALLOWED_CHAT_IDS` list.
Any messages coming from chats outside this list will be ignored.

This bot works in a `[pull](https://dev.to/anubhavitis/push-vs-pull-api-architecture-1djo)` architecture, querying the Telegram APIs every `10` seconds.

The `Dockerfile` contained in the repo will create an image that runs the `app.py` file.

Such solution is very simple and can be improved in many possible ways. It has been written with the purpose to serve only few clients and to work from inside a LAN, which is why it does not implement the use of webhooks and queries the Telegram APIs instead of listening for new incoming messages.
