from sudachipy import tokenizer
from sudachipy import dictionary

# 形態素解析クラス
class MorphologicalAnalyzer:
  __tokenizer_obj = None
  __mode_c = None

  # initialize
  def __init__(self):
    self.__tokenizer_obj = dictionary.Dictionary(dict_type="full").create()
    self.__mode_c = tokenizer.Tokenizer.SplitMode.C

  # tokenize
  def tokenize(self, text):
    return [m.surface() for m in self.__tokenizer_obj.tokenize(text, self.__mode_c)]

# lambda app handler
def handler(event, context):

  text = event['text']
  analyzer = MorphologicalAnalyzer()
  res = analyzer.tokenize(text)
  
  print(res)
  return res

if __name__=="__main__":
  res = handler({}, {})
  print(res)