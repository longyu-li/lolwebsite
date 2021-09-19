import React from 'react'
import { Input, Button, Form, FormDropdown, Search } from 'semantic-ui-react'
import './App.css';
import axios from 'axios';



const region_options = [
  {
    key: 'na1',
    text: 'North America',
    value: 'na1',
    //image: { avatar: true, src: '/images/avatar/small/jenny.jpg' },
  },
  {
    key: 'br1',
    text: 'Brazil',
    value: 'br1',
    //image: { avatar: true, src: '/images/avatar/small/jenny.jpg' },
  },
  {
    key: 'eun1',
    text: 'Europe Nordic and East',
    value: 'eun1',
    //image: { avatar: true, src: '/images/avatar/small/jenny.jpg' },
  },
  {
    key: 'jp1',
    text: 'Japan',
    value: 'jp1',
    //image: { avatar: true, src: '/images/avatar/small/jenny.jpg' },
  },
  {
    key: 'kr',
    text: 'Korea',
    value: 'kr',
    //image: { avatar: true, src: '/images/avatar/small/jenny.jpg' },
  },
  {
    key: 'la1',
    text: 'Latin America North',
    value: 'la1',
    //image: { avatar: true, src: '/images/avatar/small/jenny.jpg' },
  },
  {
    key: 'la2',
    text: 'Latin America South',
    value: 'la2',
    //image: { avatar: true, src: '/images/avatar/small/jenny.jpg' },
  },
  {
    key: 'oc1',
    text: 'Oceania',
    value: 'oc1',
    //image: { avatar: true, src: '/images/avatar/small/jenny.jpg' },
  },
  {
    key: 'ru',
    text: 'Russia',
    value: 'ru',
    //image: { avatar: true, src: '/images/avatar/small/jenny.jpg' },
  },
  {
    key: 'tr1',
    text: 'Turkey',
    value: 'tr1',
    //image: { avatar: true, src: '/images/avatar/small/jenny.jpg' },
  },
]

function App() {
  const [summoner_name, set_summoner_name]=React.useState();
  const [region, set_region]=React.useState();

  const handle_submit= async (evt)=>{
    evt.preventDefault();

    console.log(region)
    const data = await axios(`http://localhost:5000/${region}/${summoner_name}`)
    //console.log(data)
    //alert(data.data[0])
    var entries = data.data.to_return.length
    var i = 0
    var paragraph = document.getElementById("spam_and_fun")
    paragraph.innterText = ""
    while (i < entries) {
      console.log(data.data.to_return[i])
      paragraph.innterText += ('\n' + data.data.to_return[i] + '\n')

      i++
    }



  }

  return (
    <h1>

    
    <Form onSubmit={handle_submit}
    class="ui_form">
      <Form.Field>
        <Input 
          type="text"
          placeholder="search a name"
          id="search_name"
          onChange= {summoner_name=>set_summoner_name(summoner_name.target.value)}
        >
        </Input>
      </Form.Field>
      <FormDropdown
        options={region_options}
        id="region_selection"
        onChange= {(region,{value})=>
          set_region(value)}

      >
      </FormDropdown>
    <Form.Field>
      <Button
        type="submit"
          
    
      >Search!

      </Button>
    </Form.Field>
    </Form>
      <body>
        <p id="spam_and_fun">

        </p>
      </body>
    </h1>
    


  );
}

export default App;
