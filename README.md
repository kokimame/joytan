## Joytan ジョイ単

<img src="./logo/joytan.png" align="right" width="90" height="90" title="logo">
     
[![Build Status](https://travis-ci.org/kokimame/joytan.svg?branch=master)](https://travis-ci.org/kokimame/joytan)
[![Gitter chat](https://badges.gitter.im/gitterHQ/gitter.png)](https://gitter.im/JoytanApp/Lobby)
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Twitter](https://img.shields.io/twitter/follow/JoytanApp.svg?style=social&label=Follow)](https://twitter.com/intent/follow?screen_name=JoytanApp)

**Website**: https://kokimame.github.io/joytan/


#### Convert CSV files to your original audio/textbooks with Joytan.
Joytan is a free, small cross-platform desktop app that facilitates the process of making audio/textbooks.
Joytan comes with some powerful features which are especially designed to be useful for language-learners.

Key features include:
- **Creating MP3 audiobooks with your best-loved songs and sound effects**
- Full control of sequence and every timbre of your audiobook
- Audiobook with **lifelike speech using [Amazon Polly](https://aws.amazon.com/polly/)**
- Support free, fast and local Text-to-Speech alternatives
- **Creating textbook** fast and locally for free, easy to export to PDF
- **Designing original textbook** with basic HTML
- **Automatic language translation** powered by Google Translation
- **Automatic visual aid (images) download** to your textbook from Google Image
- **Automatic online dictionary-lookup** for language learning
- **Saving scripts in CSV files, ready to export to [Anki](https://apps.ankiweb.net)**
- Editing scripts online even with people around the world via Google Sheets
- Simple and tiny GUI, just 3 main dialogs!


## What You See
<!-- Screenshots of dialogs -->
<figure>
  <a href="./docs/images/main_full.png">
    <img src="./docs/images/main_full.png"
    alt="Screenshots of Input window" width="150" height="180">
  </a>
</figure>
<figure>
  <a href="./docs/images/audio_full.png">
    <img src="./docs/images/audio_full.png"
    alt="Screenshots of Textbook setting window" width="150" height="180">
  </a>
</figure>
<figure>
  <a href="./docs/images/text_full.png">
    <img src="./docs/images/text_full.png"
    alt="Screenshots of Audiobook setting window" width="150" height="180">
  </a>
</figure>



## What You Get
We are distributing some of sample creations on [YouTube](https://www.youtube.com/channel/UC0bLbtTI9uni3bNRPIJQAqA). Take a look!

<a href="https://www.youtube.com/watch?v=HOWVGxGHCMg">
  <img src="https://img.youtube.com/vi/tEIpgTREexQ/0.jpg" width="260" height=180" />
</a>
<a href="https://www.youtube.com/watch?v=2wVEDKgj1TA">
  <img src="https://img.youtube.com/vi/ehkQu1mKyeU/0.jpg" width="260" height=180" />
</a>

*NOTE: Videos were created from two resources. One is audiobooks which were
 created with Joytan, the other is image clips which were created separately from the app.
 Video-making feature is not included in the current version of Joytan.*

## Download & Installation
Joytan works on Windows, Mac, and Linux.

Please download & installation Joytan from [our website](https://kokimame.github.io/joytan/install.html
).

## Quick Start
Tutorials are available on [our website](https://kokimame.github.io/joytan/index.html).
- [Set up Amazon Polly](https://kokimame.github.io/joytan/tutorial.html)
- [How to Organize for your book](https://kokimame.github.io/joytan/tutorial_input.html)
- [How to Make Audiobooks](https://kokimame.github.io/joytan/tutorial_audio.html)
- [How to Make Textbooks](https://kokimame.github.io/joytan/tutorial_text.html)


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
- Report a bug: See [issues](https://github.com/kokimame/joytan/issues)
- Feature/Content request and feedback on [Twitter](https://twitter.com/JoytanApp), 
[YouTube](https://www.youtube.com/channel/UC0bLbtTI9uni3bNRPIJQAqA) are appreciated.


## Disclaimer
Copyright © 2017-Present Kohki Mametani (kohkimametani@gmail.com).

Joytan is lincensed under the GNU General Public License version 3.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES
OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
