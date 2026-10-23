import asyncio, os
from playwright.async_api import async_playwright

headless = True
chrome = headless
url = "https://gemini.google.com/app"

box = "rich-textarea div.ql-editor, div[contenteditable='true'][role='textbox']"
send = "button[aria-label='Send message'], button.send-button"
stop = "button[aria-label='Stop response'], button[aria-label='Stop generating']"
reply = "model-response message-content, message-content"


async def finish(page, limit=120):
    button = page.locator(stop).first

    try:
        await button.wait_for(state="visible", timeout=10000)
        await button.wait_for(state="detached", timeout=limit * 1000)
        await page.wait_for_timeout(800)
        return
    except Exception:
        pass

    last = ""
    ticks = 0
    for tick in range(limit * 2):
        await page.wait_for_timeout(500)
        texts = await page.locator(reply).all_text_contents()
        current = texts[-1].strip() if texts else ""
        if current and current == last:
            ticks += 1
            if ticks >= 4:
                return
        else:
            ticks = 0
            last = current


async def main():
    folder = os.path.abspath("./profile")
    os.makedirs(folder, exist_ok=True)

    async with async_playwright() as play:
        options = dict(
            user_data_dir=folder,
            headless=headless,
            viewport={"width": 1280, "height": 800},
            args=["--disable-blink-features=AutomationControlled"],
            ignore_default_args=["--enable-automation"],
        )
        if chrome:
            options["channel"] = "chrome"

        try:
            context = await play.chromium.launch_persistent_context(**options)
        except Exception:
            if chrome:
                options.pop("channel", None)
                context = await play.chromium.launch_persistent_context(**options)
            else:
                raise

        page = context.pages[0] if context.pages else await context.new_page()

        await page.goto(url, wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)

        if not headless:
            print("\n[*] If you aren't logged in, log in now in the browser window.")
            input("[*] Press Enter here once you can see the chat box... ")

        try:
            await page.locator(box).first.wait_for(state="visible", timeout=15000)
        except Exception:
            print("\n[!] Couldn't find the chat box. You're probably not logged in,")
            print("[!] or the page is showing a bot check, consent screen, or popup.")
            print("[!] To log in: set headless = False at the top of the script.")
            await context.close()
            return

        while True:
            try:
                prompt = input("You: ").strip()
                if not prompt:
                    continue
                if prompt.lower() in ["exit", "quit"]:
                    print("Exiting...")
                    break

                before = await page.locator(reply).count()

                field = page.locator(box).first
                await field.wait_for(state="visible", timeout=5000)
                await field.click()
                await field.fill(prompt)
                await page.wait_for_timeout(500)

                button = page.locator(send).first
                if await button.is_visible():
                    await button.click()
                else:
                    await page.keyboard.press("Enter")

                print("Gemini is thinking...", end="\r")

                for tick in range(40):
                    if await page.locator(reply).count() > before:
                        break
                    await page.wait_for_timeout(500)

                await finish(page)

                texts = await page.locator(reply).all_text_contents()
                if texts:
                    latest = texts[-1].strip()
                    print(" " * 30, end="\r")
                    print(f"\nGemini: {latest}\n")
                else:
                    print("\nGemini: [Response received, but couldn't parse text directly]\n")

            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as error:
                print(f"\n[!] Error during interaction: {error}\n")

        await context.close()


if __name__ == "__main__":
    asyncio.run(main())
