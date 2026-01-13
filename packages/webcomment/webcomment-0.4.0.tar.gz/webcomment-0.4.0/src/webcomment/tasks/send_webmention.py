import requests
from django.utils import timezone
from django.tasks import task
from webcomment.settings import comment_settings
from webcomment.models import Thread, ThreadTarget
from webcomment.webmention.parser import parse_sending_targets


@task(queue_name=comment_settings.TASK_QUEUE_NAME)
def send_webmention(thread_id: int):
    thread = Thread.objects.get_from_cache_by_pk(thread_id)
    items = parse_sending_targets(thread.url)
    for target, endpoint in items:
        if endpoint:
            resp = requests.post(endpoint, data={"target": thread.url, "source": target}, timeout=5)
            ThreadTarget.objects.create(
                tenant_id=thread.tenant_id,
                thread_id=thread.id,
                target=target,
                webmention_endpoint=endpoint,
                status=resp.status_code,
                published_at=timezone.now(),
            )
