-- Developer: Andrés Aníes <andres_anies@hotmail.com>

-- Drop the database tournament if does not exist
--  and them create it again for resetting the schema
--  and the data(useful for running the script multiple times).
DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;
\c tournament

-- Players schema definition.
CREATE TABLE Players (
  ID   SERIAL PRIMARY KEY,
  NAME TEXT
);

-- Matches schema definition.
CREATE TABLE Matches (
  ID     SERIAL PRIMARY KEY,
  WINNER INTEGER REFERENCES Players (ID),
  LOSER  INTEGER REFERENCES Players (ID)
);

-- Prevent rematches between players.
CREATE UNIQUE INDEX UniqueMatches
ON Matches (WINNER, LOSER);

-- View for getting the number of wins for each player.
CREATE VIEW PlayerWins AS
  SELECT
    Players.id,
    count(Matches.winner) AS wins
  FROM Players
    LEFT JOIN Matches
      ON Players.id = Matches.winner
  GROUP BY Players.id, Players.name;

-- View for getting the number of matches for each player.
CREATE VIEW PlayerMatches AS
  SELECT
    Players.id,
    count(Matches.id) AS matches
  FROM Players
    LEFT JOIN Matches
      ON Players.id = Matches.winner OR Players.id = Matches.loser
  GROUP BY Players.id, Players.name;

-- View for getting the number of wins and matches(standings) for each player.
CREATE VIEW PlayerStandings AS
  SELECT
    Players.id,
    Players.name,
    PlayerWins.wins,
    PlayerMatches.matches
  FROM Players, PlayerWins, PlayerMatches
  WHERE Players.id = PlayerWins.id AND Players.id = PlayerMatches.id
  ORDER BY wins DESC;
