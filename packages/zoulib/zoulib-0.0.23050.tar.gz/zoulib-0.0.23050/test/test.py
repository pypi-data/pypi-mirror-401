from zoulib import web_checker

browser = web_checker.Browser("https://github.com")

print("Title:", browser.get_title())
print("HTML первые 200 символов:", browser.get_html()[:200])
print("Инфо о сайте:", browser.get_info())

browser.type("#username", "мой_логин")
browser.type("#password", "мой_пароль")
browser.click("#submit")

browser.quit()
