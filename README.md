# geminal
Chat with Gemini from your terminal NO API KEY

geminal is a tiny Python script that drives your own logged-in Gemini session with [Playwright](https://playwright.dev/python/) and turns it into a command-line chat. Type a prompt, get a reply, never leave the terminal.

```
You: explain recursion in one sentence

Gemini: Recursion is when a function solves a problem by calling itself on smaller versions of that problem until it reaches a simple base case.

You:
```

## Features

- Chat with Gemini straight from your terminal
- No API key, uses your own Google account session
- Login is saved, so you only sign in once
- Runs headless in the background, or visible if you want to watch
- Waits for the full reply instead of cutting it off
- Single file, about 130 lines, easy to read and modify

## Install

Requires Python 3.9+.

```bash
git clone https://github.com/cherycoke/geminal.git
cd geminal
pip install playwright
playwright install chromium
```

## Usage

**First run (log in once):**

1. Open `main.py` and set `headless = False`
2. Run it:

```bash
python main.py
```

3. Log in to your Google account in the window that opens
4. Press Enter in the terminal when you can see the chat box

**After that:** set `headless = True` and run it again. Your login is stored in the `browser_profile_gemini` folder.

Type `exit` or `quit` to close.

## Settings

Edit these at the top of `main.py`:

| Setting    | Default | What it does                                      |
| ---------- | ------- | ------------------------------------------------- |
| `headless` | `True`  | Hide the browser window. Use `False` to log in.   |
| `chrome`   | `True`  | Use your installed Chrome, falls back to Chromium |
| `url`      | Gemini  | The page to open                                  |

## Troubleshooting

**"Couldn't find the chat box"**
You're probably not logged in, or Google is showing a bot check. Set `headless = False`, log in manually, and try again.

**Google says "This browser or app may not be secure"**
Install regular Google Chrome and keep `chrome = True`. Google sometimes blocks sign-in in automated browsers.

**It stopped working after a Gemini update**
Gemini's page layout changes often. Open Gemini, right-click the element that's failing, choose Inspect, and update the matching selector (`box`, `send`, `stop`, `reply`) at the top of `main.py`.

## Limitations

- It depends on Gemini's web page layout, so it can break whenever Google changes the site
- Replies are slower than the official API because everything goes through a real browser
- One conversation at a time
- Not suitable for production, multi-user apps, or heavy automation

## Disclaimer

This project is not affiliated with or endorsed by Google. It automates the Gemini web interface, which may go against Google's Terms of Service. Use it for personal, light use at your own risk, and your account could be rate-limited or restricted. If you're building something real, use the official [Gemini API](https://ai.google.dev/) instead.

## Contributing

Issues and pull requests are welcome, especially updated selectors when the Gemini UI changes.

## License

MIT
