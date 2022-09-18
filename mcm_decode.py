#!/usr/bin/env python3

import argparse

huffman_table = ['1111110101100100000010', '1111110101100100000011', '1111110101100100000100', '1111110101100100000101',
                 '1111110101100100000110', '1111110101100100000111', '1111110101100100001000', '1111110101100100001001',
                 '1111110101100100001010', '00111', '10101', '1111110101100100001011', '1111110101100100001100',
                 '1111110101100100001101', '1111110101100100001110', '1111110101100100001111', '1111110101100100010000',
                 '1111110101100100010001', '1111110101100100010010', '1111110101100100010011', '1111110101100100010100',
                 '1111110101100100010101', '1111110101100100010110', '1111110101100100010111', '1111110101100100011000',
                 '1111110101100100011001', '1111110101100100011010', '1111110101100100011011', '1111110101100100011100',
                 '1111110101100100011101', '1111110101100100011110', '1111110101100100011111', '110', '01100000101',
                 '0000011', '10110110111', '101101101100', '1111110101101', '1111110100', '11111101011000', '0100100',
                 '0100101', '11101100', '10111110', '11100', '1111011', '1110111', '1001111', '101100', '111100',
                 '010110', '1011110', '1011010', '0101110', '0000010', '0110001', '0101111', '0100001', '1110101',
                 '10111111', '101101101101', '010101', '01111100', '111111010100', '0111111100100', '010011101',
                 '111011010', '0100110', '101101111', '011000010', '100111010', '011000000', '1001110110', '01111101',
                 '011000001001', '111111010111', '101101100', '111111011', '101101110', '0111111101', '11111100',
                 '0111111111', '01111110', '0100000', '01001111', '011111110011', '01111111000', '1001110111',
                 '11111101011001001', '011000001000', '1111110101100101', '00101', '111111010101', '00110', '10011100',
                 '1110100', '0110000011', '10001', '0101000', '011001', '1111010', '0001', '1001101', '1111101',
                 '000010', '10100', '010011100', '111011011', '101110', '010001', '10010', '01101', '011110',
                 '1011011010', '01110', '00100', '10000', '000011', '0101001', '011000011', '1111100', '1001100',
                 '0111111110', '1111111', '0111111100101', '000000', '111111010110011', '111111010110010000000']

split_string = lambda x, n: [x[i:i+n] for i in range(0, len(x), n)]

'''
Builds a Huffman tree, corresponding to the given Huffman lookup table,
for ease of decoding an encoded bit stream.
'''
def build_huffman_tree(list):
    tree = []
    for i in range(0, len(list)):
        ## Convert element i from the lookup table into its tree representation.
        # 1. Browse the tree to find the leaf node (create nodes if necessary).
        node = tree
        for c in list[i]:
            # Initialize the node if necessary.
            if node == []:
                node.extend([[],[]])
            if (c != '0' and c != '1'):
                raise Exception("Invalid Huffman table")
            # bit = int(c)
            node = node[int(c)]
        # 2. Store the corresponding list index in the leaf node.
        node.append(i)
    return tree

'''
For reference, see https://towardsdatascience.com/huffman-decoding-cca770065bab
and https://towardsdatascience.com/huffman-encoding-python-implementation-8448c3654328
We simplify the coding by using nested lists to represent the Huffman tree,
instead of a custom structure.
'''
def huffman_decode(s):
    result = ''

    # Setup the Huffman tree for ease of decoding the bit stream.
    tree = build_huffman_tree(huffman_table)

    # Do the bit stream decoding proper:
    # browse the tree to find the corresponding leaf nodes.
    node = tree
    for c in s:
        # Initialize the node if necessary.
        if (c != '0' and c != '1'):
            raise Exception("Invalid stream")

        node = node[int(c)]
        if len(node) == 1:
            result += chr(node[0]) # Leaf contains the character index.
            node = tree # Reset the current node to the top of the tree.

    # Find the last EOT character and strip it and everything else after it.
    return result.rsplit(chr(4), 1)[0]

def base95_decode(s):
    result = ''
    code = split_string(s, 2)
    for c in code:
        hi = ord(c[0]) - 32
        lo = ord(c[1]) - 32
        number = hi*95 + lo
        # Convert decoded number to its binary representation string, ensure
        # 13 digits are emitted, strip the '0b' prefix, and reverse the bits.
        result += bin(number)[2:].zfill(13)[::-1]
    return result

def main():
    parser = argparse.ArgumentParser('mcm.py', description='Decode Mathematica files')
    parser.add_argument('input_file', help='file to be decoded')
    parser.add_argument('output_file', help='file where the decoded output will be written')
    args = parser.parse_args()

    with open(args.input_file, 'r') as file:
        code = file.read()
        if code[:12] != '(*!1N!*)mcm\n':
            raise Exception('Invalid encrypted Mathematica file!')

    bits = base95_decode(''.join(code[12:].split('\n')))
    body = huffman_decode(bits)

    with open(args.output_file, 'w+') as result_file:
        result_file.write(body)

if __name__ == '__main__':
    main()
