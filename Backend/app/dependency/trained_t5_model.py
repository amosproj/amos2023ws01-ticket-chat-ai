from fastapi.params import Depends
from transformers import T5ForConditionalGeneration, T5Tokenizer

from app.dependency.t5_for_conditional_generation import get_t5_for_conditional_generation
from app.dependency.t5_tokenizer import get_t5_tokenizer
from app.model.t5.use_trained_t5_model import TrainedT5Model


def get_trained_t5_model(model: T5ForConditionalGeneration = Depends(get_t5_for_conditional_generation),
                         tokenizer: T5Tokenizer = Depends(get_t5_tokenizer)) -> TrainedT5Model:
    return TrainedT5Model(model=model, tokenizer=tokenizer)
