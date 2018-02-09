## Joytan ジョイ単

<img src="./logo/joytan.png" align="right" width="90" height="90" title="logo">
     
[![Build Status](https://travis-ci.org/kokimame/joytan.svg?branch=master)](https://travis-ci.org/kokimame/joytan)
[![Gitter chat](https://badges.gitter.im/gitterHQ/gitter.png)](https://gitter.im/JoytanApp/Lobby)
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Twitter](https://img.shields.io/twitter/follow/JoytanApp.svg?style=social&label=Follow)](https://twitter.com/intent/follow?screen_name=JoytanApp)

***Joytan is in early development and does not yet have a stable production.***

Joytan is a small desktop app that automates the boring process of **creating your own audio/textbooks**.
It's designed to be especially useful for language learner and encourages screen-free study in general.

Key features include:
- Non-commercial open source and cross-platform desktop application
- **Creating MP3 audiobooks with your best-loved songs and sound effects**
- Full control of sequence and every timbre of your audiobook
- Audiobook with **lifelike speech** from Amazon Polly
- Support free, fast and local Text-to-Speech alternatives
- **Creating textbook** fast and locally for free, easy to export to PDF
- **Designing your own original textbook** with basic HTML
- **Automatic language translation** powered by Google Translation
- **Automatic visual aid (images) download** to your textbook from Google Image
- **Automatic online dictionary lookup** for language learning
- Saving scripts as light and readable CSV format
- With Google Sheets, you can edit scripts anywhere, anytime with your friends
- Simple and tiny GUI, just 3 main dialogs!


## What You Create
We are distributing some of sample creation on YouTube. Take a look!

[![acronyms](https://img.youtube.com/vi/2wVEDKgj1TA/0.jpg)](https://www.youtube.com/watch?v=2wVEDKgj1TA)

[![jlpt_sample](https://img.youtube.com/vi/Qj_Nw97ZkPY/0.jpg)](https://www.youtube.com/watch?v=Qj_Nw97ZkPY)



*NOTE: Videos were created from two resources. One is audiobooks which were
 created with Joytan, the other is image clips which were created separately from the app.
 Video-making feature is not included in the current version of Joytan.*

## Download & Installation
#### Windows
1. Download [Windows Installer (.exe)](https://drive.google.com/uc?export=download&id=1QhkcsuzZYVpWrNne8sh6qGUK0wh1JwVX)
to your desktop or download folder.
2. Double-click on the installer and follow instructions. Joytan will be installed to your computer.
3. Double-click on the new Joytan icon on your desktop to start Joytan.

*NOTE: You will see a black window (console) while running Joytan on Windows. Please don't close the window,
the strange behaviour arises from a difficulty of handling underlying processes on Windows.*

#### Mac
1. Download [Joytan for Mac (.dmg)](https://drive.google.com/uc?export=download&id=1KqcJqL4Xf_Zt105iIfrHJO1irNPcaK1U)
to your desktop or download folder.
2. Open the file and drag Joytan Icon into Application folder.

#### Linux/BSD
1. Download [Joytan for Linux (.zip)](https://drive.google.com/uc?export=download&id=1Uvgy4mIQ8xOYGXnD2jblojRUNXoAh7sd)
2. Then from Terminal, the following commands install dependencies and Joytan. (Example on Ubuntu)
```
$ tar xjf Downloads/joytan-0.0.0-amd64.tar.bz2
$ cd joytan-0.0.0
$ sudo apt-get install ffmpeg
$ sudo apt-get install lame
$ make
$ sudo make install
```


#### Others
- [Source (.zip)](https://github.com/kokimame/joytan/archive/v0.0.0-beta.zip)
- [Source (.tar.gz)](https://github.com/kokimame/joytan/archive/v0.0.0-beta.tar.gz)

## Quick Start

We highly recommend you to use **Amazon Polly** as Text-to-Speech service of your audiobooks
because of its speech quality and cost-effectiveness.
Although it's not free, but if you're first to use AWS, you're eligible to the AWS Free Tier and
you are free to turn 5 million characters per month into speech for the first 12 months.
Even if you're not, its free replay feature is very cost-effective especially for our usage.
This means previewing your audiobooks is free.

To see its pricing and create free account, see [the website](https://aws.amazon.com/polly/pricing/).

After successfully creating your Amazon Web Service (AWS) account, you have personal configurations of AWS. 
To activate Amazon Polly on Joytan, you need to make two files in a specific folder to store settings. 
The detail of this process is explained [here](https://boto3.readthedocs.io/en/latest/guide/configuration.html).

1. Create your credentials file at 
```~/.aws/credentials``` (```C:\Users\USER_NAME\.aws\credentials``` for Windows users)
 and save the following lines after replacing the placeholders with your own.
```
[default]
aws_access_key_id = YOUR_KEY
aws_secret_access_key = YOUR_SECRET
```

2. Next, create your config file at
```~/.aws/config``` (```C:\Users\USER_NAME\.aws\config``` for Windows users)
 and save the following lines.
```
[default]
region=us-east-1
```

3. That's it. Now you can select Amazon Polly on Text-to-Speech selector from Edit/Preferences. 

## Development
Joytan requires:
- Python 3.5+
- PyQt that supports Qt 5.9+
- ffmpeg (Pydub's dependency, it may work with 'libav' but not tested)
- lame (AwesomeTTS's dependecy)

and a number of Python packages, which you can install via pip:
```
pip3 install -r requirements.txt
```

To use the development version:

```
git clone https://github.com/kokimame/joytan.git
cd joytan
./devscript/build_ui.sh
```

If you get any errors, you will not be able to proceed, so please return to
the top and check the requirements again.

Now you are ready to run Joytan by:
```
./runapp
```


## Contribution
- Report a bug: See [issues]()
- Feature/Content request and feedback on [Twitter](https://twitter.com/JoytanApp), 
[YouTube](https://www.youtube.com/channel/UC0bLbtTI9uni3bNRPIJQAqA) are appreciated.


## Disclaimer
Copyright © 2017-Present Koki Mametani.

Joytan is lincenced under the GNU General Public License version 3.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES
OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
