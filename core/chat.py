from django.http import JsonResponse, StreamingHttpResponse
from django.conf import settings
from django.views.decorators.http import require_http_methods
from core.model import ContextLookup
from core.views import login_required, require_perm
from time import time
import json
import requests


@login_required
@require_perm(relation="member", domain="chatbot")
@require_http_methods(["GET"])
def chat_api(request):
    try:
        query = request.GET['query']
    except KeyError:
        return JsonResponse({"error": "Missing query"}, status=400)

    return StreamingHttpResponse(
        response_generator(query=query),
        content_type='text/event-stream'
    )


def event(**kwargs):
    return f"data: {json.dumps(kwargs)}\n\n".encode()


SYSTEM_PROMPT = """
Ты — ассистент с доступом к содержанию книги. Строго соблюдай правила:

1. Источник информации — ТОЛЬКО предоставленный контекст
2. Если ответа нет в контексте: "Информация не найдена в документации"
3. Запрещено:
   - Придумывать факты
   - Использовать знания вне контекста
4. Формат ответа:
   - Кратко (1-3 предложения)
   - В цитатах необходимо упоминать источник
5. Контекст состоит из нескольких фрагментов, обрамленных фразами
   НАЧАЛО КОНТЕКСТА НОМЕР N и КОНЕЦ КОНТЕКСТА НОМЕР N, каждый фрагмент
   содержит ИСТОЧНИК
6. Фрагменты контекста отсортированы по порядку встречания в книге
"""


def response_generator(query):
    print('got request', time())
    yield event(type="user", text=query)
    print('first response', time())

    model: ContextLookup = settings.MODEL
    results = model.lookup(query)

    prompt = ['ВОПРОС:', query]

    prompt.append('')
    prompt.append('КОНТЕКСТ:')

    for ir, r in enumerate(results):
        prompt.append('')
        prompt.append(f'НАЧАЛО КОНТЕКСТА НОМЕР {ir+1}. ИСТОЧНИК: {r["source"]}, чанк {r["idx"]}')
        prompt.append(r['text'])
        prompt.append(f'КОНЕЦ КОНТЕКСТА НОМЕР {ir+1}')

        yield event(type="context", title=f'Контекст {ir+1}. Источник: {r["source"]}, чанк {r["idx"]}', text=r["text"])

    prompt = '\n'.join(prompt)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
    ]

    t1 = time()
    usage = None
    try:
        token = settings.DEEPSEEK_TOKEN
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "model": "deepseek-chat",
                "messages": messages,
                "temperature": 0.3,
            },
            timeout=60,
        )
        response.raise_for_status()

        body = response.json()
        ai_response = body["choices"][0]["message"]["content"]
        usage = body["usage"]
    except Exception as e:
        ai_response = f"Ошибка: {str(e)}"
    t2 = time()

    meta = f'{t2 - t1:.1f} sec'
    # https://api-docs.deepseek.com/quick_start/pricing/
    # 1M TOKENS INPUT (hit)  7c
    # 1M TOKENS INPUT (miss) 27c
    # 1M TOKENS OUTPUT       110c
    prices = {
        'prompt_cache_hit_tokens': 7,
        'prompt_cache_miss_tokens': 27,
        'completion_tokens': 110,
    }
    if usage:
        cost = 0
        for sku, price in prices.items():
            cost += usage.get(sku, 0) * price
        cost = cost / 1e6
        meta = meta + f', cost: {cost:.3f}¢'

    ai_response = ai_response + "\n\n_" + meta + "_"

    yield event(type="assistant", text=ai_response)

    yield b"event: close\ndata: \n\n"
