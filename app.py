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
        cls="flex flex-col gap-2 p-4 h-[40vh] overflow-y-auto w-full",
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


def title():
    return Div(
        Span("Modal + FastHTML", cls="font-bold text-6xl"),
        Span(
            Span("Get started by editing ", cls=""),
            Span(
                "app.py",
                cls="font-mono text-green-500 bg-zinc-900 px-1 py-0.5 rounded-md text-sm",
            ),
            Span(" or deploying to Modal with ", cls=""),
            Span(
                "deploy.py",
                cls="font-mono text-green-500 bg-zinc-900 px-1 py-0.5 rounded-md text-sm",
            ),
        ),
        cls="flex-1 flex flex-col items-center justify-center gap-2",
    )


def arrow_right():
    return Div(
        Svg(
            NotStr(
                """<circle cx="12" cy="12" r="10"/><path d="M8 12h8"/><path d="m12 16 4-4-4-4"/>"""
            ),
            width="24",
            height="24",
            viewBox="0 0 24 24",
            fill="none",
            stroke="currentColor",
            stroke_width="1.5px",
        ),
        cls="flex items-center justify-center text-green-500 group-hover:text-green-400 size-5 -rotate-45",
    )


def github_link():
    return A(
        Svg(
            NotStr(
                """<path d="M7.49933 0.25C3.49635 0.25 0.25 3.49593 0.25 7.50024C0.25 10.703 2.32715 13.4206 5.2081 14.3797C5.57084 14.446 5.70302 14.2222 5.70302 14.0299C5.70302 13.8576 5.69679 13.4019 5.69323 12.797C3.67661 13.235 3.25112 11.825 3.25112 11.825C2.92132 10.9874 2.44599 10.7644 2.44599 10.7644C1.78773 10.3149 2.49584 10.3238 2.49584 10.3238C3.22353 10.375 3.60629 11.0711 3.60629 11.0711C4.25298 12.1788 5.30335 11.8588 5.71638 11.6732C5.78225 11.205 5.96962 10.8854 6.17658 10.7043C4.56675 10.5209 2.87415 9.89918 2.87415 7.12104C2.87415 6.32925 3.15677 5.68257 3.62053 5.17563C3.54576 4.99226 3.29697 4.25521 3.69174 3.25691C3.69174 3.25691 4.30015 3.06196 5.68522 3.99973C6.26337 3.83906 6.8838 3.75895 7.50022 3.75583C8.1162 3.75895 8.73619 3.83906 9.31523 3.99973C10.6994 3.06196 11.3069 3.25691 11.3069 3.25691C11.7026 4.25521 11.4538 4.99226 11.3795 5.17563C11.8441 5.68257 12.1245 6.32925 12.1245 7.12104C12.1245 9.9063 10.4292 10.5192 8.81452 10.6985C9.07444 10.9224 9.30633 11.3648 9.30633 12.0413C9.30633 13.0102 9.29742 13.7922 9.29742 14.0299C9.29742 14.2239 9.42828 14.4496 9.79591 14.3788C12.6746 13.4179 14.75 10.7025 14.75 7.50024C14.75 3.49593 11.5036 0.25 7.49933 0.25Z" fill="currentColor" fill-rule="evenodd" clip-rule="evenodd"/>"""
            ),
            width="15",
            height="15",
            viewBox="0 0 15 15",
            fill="none",
            cls="bg-zinc-900 rounded-sm p-0.5 border border-green-500",
        ),
        Span("GitHub", cls="font-mono text-green-500 hover:text-green-400 text-sm"),
        href="https://github.com/arihanv/modal-fasthtml",
        target="_blank",
        cls="font-mono text-green-500 hover:text-green-400 flex items-center gap-1",
    )


def footer():
    return Div(
        Div(
            Div("Docs", cls="text-zinc-400 text-sm"),
            Div(
                A(
                    Span(
                        "Modal",
                        cls="font-mono text-green-500 group-hover:text-green-400 text-xl",
                    ),
                    arrow_right(),
                    href="https://modal.com/docs",
                    target="_blank",
                    cls="justify-between items-center pl-2 pr-1 flex border border-green-500 w-40 rounded-md group",
                ),
                Div(cls="w-px bg-zinc-700 h-6"),
                Div(
                    A(
                        "FastHTML",
                        href="https://docs.fastht.ml/",
                        target="_blank",
                        cls="font-mono text-green-500 hover:text-green-400 text-xl",
                    ),
                    arrow_right(),
                    cls="justify-between items-center pl-2 pr-1 flex border border-green-500 w-40 rounded-md",
                ),
                cls="flex items-center justify-start gap-2",
            ),
            cls="flex flex-col items-center gap-1",
        ),
        Div(
            Div("Source", cls="text-zinc-400 flex justify-center w-full text-sm"),
            Div(
                github_link(),
            ),
            cls="flex flex-col items-center gap-1",
        ),
        cls="flex-1 flex-col flex items-center justify-center gap-5",
    )


@rt("/")
async def get():
    cts = Div(
        title(),
        chat(),
        footer(),
        cls="flex flex-col items-center min-h-screen bg-black",
    )
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
