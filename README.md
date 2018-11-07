# Email Sourcing Script

Author: Addison Chan

Github Username: addcninblue

Landing site: i'll make this available as a web app later on

### Usage

Use Linkedin for names

Use rocketreach.co for email formats

main file: `emails.py`

### Revision History

| Date        | Comments      | Author    |
| ----------- | ------------- | --------- |
| 11/07/2018  | Initial Draft | Addison Chan |

### Overview / Purpose

Sourcing emails is a pain. There's a set routine of finding people's names and trying to match their name to their company email format.

This script hopes to change that. It automates the most tedious parts of it, allowing people to automate sourcing emails, focusing on being as accurate as fast as possible

### Work Requirements

| # | Description   | Hours Estimated | Completion Date | Miscellaneous |
| - | ------------- | --------------- | --------------- | ------------- |
| 1 | Analyzing tools available for webscraping / email server pinging | 1 Hour | 11/01/2018 |  |
| 2 | Create basic functionality with manual/hard-coded emails + email server pinging api hack | 1 Hour | 11/01/2018 | |
| 3 | Create basic functionality with hard-coded emails + automated server pinging | 1 Hours | 11/01/2018 |  |
| 4 | Create functionality with scraping emails from saved websites | 2 Hours | |  |
| 5 | Create functionality with converting email formats from website format | 1 Hour | |  |
| 6 | Create frontend/website for scraping emails | 4 Hours | |  |
| 7 | Use Selenium to automate scraping | ? Hours | | Looking to implement in the future / after dev |

### Technical Stack

This script essentially is self-contained. It takes in a list of emails, a list of potential email formats, and it will brute force all possible emails against an email server until it returns a 250 (working) response. It takes advantage of the `socket`, `smtplib`, `dns.resolver`, and `re` modules.
