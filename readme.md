# Lispr Flow v0
> Note: This name is temporary, i may think of a better name later 

---

## Why am i building this?

its Jul 10 2026, i switched on Linux a few days ago and i am really missing wispr flow. I love the OS but the lack of Wispr flow hurts me. And since more and more people are trying to leave microslop, i thought why not fix this? AI coding with gpt5.6 is really good. 

So this is my attempt to make a dumb clone, with not as many features as wispr but something that just works. And then i will opensource it for the comunity to add features and all. I can’t focus on this full time coz of my other comitments, but i can definetly start the project.

---

# Pricing & GTM

I am planning to opensource this project, but also charge a subscription tier of $5/mo for a install this and it just works (no hassle) version. I would love for this to be free, but then i have to pay API prices for the Voice to Text models. There will be a way to just bring in ur API key and u can use it with no subscriptions.  

I will try to launch it using my twitter & other platforms. Also i will try to get shoutouts from some small creators, and i will try to get this to a monthly subscription of 100 people. and then let this thing just exist, unless i get a overwhelming response. 

That overwhelming response shldn’t be people using this coz this is cheaper then wispr, i don’t wanan be the cheaper clone of a existing software. I just want to fullfill a real pain-point i have, and i assume many have. 

---

# Tech Stack

I don’t know the app dev layout of linux, coz i want this to work on as many distros as possible without wasting a ton of my time, i would 1st support ubuntu (coz that’s what i use). I also don’t know how to build apps, how to ship them as binaries, etc etc, so this is gonna be a fun ride. 

What i know is i am gonna use 11labs scribe v2 or gpt 4o transcribe voice to text models in the backend, and clerk for auth (coz i heard abt them via Theo, and i don’t wanna deal with GCP auth).

---

## Day 0 UI prototype

The first visual prototype is a lightweight native PySide6 window. It is deliberately
click-through only: it does not record audio, save API keys, authenticate users, or
open billing yet.

### Look at the app while developing

You do **not** build a binary while making changes. Lispr runs straight from
`main.py`, the same way the old prototype did.

Do this setup **once** after cloning the project. It creates `.venv`, a private
folder containing PySide6 for this project only:

```bash
sudo apt install python3 python3-venv
git clone https://github.com/prshv1/Lispr.git
cd Lispr
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Then, every time you change the code, simply run:

```bash
.venv/bin/python main.py
```

That opens the app directly from your edited source code. Close the window,
make another change, and run the same command again. There is no build step and
no reinstall step during normal development.

If you prefer the old short command, activate the project environment once per
terminal window:

```bash
source .venv/bin/activate
python main.py
```

`source .venv/bin/activate` only changes which Python your current terminal
uses. It does not install the app. Close the terminal and you are back to your
normal system Python.

#### If Ubuntu says `venv` is unavailable

Install the package matching the Python version shown in the error. For example,
if it says `python3.14-venv`:

```bash
sudo apt install python3.14-venv
```

Then repeat the one-time setup commands above.

The UI currently includes a native warm-paper desktop layout, a visual dictation
state, working invite-link and transcript copy, deletable transcript-history preview,
speaking summary, and settings controls. It is still a visual prototype: no recordings
or accounts are persisted.
