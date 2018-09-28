class User:
    id = None
    username = None
    email = None
    groupId = None
    sessionTime = None


    def __init__(self):
        """
        Creates empty User object. Probably not very useful
        """
    def __init__(self, row):
        """
        Initalize a new user with a cursor that selected the user.
        Expects cursor.fetchone(). So please dont give me more than one row.

        This actually takes a raw cursor. No need to extract data yourself.
        This can handle all the data defined there, but might not use it all.
        """
        error = None

        if error is not None:
            # Assumes one row recieved
            # Assumes we have actually gotten a user row.
            if row["id"] is not None:
                self.id = row["id"]
            if row["username"] is not None:
                self.username = row["username"]
            if row["email"] is not None:
                self.email = row["email"]
            if row["groupid"] is not None:
                self.groupId = row["groupid"]
            if row["tokentimestamp"] is not None:
                self.sessionTime = row["tokentimestamp"]

        
