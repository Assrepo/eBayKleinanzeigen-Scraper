# ░█████╗░░█████╗░███╗░░██╗███████╗██╗░██████╗░
# ██╔══██╗██╔══██╗████╗░██║██╔════╝██║██╔════╝░
# ██║░░╚═╝██║░░██║██╔██╗██║█████╗░░██║██║░░██╗░
# ██║░░██╗██║░░██║██║╚████║██╔══╝░░██║██║░░╚██╗
# ╚█████╔╝╚█████╔╝██║░╚███║██║░░░░░██║╚██████╔╝
# ░╚════╝░░╚════╝░╚═╝░░╚══╝╚═╝░░░░░╚═╝░╚═════╝░

# Your Gmail credentials (The scraper uses to send the E-Mail)
# You need to 'Allow less secure apps to access your account' in order to automatically send emails, see below:
# https://support.google.com/accounts/answer/6010255
# If you are getting an SMTPAuthenticationError with an error code of 534 try this step:
# https://accounts.google.com/DisplayUnlockCaptcha
EMAIL_ADDRESS = 'your_scraper@gmail.com'
PASSWORD = 'password'

# Your email address, the offers get send to
YOUR_EMAIL = 'your@email.com'

# Fill in your location
LOCATION = "Dresden"

# Interval to check new offers in hours
INTERVAL = 4

# Detailed text output of why offers are rejected (Intended for @Varsius)
DEBUG = False

# ░░░░░██╗░█████╗░██████╗░░██████╗
# ░░░░░██║██╔══██╗██╔══██╗██╔════╝
# ░░░░░██║██║░░██║██████╦╝╚█████╗░
# ██╗░░██║██║░░██║██╔══██╗░╚═══██╗
# ╚█████╔╝╚█████╔╝██████╦╝██████╔╝
# ░╚════╝░░╚════╝░╚═════╝░╚═════╝░

# You can save jobs to the variable "JOBS" which the bot will then execute
# You can find a jobs blueprint with annotations below:
"""
Detailed description:
{
    # There are two main modes the bot is used in
    # 'Everything': The bot will take a look at every offer in the given category
    # 'Specific': The bot uses the given words in 'Search_for' to explicitly look for specific products 
    'Mode': 'Everything', # or 'Specific'
    
    # Category the bot searches through when 'Everything' is the selected mode 
    'Category': 'Elektronik',
    
    # Highest cost the offer can have
    # Fill with 0 to only consider free offers
    'Max_price': 0,
    
    # Whether you want to include offers where no initial price is given by the seller
    'Include_VB': False,
    
    # The arguments to search for when 'Specific' is the selected mode
    'Search_for': 'GTX 1080Ti',
    
    # Offers will be filtered out and not send to the user if they contain one of the following words:
    'Filters': [
        "Drucker",
        "Waschmaschine",
        "Mikrowelle",
        "Suche"
    ]
}

Minimum structure to fill in yourself: (Do not delete unused attributes, leave them empty instead!)
{
    'Mode': 'Everything', # or 'Specific'
    'Category': '',
    'Max_price': 0,
    'Include_VB': False,
    'Search_for': '',
    'Filters': []
}
"""

# Include your jobs inside the square brackets
# Separate multiple jobs with a comma (',')
# The two jobs below serve as an example, you should edit / delete them
JOBS = [
    {
        'Mode': 'Everything',
        'Category': 'Elektronik',
        'Max_price': 0,
        'Include_VB': False,
        'Search_for': '',
        'Filters': [
            "Drucker",
            "Waschmaschine",
            "Mikrowelle"
        ]
    },
    {
        'Mode': 'Specific',
        'Category': '',
        'Max_price': 1000,
        'Include_VB': False,
        'Search_for': 'GTX 1080Ti',
        'Filters': []
    }
]
