from PIL import Image as im
import random
import sys
import numpy
from scipy.fftpack import dct
from scipy.fftpack import idct


def get_random_numbers_list():
    s = [-1, 1]
    return [random.random()*random.choice(s)  for i in range(1000)]


if __name__=="__main__":
    if len(sys.argv) != 3:
        print("Provide an input image and output image")
        sys.exit
    
    '''
        https://mail.python.org/pipermail/image-sig/2010-October/006526.html
        Used for conversion of RGB image to YCbCr image
    '''

    # Read Inputs
    image = im.open(sys.argv[1])
    o_image = sys.argv[2]

    # Convert to YCbCr
    ycbcr = image.convert('YCbCr')
    B = numpy.ndarray((image.size[1], image.size[0], 3), 'u1', ycbcr.tobytes())
    #print B.shape
    #im.fromarray(B[:,:,0], "L").show()
    
    # Extract Y plane from YCbCr
    y = B[:,:,0]

    # Calculate DCT
    dct_m = dct(y.astype(float),norm = 'ortho')
    #dct_m = dct(dct(y.astype(float), axis=0, norm = 'ortho'), axis=1, norm = 'ortho')

    # Convert DCT matrix to vector
    dct_v = dct_m.flatten()

    # Generate Watermark sequence
    watermark_seq = get_random_numbers_list()

    # Embed watermark sequence to original vector
    for i in range(1000):
        dct_v[i] = dct_v[i] * watermark_seq[i]

    # Output watermarked image with RGB color space
    n_dct_m = dct_v.reshape(dct_m.shape)
    n_y = idct(n_dct_m, norm='ortho')
    #n_y = idct(idct(n_dct_m, axis=1, norm='ortho'), axis=0, norm='ortho')
    n_img = numpy.dstack((n_y, B[:,:,1:]))

    result = im.fromarray((n_img).astype(numpy.uint8), mode='YCbCr').convert('RGB')
    result.save(o_image)

    pass
