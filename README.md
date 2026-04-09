# nSEA-with-GUI
> (not) Safe Exam Addon - with GUI

## What
nSEA-with-GUI is a desktop app that automates access to Safe Exam Browser (SEB) exams without SEB, through a standard browser.

It logs into your school's Moodle instance, downloads the `.seb` config file, and generates the HTTP header needed to access the exam.

Supported levels of security:
- [x] Unencrypted Config Key
- [ ] Encrypted Config Key
- [ ] Browser Exam Key

## Why
SEB isn't available for GNU/Linux. Linux students, whenever an exam is taken, must connect via the school's Windows computers. This tool removes that requirement.

## Setup
1. Create a `credentials.txt` file in the same folder as the app with exactly this format,
   each on its own line, no spaces around the `=`:
```
username=youruser
password=yourpassword
```

## How
1. Navigate to your Moodle exam page in a browser
2. Copy the URL and paste it into the app
3. Click **Enter**
4. The app will:
   - Log into Moodle using your credentials
   - Find and download the `.seb` config file
   - Generate the config key hash
5. Copy the output header and add it to your browser using an addon like [SimpleModifyHeaders](https://github.com/didierfred/SimpleModifyHeaders) for [Firefox](https://addons.mozilla.org/firefox/addon/simple-modify-header/) or [Chrome](https://chrome.google.com/webstore/detail/simple-modify-headers/gjgiipmpldkpbdfjkgofildhapegmmic)

The output will look like:  
X-SafeExamBrowser-ConfigKeyHash : 6eb3652038ec372a2f2ec0c374e2cbf2c924e9b5d5aade177e7cef57f0598580

## Resources
- [Original nSEA script](https://github.com/Chiogros/nSEA)
- [Developer documentation - Config key](https://safeexambrowser.org/developer/seb-config-key.html)

## Disclaimer
This is for educational purposes only. Don't use it to cheat. I'm not responsible for whatever you do with it.  
The login and scraping are made for TGM's Moodle, no idea if it works for other schools. Also i know the GUI looks like shit as its just made to enable people who don't like using the terminal.
