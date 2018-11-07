import requests

COOKIE = "f0509de8fef13015511210cf155147fad683a3d916ac82b840ffe06d81c2acea"

def post_request(email):
    cookies = {
        'inar': COOKIE
    }

    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Origin': 'https://www.verifyemailaddress.org',
        'Upgrade-Insecure-Requests': '1',
        'DNT': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 11151.11.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.21 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'https://www.verifyemailaddress.org/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7',
    }

    data = {
      'email': email
    }

    response = requests.post('https://www.verifyemailaddress.org/', headers=headers, cookies=cookies, data=data)
    if response.status_code == 200:
        return(response.text)
    else:
        return None

class Name():
    def __init__(self, name):
        self.first, self.last = name.lower().split(" ")
        self.first_initial = self.first[0]
        self.last_initial = self.last[0]

def main():
    # use rocketreach
    formatted_email = lambda n: [f'{n.first_initial}{n.last}@nvidia.com',
                                 f'{n.first}{n.last}@nvidia.com',
                                 f'{n.first}{n.last_initial}@nvidia.com'
                                 ]

    # names = ["Daniel Yang", "Dan Patel", "Ashley Chu", "Jennifer Jones", "Haig White", "Isabel Sarkis", "Julia Tyson"]
    # names = ["Craig Giraudo", "Bennett Yang", "Edwin Dong", "Ashley Jetson", "Shane Thrett", "Marilyn Ibanez", "Jessica Verley", "Vimu Rajdev", "Dayna Wu"]
    names = ["Shahid Khan", "Carol Stanford", "Landon Allen", "Crystal Aggarwal", "Bella Yanovsky"," Sandeep Tripathi", "Floyd Clark - SPHR", "Sylvia Li", "Ajaypaul Singh", "Katherine Nguyen", "Lauren Silveira", "Tiffany Landayan", "Prashant Srivatsa", "Hanson zhang(hansonz@nvidia.com)"]
    for name in names:
        n = Name(name)
        for email in formatted_email(n):
            response = post_request(email)
            if f'<span>{email}</span> is valid' in response:
                print(email)

main()
