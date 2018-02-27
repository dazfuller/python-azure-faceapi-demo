# Cognitive Service - Face API Demo

This is a simple python app which uses the Azure [Cognitive Services](https://azure.microsoft.com/services/cognitive-services/) Face API, it will take collection of JPG images from a source directory, submit each image and then produce a card for each face found showing the facial attributes (age and gender) along with the emotional scoring.

![Example card](/media/example_card.png?raw=true "Example card")

## Setting up

The code should pretty much work as is but with a couple of minor things. First I'm working within a python virtual environment on OSX, I've got Anaconda installed but you'll need to upgrade Python to get the `venv` module working. You can do this wtih the following command.

```bash
$ conda update python
```

Then you can set up the virtual environment as follows.

```bash
$ mkdir venv
$ python -m venv venv/csdemo
$ source venv/csdemo/bin/activate
$ pip install -r requirements.txt
```

I've built the solution using [Visual Studio Code](https://code.visualstudio.com) and there is a vscode settings file in place which will work with this virtual environment (assuming you have the python extension install).

After this you'll need to create a `config.json` file in the root of the repository, this will contain the API Key for your cognitive services account. If you don't have one then head over to the website and click the Try for Free link. Alternatively, if you already have an Azure saubscription then you can add cognitive services as a resource.

```json
{
    "apiKey": "<Face API Key>"
}
```

Last thing, in the `csdemo.py` code file there's a variable at the top for setting the font used when building the card. This should work on most environments, but if not then this will need changing. If you're on Windows then the library will search the system fonts by default so you could change it to something like `'arial.ttf'` to get it to work.
