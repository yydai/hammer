from .execute import Execute

class CRF(object):
    def __init__(self):
        pass

    @classmethod
    def train(self, train_data, model, desp=None, template_name='template.txt',
              verbose=False):
        if not model:
            import datetime
            model = datetime.datetime.now().isoformat()
            model = './{}'.format(model)
            print("current model name is {}".format(model))

        print("model name is {}".format(model))
        cmd = ['crf_learn', '-f', '3', '-c', '4.0', template_name,
               train_data, model, '-t']
        Execute.call(cmd, verbose=verbose)
        return model

    @classmethod
    def test(self, test_data, result, model, desp=None, level=''):
        cmd = 'crf_test {} -m {} {} > {}'.format(level, model, test_data, result)

        Execute.system_call(cmd)
