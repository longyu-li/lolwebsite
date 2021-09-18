import React, { useEffect, useState } from "react";
import "./App.css";
import { Players } from "./components/Movies";
import { Player_Search } from "./components/MovieForm";
import { Container } from "semantic-ui-react";

function App() {
  const [players, setMovies] = useState([]);


  return (
    
    <Container style={{ marginTop: 40 }}>
      <Player_Search
        Player_Search={player =>
          setMovies(current_players => [player, ...current_players])
        }
      />
      <Players players={players} />
    </Container>
  );
}

export default App;
