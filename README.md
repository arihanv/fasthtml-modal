# FastHTML + Modal Template

Deploy a FastHTML app in just a few lines of simple python code on Modal's serverless infra. 

This template is an implementation of a streaming chat app with auto-scrolling and a simple UI where you can easily swap out the dummy generator with your own LLM.

<div align="center">
  <img src="https://github.com/user-attachments/assets/0e8da83a-52e4-47d0-a89b-e4ade3a779ab" alt="fasthtml-modal" width="500">
</div>

## Run the App Locally
```
pip install -r requirements.txt
python app.py
```

## Deploy the App
Visit [modal.com](https://modal.com/) and create a free account. Then follow the instructions to authenticate in your CLI.

Run the following command in your terminal:
```
modal deploy deploy.py
```
That's it!
