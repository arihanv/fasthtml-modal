import asyncio
import random
from typing import Literal

from fasthtml.common import *

tlink = Script(src="https://cdn.tailwindcss.com")
fasthtml_app, rt = fast_app(ws_hdr=True, hdrs=[tlink])

messages = []


def chat_input(disabled=False):
    return Input(
        type="text",
        name="msg",
        id="msg-input",
        placeholder="Type a message",
        hx_swap_oob="true",
        autofocus="true",
        disabled=disabled,
        cls="!mb-0 bg-zinc-900 border border-zinc-700 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-zinc-500 disabled:bg-zinc-800 disabled:border-zinc-700 disabled:cursor-not-allowed",
    )


def chat_message(msg_idx):
    msg = messages[msg_idx]
    content_cls = f"px-2.5 py-1.5 rounded-lg max-w-xs {'rounded-br-none border-green-700 border' if msg['role'] == 'user' else 'rounded-bl-none border-zinc-400 border'}"

    return Div(
        Div(msg["role"], cls="text-xs text-zinc-500 mb-1"),
        Div(
            msg["content"],
            cls=f"bg-{'green-600 text-white' if msg['role'] == 'user' else 'zinc-200 text-black'} {content_cls}",
            id=f"msg-content-{msg_idx}",
        ),
        id=f"msg-{msg_idx}",
        cls=f"self-{'end' if msg['role'] == 'user' else 'start'}",
    )


def chat_window():
    return Div(
        id="messages",
        *[chat_message(i) for i in range(len(messages))],
        cls="flex flex-col gap-2 p-4 h-96 overflow-y-auto w-full",
    )


def chat_title():
    return Div(
        "streaming-chat-example",
        cls="text-xs font-mono absolute top-0 left-0 w-fit p-1 bg-zinc-900 border-b border-r border-zinc-700 rounded-tl-md rounded-br-md",
    )


def chat():
    return Div(
        chat_title(),
        chat_window(),
        Form(chat_input(), id="form", ws_send=True, cls="w-full"),
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
        cls="flex flex-col w-full max-w-2xl border border-zinc-700 h-full p-2 rounded-md outline-1 outline outline-zinc-700 outline-offset-2 relative",
    )


@rt("/")
async def get():
    cts = Div(chat(), cls="flex justify-center items-center min-h-screen bg-black")
    return cts


@fasthtml_app.ws("/ws")
async def ws(msg: str, send):
    messages.append({"role": "user", "content": msg})

    await send(chat_input(disabled=True))
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

    await send(chat_input(disabled=False))


if __name__ == "__main__":
    serve(app="fasthtml_app")
