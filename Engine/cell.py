################################################################################
# Name: James A. Chase
# File: cell.py
# Date: 23 April 2024
# Description:
#
# Class file for Cell class.
#
################################################################################

class Cell:
    def __init__(self, val: int=0) -> None:
        '''
        Constructor

        Parameters:
            - val: an integer indicating the value of the cell [1-9]

        Returns: None
        '''
        assert type(val) == int
        assert 0 <= val <= 9

        self.set_val(val)

    def get_val(self) -> int:
        '''
        Getter for private attribute {_val}

        Parameters: None

        Returns:
            - an integer containing the value stored in {_val}
        '''
        return self._val

    def set_val(self, val: int) -> bool:
        '''
        Setter for private attribute {_val}

        Parameters:
            - val: an integer indicating the value to be set to {_val}

        Returns:
            - a boolean indicating the success of the operation
        '''
        assert type(val) == int
        assert 0 <= val <= 9

        # verify input is in correct bounds, indicate failure if not
        if val < 0 or val > 9: return False

        # update val
        self._val = val

        # indicate success
        return True

if __name__ == '__main__':
    assert False, 'This is a class file. Import its contents into another file.'
