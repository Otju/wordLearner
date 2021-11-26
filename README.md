## How to use

### Setup

1. Download Python 3: https://www.python.org/downloads/
2. Run `setup.sh` (or just `pip install pyttsx3`)
3. Add some dictionary to root folder as `dictionary.json`, ex.

```
{
  "Animals": {
    "cat": "кот"
  },
  "Vehicles": {
    "motor vehicle": "машина",
  }
}
```

4. Install Russian text to speech: [Windows](https://support.microsoft.com/en-us/topic/how-to-download-text-to-speech-languages-for-windows-10-d5a6b612-b3ae-423f-afa5-4f6caf1ec5d3), [Mac](https://support.apple.com/en-my/guide/mac-help/mchlp2290/mac)

- If the Text-To-Speech doesn't work (sound doesn't play on start)

  - On Windows: try fix here https://stackoverflow.com/a/56733000
  - On Mac/Linux: you're probably fucked

### Use

- Just start with `start.sh` (or `python gui.py`)
