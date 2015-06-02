# slackzon

Simple Amazon Product Search in Slack. All searches are private and only visible to you.

<< DEMO >>

## Usage

From any Slack channel, just type `/amazon [search terms]`. The products will be shown on the same channel visible just to you.

## Integrate with your team

1. Go to your channel
2. Click on **Configure Integrations**.
3. Scroll all the way down to **DIY Integrations & Customizations section**.
4. Click on **Add** next to **Slash Commands**.
  - Command: `/amazon`
  - URL: `http://amazon.goel.io/search`
  - Method: `POST`
  - For the **Autocomplete help text**, check to show the command in autocomplete list.
    - Description: `Simple Amazon Product Search in Slack.`
    - Usage hint: `[search terms]`
  - Descriptive Label: `Search Amazon`

## Developing

Add a `config.py` file based on `config.py.example` file. Grab your AWS credentials.

```python
# Install python dependencies
$ pip install -r requirements.txt

# Start the server
$ python app.py
```

## Contributing

- Please use the [issue tracker](https://github.com/karan/slackzon/issues) to report any bugs or file feature requests.
