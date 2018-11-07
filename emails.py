import socket
import smtplib
import dns.resolver
import re
import os

class Name():
    def __init__(self, name):
        name_parts = name.lower().split(" ")
        if len(name_parts) == 2:
            self.first, self.last = name_parts
        elif len(name_parts) == 3:
            self.first, self.last = name_parts[0], name_parts[2]
        else:
            self.first = ""
            self.last = ""
        self.first_initial = self.first[0:1]
        self.last_initial = self.last[0:1]

def check_email(addressToVerify):
    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', addressToVerify)

    if match == None:
        print('Bad Syntax', addressToVerify)

    index = addressToVerify.find("@")
    domain = addressToVerify[index+1:]
    records = dns.resolver.query(domain, 'MX')
    mxRecord = records[0].exchange
    mxRecord = str(mxRecord)

    # Get local server hostname
    host = socket.gethostname()

    # SMTP lib setup (use debug level for full output)
    server = smtplib.SMTP()
    server.set_debuglevel(0)

    # SMTP Conversation
    server.connect(mxRecord)
    server.helo(host)
    server.mail('me@domain.com')
    code, message = server.rcpt(str(addressToVerify))
    server.quit()

    # Assume 250 as Success
    if code == 250:
        return True
    else:
        return False

def get_emails_from_folder(folder_name):
    """
    Returns names of files in a folder
    mapping: company name (str) -> list of names ([str])
    """
    files = os.listdir(folder_name)
    company_to_file = {}
    for file in files:
        file_parts = file.rsplit(".", 1)
        if len(file_parts) != 2:
            continue
        filename, extension = file_parts
        if extension != "mhtml":
            continue
        company, number = file.split("_")
        company_files = company_to_file.get(company, [])
        company_to_file[company] = company_files + [file]
    return company_to_file

def get_formats_from_folder(folder_name):
    """
    Returns names of files in a folder
    mapping: company name (str) -> filename (str)
    """
    files = os.listdir(folder_name)
    company_to_file = {}
    for file in files:
        file_parts = file.rsplit(".", 1)
        if len(file_parts) != 2:
            continue
        filename, extension = file_parts
        if extension != "mhtml":
            continue
        company_to_file[filename] = file
    return company_to_file

def email_file_to_names(filename):
    """
    Returns names from a linkedin page
    """
    with open(filename) as f:
        return re.findall('actor-name">([a-zA-z ]*)<', f.read())

def format_file_to_formats(filename):
    """
    Returns top 3 email formats of a company given the file
    """
    with open(filename) as f:
        results = re.findall('ng-binding">([^@%\n]*)<', f.read())
        print(results)
        return results[2:]

def construct_email_formats(formats, domain):
    def formatted_email(n):
        email_styles = []
        for email_format in formats:
            parts = email_format.split(" ")
            if len(parts) == 3 and parts[1] in ["'_'", "'.'", "'-'"]:
                first_part, middle_part, second_part = parts
                middle_part = middle_part.strip("'")
            elif len(parts) == 2:
                first_part, second_part = parts
                middle_part = ""
            elif len(parts) == 1:
                first_part = parts[0]
                middle_part = ""
                second_part = ""
            else:
                print(email_format)
                continue
            email_style = '{first_part}{middle_part}{second_part}@{domain}'.format(
                first_part=getattr(n, first_part, ""),
                middle_part=middle_part,
                second_part=getattr(n, second_part, ""),
                domain=domain,
            )
            email_styles.append(email_style)
        return email_styles
    return formatted_email

def main():
    emails_folder = "linkedin"
    formats_folder = "rocketreach"
    emailfiles = get_emails_from_folder(emails_folder)
    formatfiles = get_formats_from_folder(formats_folder)
    possible_emails = []
    for domain, files in emailfiles.items():
        # check for catch-all domains
        if check_email(f'asdfasdfasdfadsfasdfasdf@{domain}'):
            print(f'{domain} has a catch all, so we cannot get emails')
            continue
        names = []
        for file in files:
            names += email_file_to_names(emails_folder + "/" + file)
        formats = format_file_to_formats(f'{formats_folder}/{domain}.mhtml')
        formatted_email = construct_email_formats(formats, domain)
        for name in names:
            if "linkedin" in name.lower():
                continue
            possible_emails += formatted_email(Name(name))
    print(possible_emails)
    working_emails = []
    try:
        for email in possible_emails:
            if check_email(email):
                print(email)
                working_emails.append(email)
    except KeyboardInterrupt:
        print(working_emails)
    return

main()
