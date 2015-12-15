#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def executeSql(sql, parameters=(), commit=False):
    """Execute the required sql and commit the changes to the database if needed,
    additionally returns any data that could by being asked to the database.
    Args:
        sql: The SQL command to be sent to the database.
        parameters: Any dynamic generated data or user input needed to be cleaned.
        commit: Specifies if the sql command needs to be committed.

    Returns: List of tuples that was asked if the sql command was a query statement.
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(sql, tuple([bleach.clean(parameter) for parameter in parameters]))
    data = None
    if commit:
        conn.commit()
    else:
        data = cursor.fetchall()
    conn.close()
    return data


def deleteMatches():
    """Remove all the match records from the database."""
    executeSql("DELETE FROM Matches;", commit=True)


def deletePlayers():
    """Remove all the player records from the database."""
    executeSql("DELETE FROM Players;", commit=True)


def countPlayers():
    """Returns the number of players currently registered."""
    return executeSql("SELECT COUNT(*) FROM Players;")[0][0]


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    executeSql("INSERT INTO Players(NAME) VALUES(%s);",
               parameters=(name,), commit=True)


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    return executeSql("SELECT * FROM PlayerStandings")


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    executeSql("INSERT INTO Matches(WINNER, LOSER) VALUES(%s,%s)",
               parameters=(winner, loser), commit=True)


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    raw_pairs = executeSql("SELECT player1.id, player1.name, player2.id, player2.name "
                           "FROM PlayerStandings AS player1, PlayerStandings AS player2 "
                           "WHERE player1.wins = player2.wins AND player1.id < player2.id;")
    return filter_duplicate_players_in_pairing(raw_pairs)


def filter_duplicate_players_in_pairing(pairs):
    """
    Filters the duplicate players for the swiss pairing
        making sure that a player just plays one match per round.
    Args:
        pairs: A list of tuples for swiss pairing which maybe
            include multiple matches for a player
    Returns: A list of tuples filtered that contains just one player per round
    """
    pairs, players, duplicate_players_in_pair = set(pairs), [], []
    for pair in pairs:
        if pair[0] in players or pair[2] in players:
            duplicate_players_in_pair.append(pair)
        else:
            players.extend([pair[0], pair[2]])
    pairs = pairs.difference(duplicate_players_in_pair)
    return list(pairs)
