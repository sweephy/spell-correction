from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch


class LanguageDetectionUtil:
	tokenizer = AutoTokenizer.from_pretrained("papluca/xlm-roberta-base-language-detection")
	model = AutoModelForSequenceClassification.from_pretrained("papluca/xlm-roberta-base-language-detection")

	def get_language(self, text):
		inputs = self.tokenizer(text, return_tensors="pt")
		with torch.no_grad():
			logits = util.model(**inputs).logits

		predicted_class_id = logits.argmax().item()
		res = util.model.config.id2label[predicted_class_id]
		return res  # tr, en etc.


if __name__ == '__main__':
	util = LanguageDetectionUtil()
	util.get_language('deneme yazisi')
