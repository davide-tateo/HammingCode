# Hamming Code implementation in Python
This code was realised in cooperation with a colleague as an assignment for the Foundation of Data Science course at Copenhagen Business School.
Collaborator: Francesca Salute

## DESCRIPTION
In this project, a university colleague and I implemented Hamming's (7,4) algorithm, a linear error-correcting code invented by Richard W. Hamming in 1950. The encoder, written in Python, takes a 4-bit binary value and transforms it into a robust 7-bit binary codeword using the generator matrix (G). The encoder also includes a parity check functionality based on the parity-check matrix (H) to detect errors in the codeword.

Additionally, a Python decoder program has been crafted to reverse the encoding process. Given a 7-bit vector codeword, the decoder utilizes Hamming's Decoder Matrix (R) to recover the original 4-bit binary value. The decoder ensures that applying the matrix-vector product (R * codeword) yields the original word.

To validate the functionality, rigorous testing has been conducted with both error-free and erroneous scenarios. The code handles the encoding and decoding of 4-bit vectors seamlessly, providing a practical demonstration of error detection and correction, mirroring the importance of Hamming codes in various communication and storage applications, including WiFi, cell phones, satellites, and digital television.
