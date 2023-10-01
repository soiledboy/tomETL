import React, { Component } from "react";
import { Query } from 'react-apollo';
import gql from 'graphql-tag';

const CARD_QUERY = gql`
  query {
    cards {
      success,
      errors,
      cards {
        name
      }
    }
  }
`;

 
class CardPage extends Component {
  render() {
    return (
      <div className="row">
        <div className="col-md-12">
          <h1 className="mt-5">Card (single) Page</h1>
          <p>H Component</p>

          <Query query={CARD_QUERY}>
            {({ loading, error, data }) => {
              if (loading) return <div>Fetching</div>
              if (error) return <div>Error</div>
              
              const cardsToRender = data.cards.cards;

              return (
                <>
                  {cardsToRender.map(card => <li key={card.name}>{card.name}</li>)}
                </>
              )
            }}
          </Query>
          
        </div>
      </div>
    );
  }
}

export default CardPage;
 