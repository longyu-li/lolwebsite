import React from "react";
import { List, Header, Rating } from "semantic-ui-react";

export const Players = ({ players }) => {
  return (
    <List>
      {players.map(player => {
        return (
          <List.Item key={player.player_id}>
            <Header>{player.summoner_name}</Header>
            <Rating rating={player.games_played} maxRating={30} disabled />
          </List.Item>
        );
      })}
    </List>
  );
};
