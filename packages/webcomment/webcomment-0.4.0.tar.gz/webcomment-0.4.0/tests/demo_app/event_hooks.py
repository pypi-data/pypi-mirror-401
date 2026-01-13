from django.dispatch import receiver
from webcomment.signals import webmention_received, thread_created
from webcomment.tasks.receive_webmention import create_webmention
from webcomment.tasks.send_webmention import send_webmention


@receiver(webmention_received)
def on_webmention_received(sender, **kwargs):
    create_webmention.enqueue(
        tenant_id=kwargs["tenant_id"],
        source=kwargs["source"],
        target=kwargs["target"],
    )


@receiver(thread_created)
def on_thread_created(sender, instance, **kwargs):
    send_webmention.enqueue(str(instance.id))
