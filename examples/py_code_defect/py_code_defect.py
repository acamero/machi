import machi.tools.data_utils as du


def generateSeq(filename_ok,
                filename_def):
  ok_vector = du.py2vector(filename_ok)
  ok_seq = du.tokens2seq(ok_vector, du.py_vocab)
  def_vector = du.py2vector(filename_def)
  def_seq = du.tokens2seq(def_vector, du.py_vocab)
  def_class = du.mark_defects(def_vector, ok_vector)
  df_seq = du.seq2df(def_seq, def_class, du.py_vocab, ['ok', 'defective'])
  return df_seq


if __name__ == '__main__':
  _tf = None
  if _tf:
    # clone Tensorflow repository and get the src
    # execute 'bash py_code_defect_tf.sh'
  else:
    filename = "./test.py"
    filename_def = "./test_def.py"
  

