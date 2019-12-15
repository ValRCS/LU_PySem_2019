import numpy as np
import os
import subprocess
import zipfile
import tensorflow as tf

class DeepDream(object):
    '''DeepDream implementation, adapted from official tensorflow deepdream tutorial:
    https://github.com/tensorflow/tensorflow/tree/master/tensorflow/examples/tutorials/deepdream
    Credit: Alexander Mordvintsev
    '''

    _DOWNLOAD_URL = 'https://storage.googleapis.com/download.tensorflow.org/models/inception5h.zip'
    _ZIP_FILENAME = 'deepdream_model.zip'
    _MODEL_FILENAME = 'tensorflow_inception_graph.pb'

    @staticmethod
    def _download_model():
        try:
            from urllib.request import urlretrieve  # python 3
        except ImportError:
            from urllib import urlretrieve  # python 2
        urlretrieve(DeepDream._DOWNLOAD_URL, DeepDream._ZIP_FILENAME)

        zipfile.ZipFile(DeepDream._ZIP_FILENAME, 'r').extractall('.')

    @staticmethod
    def _tffunc(*argtypes):
        '''Helper that transforms TF-graph generating function into a regular one.
        See `_resize` function below.
        '''
        placeholders = list(map(tf.placeholder, argtypes))
        def wrap(f):
            out = f(*placeholders)
            def wrapper(*args, **kw):
                return out.eval(dict(zip(placeholders, args)), session=kw.get('session'))
            return wrapper
        return wrap

    @staticmethod
    def _base_resize(img, size):
        '''Helper function that uses TF to resize an image'''
        img = tf.expand_dims(img, 0)
        return tf.image.resize_bilinear(img, size)[0,:,:,:]

    def __init__(self):
        if not os.path.exists(DeepDream._MODEL_FILENAME):
            self._download_model()

        self._graph = tf.Graph()
        self._session = tf.InteractiveSession(graph=self._graph)
        self._resize = self._tffunc(np.float32, np.int32)(self._base_resize)
        with tf.gfile.FastGFile(DeepDream._MODEL_FILENAME, 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
        self._t_input = tf.placeholder(np.float32, name='input') # define the input tensor
        imagenet_mean = 117.0
        t_preprocessed = tf.expand_dims(self._t_input-imagenet_mean, 0)
        tf.import_graph_def(graph_def, {'input':t_preprocessed})

        self.t_obj = self.T('mixed4d_3x3_bottleneck_pre_relu')[:,:,:,139]
        #self.t_obj = tf.square(self.T('mixed4c'))

    def T(self, layer_name):
        '''Helper for getting layer output tensor'''
        return self._graph.get_tensor_by_name('import/%s:0'%layer_name)

    def _calc_grad_tiled(self, img, t_grad, tile_size=512):
        '''Compute the value of tensor t_grad over the image in a tiled way.
        Random shifts are applied to the image to blur tile boundaries over 
        multiple iterations.'''
        sz = tile_size
        h, w = img.shape[:2]
        sx, sy = np.random.randint(sz, size=2)
        img_shift = np.roll(np.roll(img, sx, 1), sy, 0)
        grad = np.zeros_like(img)
        for y in range(0, max(h-sz//2, sz),sz):
            for x in range(0, max(w-sz//2, sz),sz):
                sub = img_shift[y:y+sz,x:x+sz]
                g = self._session.run(t_grad, {self._t_input:sub})
                grad[y:y+sz,x:x+sz] = g
        return np.roll(np.roll(grad, -sx, 1), -sy, 0)

    def process_frame(self, frame, iter_n=10, step=1.5, octave_n=4, octave_scale=1.4):
        t_score = tf.reduce_mean(self.t_obj) # defining the optimization objective
        t_grad = tf.gradients(t_score, self._t_input)[0] # behold the power of automatic differentiation!

        # split the image into a number of octaves
        img = frame
        octaves = []
        for i in range(octave_n-1):
            hw = img.shape[:2]
            lo = self._resize(img, np.int32(np.float32(hw)/octave_scale))
            hi = img-self._resize(lo, hw)
            img = lo
            octaves.append(hi)
        
        # generate details octave by octave
        for octave in range(octave_n):
            if octave>0:
                hi = octaves[-octave]
                img = self._resize(img, hi.shape[:2])+hi
            for i in range(iter_n):
                g = self._calc_grad_tiled(img, t_grad)
                img += g*(step / (np.abs(g).mean()+1e-7))
                #print('.',end = ' ')
        return img