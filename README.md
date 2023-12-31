# iLO 5 LetsEncrypt Certificate Autorenew

This project leverages the [HP iLO Python API](https://github.com/HewlettPackard/python-ilorest-library)
to automate the request and renewal process for SSL certificates on servers
running iLO5. By default this uses the Cloudflare DNS challenge for the certificate,
but it can be modified to use any method you like.

**NB: This has only been tested with iLO 5 version 2.99.**

## Installing

Make sure you have a valid Python 3 install with `pip` ready to go. I recommend
using a virtual environment of some kind to run this script. Install dependencies...

```bash
pip install -r requirements.txt
```

...and you'll be ready to go!

## Usage

1. Customize your `.env` file using the `.env.template` file provided. Make sure
to provide values for all variables.
2. Create a file called `cloudflare-token.ini` that contains your CloudFlare DNS
API token in this format:

    ```txt
    dns_cloudflare_api_token = {YOUR TOKEN HERE}
    ```

3. Run the script: `python generate_cert.py`
4. If everything worked, iLO will reset itself in a few minutes with the new
SSL cert. You're done!
