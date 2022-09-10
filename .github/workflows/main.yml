name: automation
on:
  schedule:
  - cron:  '0 0 * * *'
  workflow_dispatch:
jobs:
  send_message:
    runs-on: ubuntu-latest
    name: WeChatID:17600005204
    steps:
    - name: checkout
      uses: actions/checkout@v3
      with:
        ref: main
    - name: sender
      uses: actions/setup-python@v2
      with:
        python-version: '3.x'
        architecture: 'x64'
    - run: pip install -r ./requirements.txt && python ./main.py && python cityinfo.py
