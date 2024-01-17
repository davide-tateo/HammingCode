import numpy as np

class HammingCode(object):   

    def __init__(self, number):
        '''
        Initializes the HammingCode class
        name: str
        '''
        
        self.number=int(number) 
        self.binary_value= None
        self.message_vector = None
        self.encoded = None
        self.wrongcoded = None
        self.correctedcoded = None
        self.checkvector_wrongcoded = None


        self.convert_number_to_binary()

    def convert_number_to_binary(self):
        '''
        Every number from 0 to 15 can be transformed into a 4 digit binary number 
        '''
        if self.number >= 0 and self.number <= 15:
            self.binary_value= format(self.number, '04b')
            print(f'Integer Number: {self.number}. Binary Equivalent (4 digits): {self.binary_value}')
        else:
            raise Exception ('The number provided is not in the range 0-15 and therefore cannot be transformed into a 4-digit binary value') 
          
    def number_to_vector(self):
        '''
        Create a vector from the individual binary digits and check again it's four digits and binary
        '''
        self.message_vector = [int(digit) for digit in self.binary_value]
        if len(self.message_vector) != 4:
            raise Exception("The number provided does not have four digit")
        for element in self.message_vector:
            if element > 1 or element <0:
                raise Exception("The number provided is not a binary value")   
        self.message_vector = np.array([self.message_vector]) 
        print(f'The Message Vector for number {self.number} is {self.message_vector}')

    def encode(self):
        '''
        By multiplying Matrix G (7,4) for the message vector (1,4) we obtain the encoded vector of our message (1,7)
        '''
        G = np.array([[1, 1, 0, 1],
            [1, 0, 1, 1],
            [1, 0, 0, 0],
            [0, 1, 1, 1],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]])
        G = np.transpose(G)

        # Multiplying the vector (1,4) for the matrix transpose (4,7) so to be able to do the operation and reduced for modulo 2 so to have it binary
        self.encoded = np.dot(self.message_vector, G) % 2 
        print(f'The Encoded Vector for number {self.number} is {self.encoded}')

    def introduce_error(self, number_of_errors, error1_position, error2_position=False): 
        '''
        Possibility to add either one error digit or two error digits to the encoded message
        '''
        if error2_position:
            if error2_position < 0 or error2_position > 7:
                raise Exception("There position of error number 2 is not a valid position because it is not between 0 and 7 included")
            if error2_position == error1_position:
                raise Exception("The position of error number 2 cannot be the same as the position of error number 1")
        if error1_position < 0 or error1_position > 7:
            raise Exception("There position of error number 1 is not a valid position because it is not between 0 and 7 included")
        if self.encoded is None:
            raise Exception("There is no encoded message")
        elif number_of_errors != 1 and number_of_errors != 2:
            raise Exception("the number of errors is neither 1 nor 2")
        else:    
            self.wrongcoded=self.encoded.copy()
            if number_of_errors == 1:
                self.wrongcoded[0,error1_position-1]=1-self.wrongcoded[0,error1_position-1]
                print(f'Introduced error in one digit; the wrong vector is {self.wrongcoded}')
            else: 
                self.wrongcoded[0,error1_position-1]=1-self.wrongcoded[0,error1_position-1]
                self.wrongcoded[0,error2_position-1]=1-self.wrongcoded[0,error2_position-1]
                print(f'Introduced error in two digits; the wrong vector is {self.wrongcoded}')        
    
    '''
    Then the decoding part starts, considering how usually one end is doing the encoding and another end is doing the decoding,
    we consider how the party doing the decoding simply receives the encoded message and therefore has the need to check 
    if the number is seven digit and binary so to be decoded
    '''

    def checkencoded(self, check_wrongcoded = False):
        '''
        Checking if the message received is binary and seven digits, if so then it's possible to proceed with the decodification
        '''
        if check_wrongcoded:
            if self.wrongcoded.size != 7:
                raise Exception("The number provided does not have seven digit")
            for element in self.wrongcoded: 
                if (self.encoded > 1).any() or (self.wrongcoded < 0).any():
                    raise Exception("The number provided is not a binary value")
                print(f'The Encoded Message Vector {self.wrongcoded} is a binary seven digit value')
        else:
            if self.encoded.size != 7:
                raise Exception("The number provided does not have seven digit")
            for element in self.encoded: 
                if (self.encoded > 1).any() or (self.encoded < 0).any():
                    raise Exception("The number provided is not a binary value")
                print(f'The Encoded Message Vector {self.encoded} is a binary seven digit value')


    def paritycheck(self, check_wrongcoded = False):
        '''
        Checking in which position the encoded message is carrying error (if it's carrying any) by multiplying matrix H and the encoded vector, 
        and we assume the error is only one since the code can detect up to two bits errors but cannot identify the position for both 
        and correction is possible only when assuming only one bit is wrong
        '''
        H = np.array([[1,0,0],
              [0,1,0],
              [1,1,0],
              [0,0,1],
              [1,0,1],
              [0,1,1],
              [1,1,1]])
        
        #matrix H [7,3] and encoded [1,7]
        if check_wrongcoded:
            checkvector=np.dot(self.wrongcoded,H) % 2
            self.checkvector_wrongcoded = checkvector
        else: 
            checkvector=np.dot(self.encoded,H) % 2 #encoded [1,7] * H [7,3]

        if np.array_equal(checkvector, np.array([[0,0,0]])):
            print(f'The Check Vector is {checkvector} and no error is present')
        else: 
            print(f'The Check Vector is {checkvector} and we assume some error is present')

    
    def correct_error(self):
        """Assuming the error i a 1-bit error, it corrects the error and saves the corrected result
        """

        paritycheckdict = {0:np.array([[1,0,0]]), 1:np.array([[0,1,0]]), 2:np.array([[1,1,0]]), 3:np.array([[0,0,1]]), 4:np.array([[1,0,1]]), 5:np.array([[0,1,1]]), 6:np.array([[1,1,1]])}
        #Finding the correspondence between self.checkvector_wrongcoded and the arrays in paritycheckdict
        if self.wrongcoded is None:
            raise Exception("No error was created, therefore there is nothing to correct")
        a = None
        for key, value in paritycheckdict.items():   
            if np.array_equal(self.checkvector_wrongcoded,value):
                a = value.copy()
        #Finding the key corresponding to the value saved in the variable a
        if a is not None:
            for key, value in paritycheckdict.items():
                if np.array_equal(value,a):
                    error_index = key
                    print (f"the error is in position {error_index+1}")
                    break
            #Correcting the error
            self.correctedcoded = self.wrongcoded.copy()
            self.correctedcoded[0,error_index]=1-self.correctedcoded[0,error_index]
            print(f"If the error was 1-bit, the error in {self.wrongcoded} has been corrected. The restored encoded vector is {self.correctedcoded}. Otherwise a 2-digit error was converted in a 3-digit error, and the codeword retreived ({self.correctedcoded}) contains the wrong message")

        else: raise Exception("No one-bit error was found")

    def decode(self, restored=False):
        '''
        Using matrix R to decode the message to obtain the initial 4-bits vector and convert it back to the original integer number.
        This is done only for correct message to decode with no errors, because trying to decode something with errors would make no 
        sense and would not return a proper result.
        '''
        #Define R matrix
        R = np.array([[0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [1, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]])
        #Decoding
        if restored:
            codeword=np.array([self.correctedcoded])
        else:
            codeword=np.array([self.encoded])
        decoded=np.dot(codeword, R) % 2
        original_number = int(''.join(map(str, decoded.flatten())), 2) #Make the decoded vector back into a string and then integer of 2 digits
        print(f'The Decoded Message Vector is {decoded.flatten()}. The Original Integer Number inputed was {original_number}')
              

#Some examples of testing the different possible combinations


#Examples of encoding, parity checking and decoding with 0 error present
message_1= HammingCode(0)
message_1.number_to_vector()
message_1.encode()
message_1.checkencoded()
message_1.paritycheck()
message_1.decode()

message_2= HammingCode(2)
message_2.number_to_vector()
message_2.encode()
message_2.checkencoded()
message_2.paritycheck()
message_2.decode()

message_3= HammingCode(10)
message_3.number_to_vector()
message_3.encode()
message_3.checkencoded()
message_3.paritycheck()
message_3.decode()

message_4= HammingCode(15)
message_4.number_to_vector()
message_4.encode()
message_4.checkencoded()
message_4.paritycheck()
message_4.decode()

#Examples of encoding, parity checking and decoding with 1 digit error present
message_5= HammingCode(0)
message_5.number_to_vector()
message_5.encode()
message_5.introduce_error(1,3)
message_5.checkencoded(True)
message_5.paritycheck(True)
message_5.correct_error()
message_5.decode(True)

message_6= HammingCode(4)
message_6.number_to_vector()
message_6.encode()
message_6.introduce_error(1,1)
message_6.checkencoded(True)
message_6.paritycheck(True)
message_6.correct_error()
message_6.decode(True)

message_7= HammingCode(12)
message_7.number_to_vector()
message_7.encode()
message_7.introduce_error(1,7)
message_7.checkencoded(True)
message_7.paritycheck(True)
message_7.correct_error()
message_7.decode(True)

message_8= HammingCode(15)
message_8.number_to_vector()
message_8.encode()
message_8.introduce_error(1,6)
message_8.checkencoded(True)
message_8.paritycheck(True)
message_8.correct_error()
message_8.decode(True)

#Examples of encoding and checking with 2 digit error present. No decoding will be attempted as by default it is impossible to correct a 2-digit error
message_9= HammingCode(0)
message_9.number_to_vector()
message_9.encode()
message_9.introduce_error(2,2,6)
message_9.checkencoded(True)
message_9.paritycheck(True)
message_9.correct_error()

message_10= HammingCode(6)
message_10.number_to_vector()
message_10.encode()
message_10.introduce_error(2,6,2)
message_10.checkencoded(True)
message_10.paritycheck(True)
message_10.correct_error()

message_11= HammingCode(11)
message_11.number_to_vector()
message_11.encode()
message_11.introduce_error(2,7,1)
message_11.checkencoded(True)
message_11.paritycheck(True)
message_11.correct_error()

message_12= HammingCode(14)
message_12.number_to_vector()
message_12.encode()
message_12.introduce_error(2,4,5)
message_12.checkencoded(True)
message_12.paritycheck(True)
message_12.correct_error()