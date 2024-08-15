import asyncio
import random

from fasthtml.common import *

tlink = Script(src="https://cdn.tailwindcss.com")
fasthtml_app, rt = fast_app(ws_hdr=True, hdrs=[tlink])

messages = [
    {"role": "assistant", "content": "Hello, how can I help you today?"},
    {"role": "user", "content": "I need assistance with my order."},
    {
        "role": "assistant",
        "content": "Sure! Can you provide me with your order number?",
    },
    {"role": "user", "content": "It's 12345."},
    {"role": "assistant", "content": "Thank you! Let me check that for you."},
    {"role": "user", "content": "I need to return the item."},
    {
        "role": "assistant",
        "content": "I'm sorry to hear that. Can you please provide me with the reason for the return?",
    },
    {"role": "user", "content": "I received the wrong item."},
    {
        "role": "assistant",
        "content": "I apologize for the inconvenience. Can you please provide me with the correct item number?",
    },
]


def chat_input():
    return Input(
        type="text",
        name="msg",
        id="msg-input",
        placeholder="Type a message",
        hx_swap_oob="true",
    )


def chat_message(msg_idx):
    msg = messages[msg_idx]
    role = Div(msg["role"], cls="text-xs text-gray-500 mb-1")
    if msg["role"] == "user":
        return Div(
            role,
            Div(msg["content"], cls="bg-blue-500 text-white p-2 rounded-lg max-w-xs"),
            id=f"msg-{msg_idx}",
            cls="self-end",
        )
    else:
        return Div(
            role,
            Div(
                msg["content"],
                cls="bg-gray-300 text-black p-2 rounded-lg max-w-xs",
                id=f"msg-content-{msg_idx}",
            ),
            id=f"msg-{msg_idx}",
            cls="self-start",
        )


def chat_window():
    return Div(
        id="messages",
        *[chat_message(i) for i in range(len(messages))],
        cls="flex flex-col gap-2 p-4 max-w-3xl max-h-96 overflow-y-auto",
    )


@rt("/")
async def get():
    cts = Div(
        chat_window(),
        Form(chat_input(), id="form", ws_send=True),
        Script(
            """
            function scrollToBottom(smooth) {
                var messages = document.getElementById('messages');
                messages.scrollTo({
                    top: messages.scrollHeight,
                    behavior: smooth ? 'smooth' : 'auto'
                });
            }
            window.onload = function() {
                scrollToBottom(true);
            };

            const observer = new MutationObserver(function() {
                scrollToBottom(false);
            });
            observer.observe(document.getElementById('messages'), { childList: true, subtree: true });
            """
        ),
        hx_ext="ws",
        ws_connect="/ws",
    )
    return Titled("Websocket Test", cts)


async def on_connect(send):
    print("Connected!")
    await send(Div("Hello, you have connected", id="notifications"))


async def on_disconnect(ws):
    print("Disconnected!")


@fasthtml_app.ws("/ws", conn=on_connect, disconn=on_disconnect)
async def ws(msg: str, send):
    messages.append({"role": "user", "content": msg})

    await send(chat_input())
    await send(
        Div(chat_message(len(messages) - 1), id="messages", hx_swap_oob="beforeend")
    )

    message = "You typed: " + msg

    chunks = []
    while message:
        chunk_size = random.randint(4, 10)
        chunk = message[:chunk_size]
        chunks.append(chunk)
        message = message[chunk_size:]

    messages.append({"role": "assistant", "content": ""})

    await send(
        Div(chat_message(len(messages) - 1), id="messages", hx_swap_oob="beforeend")
    )

    stream_response = ""
    for chunk in chunks:
        stream_response += chunk
        messages[-1]["content"] += chunk
        await send(
            Span(chunk, id=f"msg-content-{len(messages)-1}", hx_swap_oob="beforeend")
        )
        await asyncio.sleep(0.2)


if __name__ == "__main__":
    serve(app="fasthtml_app")
