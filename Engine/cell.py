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
    def __init__(self, val: int=0, is_locked: bool=False) -> None:
        '''
        Constructor

        Parameters:
            - val: an integer indicating the value of the cell [1-9]
            - is_locked: a boolean value indicating if the cell should be locked
                         or not

        Returns: None
        '''
        assert type(val) == int
        assert type(is_locked) == bool
        assert 0 <= val <= 9

        self.set_locked(is_locked)
        self.set_val(val)

    def __str__(self) -> str:
        '''
        Determines how the object is represented as a string.

        Parameters: None

        Returns:
            - a string representation of the object
        '''
        return f'Cell<val: {self.get_val()}, is_locked: {self.get_locked()}>'

    def get_val(self) -> int:
        '''
        Getter for private attribute {val}

        Parameters: None

        Returns:
            - an integer containing the value stored in {val}
        '''
        return self.__val

    def set_val(self, val: int) -> bool:
        '''
        Setter for private attribute {val}

        Parameters:
            - val: an integer indicating the value to be set to {val}

        Returns:
            - a boolean indicating the success of the operation
        '''
        assert type(val) == int
        assert 0 <= val <= 9

        # verify input is in correct bounds, indicate failure if not
        if val < 0 or val > 9: return False

        # indicate failure if cell is locked
        if self.__is_locked: return False

        # update val
        self.__val = val

        # indicate success
        return True
    
    def get_locked(self) -> bool:
        '''
        Getter for private attribute {is_locked}

        Parameters: None

        Returns:
            - the boolean value stored in {is_locked}
        '''
        return self.__is_locked
    
    def set_locked(self, locked: bool) -> None:
        '''
        Setter for private attribute {is_locked}

        Parameters:
            - locked: the boolean value to be stored in {is_locked}

        Returns: None
        '''
        assert type(locked) == bool

        self.__is_locked = locked

if __name__ == '__main__':
    assert False, 'This is a class file. Import its contents into another file.'
