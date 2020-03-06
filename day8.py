def decodeImage(image, width, height):
    number_layers = int(len(image) / (width * height))
    layers = []
    temp_image = image
    for _ in range(number_layers):
        layers.append(temp_image[:width * height])
        temp_image = temp_image[width * height:]
    return layers

def checkNumbers(layers):    
    zeros = [layer.count('0') for layer in layers]
    fewest_zeros = zeros.index(min(zeros))
    ones = layers[fewest_zeros].count('1')
    twos = layers[fewest_zeros].count('2')    
    return ones * twos

def stackLayers(im, layers):
    image = ''
    i, j = 0, 0
    while i < len(im):
        for layer in layers:
            assert j < len(layer)
            if layer[j] == '2':
                continue
            image += layer[j]
            break
        j += 1
        i += len(layers)

    return image
            
            
image = open('day8_input.txt').read()
layers = decodeImage(image,25,6)
decoded_image = stackLayers(image,layers)

print(decoded_image[:25] + '\n' + decoded_image[25:50] + '\n' + decoded_image[50:75] + '\n' + 
    decoded_image[75:100] + '\n' + decoded_image[100:125] + '\n' + decoded_image[125:150])