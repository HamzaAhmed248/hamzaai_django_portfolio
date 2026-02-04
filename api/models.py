from django.db import models
from .exceptions import PromptNotSetError

# Create your models here.


class Conversation(models.Model):
    """
    One conversation per IP
    Stores full Q/A history with timestamps
    """

    ip_address = models.GenericIPAddressField(unique=True)

    conversation_text = models.TextField(blank=True)

    def __str__(self):
        return f"Conversation with {self.ip_address}"


class KnowledgeBase(models.Model):
    prompt_data = models.TextField()

    def save(self, *args, **kwargs):
        self.pk = 1   #prompt_data.pk=1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

    @classmethod
    def get_prompt(cls):
        try:
            obj = cls.objects.get(pk=1)

            if not obj.prompt_data.strip():
                raise PromptNotSetError(
                    "Prompt data is empty. Please enter the prompt first."
                )

            return obj.prompt_data

        except cls.DoesNotExist:
            raise PromptNotSetError(
                "Prompt not found. Please enter the prompt first."
            )

    def __str__(self):
        return self.prompt_data