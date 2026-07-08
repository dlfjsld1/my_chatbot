import html
import random
from textwrap import dedent


THINKING_PHRASES = [
    "생각중..",
    "이게 맞나 고민중..",
    "오 이거 괜찮은거 같아 해보는 중..",
    "머릿속 회의 소집중..",
    "답변을 반짝반짝 다듬는 중..",
    "잠깐만요, 논리 점검중..",
    "좋은 표현을 고르는 중..",
    "한 번 더 확인해보는 중..",
]


def show_thinking_loader(container):
    phrases = random.sample(THINKING_PHRASES, k=len(THINKING_PHRASES))
    total_seconds = len(phrases) * 1.45
    step_seconds = total_seconds / len(phrases)
    visible_percent = 100 / len(phrases)
    fade_percent = min(4.5, visible_percent * 0.4)

    phrase_spans = "\n".join(
        (
            f'<span style="animation-delay: {index * step_seconds:.2f}s">'
            f"{html.escape(phrase)}</span>"
        )
        for index, phrase in enumerate(phrases)
    )

    loader_markup = dedent(
        f"""
        <style>
        .rgb-thinking-loader {{
            min-height: 2.2rem;
            margin: 0.15rem 0 0.6rem;
        }}

        .rgb-thinking-loader__phrases {{
            position: relative;
            display: block;
            width: min(100%, 30rem);
            height: 1.8rem;
            overflow: hidden;
        }}

        .rgb-thinking-loader__phrases span {{
            position: absolute;
            left: 0;
            top: 0;
            max-width: 100%;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            color: transparent;
            font-size: 1.02rem;
            font-weight: 800;
            line-height: 1.8rem;
            letter-spacing: 0;
            opacity: 0;
            background: linear-gradient(
                90deg,
                #ff245d,
                #ffb300,
                #27e86f,
                #00b7ff,
                #8d4dff,
                #ff245d
            );
            background-size: 320% 100%;
            -webkit-background-clip: text;
            background-clip: text;
            animation:
                rgb-phrase-cycle {total_seconds:.2f}s infinite ease-in-out,
                rgb-color-shift 1.05s infinite linear,
                rgb-glow-pulse 0.95s infinite ease-in-out;
        }}

        @keyframes rgb-phrase-cycle {{
            0% {{
                opacity: 0;
                transform: translateY(0.32rem);
            }}
            {fade_percent:.2f}% {{
                opacity: 1;
                transform: translateY(0);
            }}
            {visible_percent:.2f}% {{
                opacity: 1;
                transform: translateY(0);
            }}
            {(visible_percent + fade_percent):.2f}% {{
                opacity: 0;
                transform: translateY(-0.32rem);
            }}
            100% {{
                opacity: 0;
                transform: translateY(-0.32rem);
            }}
        }}

        @keyframes rgb-color-shift {{
            0% {{ background-position: 0% 50%; }}
            100% {{ background-position: 320% 50%; }}
        }}

        @keyframes rgb-glow-pulse {{
            0%, 100% {{
                filter: drop-shadow(0 0 0.1rem rgba(255, 36, 93, 0.7));
            }}
            50% {{
                filter:
                    drop-shadow(0 0 0.35rem rgba(39, 232, 111, 0.82))
                    drop-shadow(0 0 0.5rem rgba(0, 183, 255, 0.7));
            }}
        }}
        </style>
        <div class="rgb-thinking-loader" role="status" aria-live="polite">
            <div class="rgb-thinking-loader__phrases">
                {phrase_spans}
            </div>
        </div>
        """
    ).strip()

    container.html(loader_markup)


def stream_with_thinking_loader(stream, container):
    show_thinking_loader(container)
    has_started = False

    try:
        for chunk in stream:
            if chunk and not has_started:
                container.empty()
                has_started = True
            yield chunk
    finally:
        if not has_started:
            container.empty()
