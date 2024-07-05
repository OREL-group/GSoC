<h2>Clone this repository</h2>

```git clone https://github.com/OREL-group/GSoC```

``` cd GSoC/Open Source Sustainability```

<h2>Website</h2>

1. Install all the necessary dependencies

    ```cd website```

	```npm i``` (for the node modules)

2. Add the Github OAuth Access Token

    ```touch .env.local```

    Add your Github OAuth token access in the env file

    ```GITHUB_TOKEN=YOUR_ACCESS_TOKEN```

<h2>Mesa</h2>

1. Create a virtual environment to install all the dependencies

    ```virtualenv venv```

2. Activate the virtual environment

    ```source venv/bin/activate```

3. Install all the dependencies

    ```pip install -r requirements.txt```

4. Deploy the Mesa Models on Cloudflare tunnel

	The Mesa models can be easily visualised on a web interface by running this command, and can be accessed on localhost on any port configured.

	```mesa runserver```

	This method is just restricted to get your model up and running in localhost.
	To have them deployed globally, we will be using [Cloudflare Tunnels](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/install-and-setup/tunnel-guide/local/).

    You need to install Cloudflare tunnels CLI via the following command.

 - Mac
	```brew install cloudflare/cloudflare/cloudflared```
	
 - Linux
	```wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb && sudo dpkg -i cloudflared-linux-amd64.deb```
	
 - Windows
	```PS C:\Users\Administrator\Downloads\cloudflared-stable-windows-amd64> .\cloudflared.exe --version```

	Once you are done installing the Cloudflare CLI, run the ```server.py``` file to get the model up and running.

    You can use this command to deploy your models

	```cloudflared tunnel --url http://localhost:{portNumber}```

	This will expose your localhost and deploy your models to a URL, which you have to update in the ```iframe src``` of the website.

	
Now that you have all things set up, you can have the project running by executing this command in the ```website``` directory.
	
```npm run dev```