class DatabaseError(Exception):
    """
    Generički izuzetak za sve greške vezane za bazu podataka.
    """
    def __init__(self, message: str = "Došlo je do greške u bazi podataka"):
        super().__init__(message)


class DbnotFoundException(DatabaseError):
    """
    Izuzetak za slučaj kada resurs nije pronađen u bazi podataka.
    """
    def __init__(self, message: str = "Resurs nije pronađen"):
        super().__init__(message)


class KlijentAlreadyExistsException(DatabaseError):
    """
    Izuzetak za slučaj kada klijent već postoji u bazi podataka.
    """
    def __init__(self, message: str = "Klijent već postoji"):
        super().__init__(message)
