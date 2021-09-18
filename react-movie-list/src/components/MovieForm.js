import React, { useState } from "react";
import { Form, Input, Button } from "semantic-ui-react";

export const Player_Search = ({ on_new_player }) => {
  const [title, set_summoner_name] = useState("");

  return (
    <Form>
      <Form.Field>
        <Input
          placeholder="enter summoner name"
          value={title}
          onChange={e => set_summoner_name(e.target.value)}
        />
      </Form.Field>
      <Form.Field>
        Select A Region
        <select id="picked_region">
          <option value="NA1">North America</option>
          <option value="BR1">Brazil</option>
          <option value="EUN1">Europe Nordic and East</option>
          <option value="EUW1">Europe West</option>
          <option value="JP1">Japan</option>
          <option value="KR">Korea</option>
          <option value="LA1">Latin America North</option>
          <option value="LA2">Latin America South</option>
          <option value="OC1">Oceania</option>
          <option value="RU">Russia</option>
          <option value="TR1">Turkey</option>
          
        </select>
        
      </Form.Field>
      <Form.Field>
        <Button
          
          onClick={async () => {
            var selected_region = document.getElementById("picked_region").value
            const player = { title, selected_region };
            alert(selected_region)

            const response = await fetch("#", {
              method: "POST",
              headers: {
                "Content-Type": "application/json"
              },
              body: JSON.stringify(player)
            });
 
            if (response.ok) {
              console.log("response worked!");
              //new_player_search(player);
              set_summoner_name("");
            }
          }}
        >
          submit
        </Button>
      </Form.Field>
    </Form>
  );
};
