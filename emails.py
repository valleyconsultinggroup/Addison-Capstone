import socket
import smtplib
import dns.resolver
import re

class Name():
    def __init__(self, name):
        self.first, self.last = name.lower().split(" ")
        self.first_initial = self.first[0]
        self.last_initial = self.last[0]

def check_email(addressToVerify):
    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', addressToVerify)

    if match == None:
        print('Bad Syntax')
        raise ValueError('Bad Syntax')

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

def main():
    # use rocketreach
    formatted_email = lambda n: [
        f'{n.first_initial}{n.last}@nvidia.com',
        f'{n.first}{n.last}@nvidia.com',
        f'{n.first}{n.last_initial}@nvidia.com'
    ]
    # names = ["Daniel Yang", "Dan Patel", "Ashley Chu", "Jennifer Jones", "Haig White", "Isabel Sarkis", "Julia Tyson"]
    # names = ["Craig Giraudo", "Bennett Yang", "Edwin Dong", "Ashley Jetson", "Shane Thrett", "Marilyn Ibanez", "Jessica Verley", "Vimu Rajdev", "Dayna Wu"]
    # names = ["Sandeep Tripathi", "Floyd Clark", "Sylvia Li", "Ajaypaul Singh", "Katherine Nguyen", "Lauren Silveira", "Tiffany Landayan", "Prashant Srivatsa"]
    for name in names:
        n = Name(name)
        for email in formatted_email(n):
            if check_email(email):
                print(email)

# main()
