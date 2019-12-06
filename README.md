# ali_parther

- Create a Python virtual environment.

    virtualenv --no-site-packages -p python3.5 env

- Upgrade packaging tools.

    env/bin/pip install --upgrade pip setuptools

- Install the project in editable mode with its testing requirements.

    env/bin/pip install -e "."
    
- Activate virtualenv in console

    source env/bin/activate

- Run

    env/bin/python -m ali_partner

- Check redirect

    curl --referer rg.yottos.com -L -I http://0.0.0.0:10000
    
- Check partner links

    source env/bin/activate

    link_check ./ali_partner/partner-links.json ./partner-links-checked.json

    
    
    
git pull && supervisorctl restart ali_parther: