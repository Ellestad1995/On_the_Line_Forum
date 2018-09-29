import click
class User():
    username = "starlord"
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
        #click.echo("Info recieved: {Id}, {Username}".format(Id=row["id"],Username=row["username"]))
        if error is None:
            # Assumes one row recieved
            # Assumes we have actually gotten a user row.
            if row["id"] is not None:
                self.id = row["id"]
            if row["username"] is not None:
                click.echo("Handling username: {}".format(row["username"]))
                self.username = row["username"]
            if row["email"] is not None:
                self.email = row["email"]
            if row["groupid"] is not None:
                self.groupId = row["groupid"]
            if row["tokentimestamp"] is not None:
                self.sessionTime = row["tokentimestamp"]
            else:
                self.sessionTime = None

    def dumpInfo(self):
        """
        Used mostly for debugging purpose.
        It just dumpts whatever info it has with click.echo
        NB: Never dump the token. Think like a script kiddie.
        """
        click.echo("""
        id: {I}
        username: {U}
        email: {E}
        groupId: {G}
        session: {S}
        """.format(I=self.id, U=self.username, E=self.email, G=self.groupId, S=self.sessionTime))
