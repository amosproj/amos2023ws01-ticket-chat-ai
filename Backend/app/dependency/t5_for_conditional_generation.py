from transformers import T5ForConditionalGeneration


def get_t5_for_conditional_generation() -> T5ForConditionalGeneration:
    return T5ForConditionalGeneration.from_pretrained(
        "TalkTix/text_generation_t5-ticket-creator"
    )
