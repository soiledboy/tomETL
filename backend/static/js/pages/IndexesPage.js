import React, { useState } from "react";
import PropTypes from 'prop-types';
import AsyncSelect from 'react-select/async';
import { useQuery } from '@apollo/react-hooks';
import { withApollo } from 'react-apollo';

import MultiSeriesChart from '../components/MultiSeriesChart';
import {QUERY_INDEXES, QUERY_CARD_SET_PRICES_BY_IDS} from '../Queries';
// import { handleInputChange } from "react-select/src/utils";


class BaseComparativeChart extends React.Component {
  constructor(props) {
    super()

    this.state = {
      timePeriod: "1m",
      indexIds: [],
      series: []
    }

    this.client = props.client;

    this.dateIntervals = ["1d", "5d", "1m", "3m", "6m", "YTD", "1Y", "2Y", "5Y", "Max"];
    this.btnSelected = "btn btn-secondary btn-sm active"
    this.btnUnselected = "btn btn-secondary btn-sm"
  }

  getBtnClassName = (di) => {
    return (this.state.timePeriod == di) ? this.btnSelected : this.btnUnselected
  }

  handleAsyncLoadOptions = (inputValue) => {
    let graphqlQueryExpression = {
      query: QUERY_INDEXES,
      variables: {
        name: inputValue
      }
    }

    const transformDataIntoValueLabel = (data) => {
      return data.indexes.indexes.map(ix => {
        return { value: ix.id, label: ix.name }
      })
    }

    return new Promise(resolve => {
      this.client.query(graphqlQueryExpression).then(response => {
        resolve(transformDataIntoValueLabel(response.data))
      })
    });
  }

  handleAsyncOnChange = (inputs) => {
    const cardSetIds = inputs.map(i => i.value)
    this.setState({indexIds: cardSetIds})
    this.fetchSeries(cardSetIds, this.state.timePeriod)
  }

  fetchSeries = (cardSetIds, timePeriod) => {
    const graphqlQueryExpression = {
      query: QUERY_CARD_SET_PRICES_BY_IDS,
      variables: {
        ids: cardSetIds, 
        timePeriod: timePeriod
      }
    }

    const extractTimeSeries = (x) => {
      return x.data.cardSetPricesByIds.cardSets.map(xx => { 
        return {name: xx.name, series: xx.dateValues}
      })
    }
    
    this.client.query(graphqlQueryExpression).then(response => {
      this.setState({series: extractTimeSeries(response)})
    })
  }

  render() {
    return (
      <>
        <div className="select-index-input" style={{width: 400, display: "inline-block"}}>
          <AsyncSelect 
            onChange={this.handleAsyncOnChange}
            isMulti={true}
            cacheOptions={true}
            defaultOptions={true}
            loadOptions={this.handleAsyncLoadOptions} />
        </div>

        <div className="btn-group" role="group" aria-label="Date Ranges">
          {this.dateIntervals.map((di) => 
            <button
              className={this.getBtnClassName(di)}
              key={di} 
              onClick={() => {this.setState({timePeriod: di})}}
            >{di}</button>)
          }
        </div>

        <div>
          <MultiSeriesChart
            xdata={this.state.series}
            // width={400}
            width={600}
            height={600} 
          />
        </div>
      </>
    )
  }  
  
  // const {loading, error, data} = useQuery(QUERY_TIME_SERIES_COLLECTION_BY_IDS, {
  //   variables: {
  //     ids: indexIds,
  //     timePeriod: timePeriod
  //   }
  // })

  // const handleAsyncLoadOptions = (inputValue = "") => {
  //   let graphqlQueryExpression = {
  //     query: QUERY_INDEXES,
  //     variables: {
  //       name: inputValue
  //     }
  //   }

  //   const transformDataIntoValueLabel = (data) => {
  //     return data.indexes.indexes.map(ix => { 
  //       return { value: ix.id, label: ix.name }
  //     })
  //   } 

  //   return new Promise(resolve => {
  //     props.client.query(graphqlQueryExpression).then(response => {
  //       resolve(transformDataIntoValueLabel(response.data))
  //     })
  //   });
  // }

  // const handleAsyncOnChange = (inputs) => {
  //   const values = inputs.map(i => i.value)
  //   setIndexIds(values)
  // }

  // // early exits
  // if (loading) return <p>Loading ...</p>;
  // if (error) return <p>Error ...</p>;

  // // render specific properties
  // const btnSelected = "btn btn-secondary btn-sm active"
  // const btnUnselected = "btn btn-secondary btn-sm"
  // const getBtnClassName = (di) => (timePeriod == di) ? btnSelected : btnUnselected
  // const dateIntervals = ["1d", "5d", "1m", "3m", "6m", "YTD", "1Y", "2Y", "5Y", "Max"]

  // // data transforms
  // const seriesCollection = data.timeSeriesCollectionByIds.collection;

  // return (
  //   <>
  //     <div className="chart-buttons-default">
  //       <div className="select-index-input" style={{width: 400, display: "inline-block"}}>
  //         <AsyncSelect 
  //           onChange={handleAsyncOnChange}
  //           isMulti={true}
  //           cacheOptions={true}
  //           defaultOptions={true}
  //           loadOptions={handleAsyncLoadOptions} />
  //       </div>

  //       <div className="btn-group" role="group" aria-label="Date Ranges">
  //       {dateIntervals.map((di) => 
  //           <button
  //             className={getBtnClassName(di)}
  //             key={di} 
  //             onClick={() => setTimePeriod(di) }
  //           >{di}</button>)
  //       }
  //       </div>
  //     </div>
  //     <div>
  //       <MultiSeriesChart
  //         xdata={seriesCollection}
  //         width={props.width}
  //         height={props.height} />
  //     </div>
  //   </>
  // )
}

BaseComparativeChart.propTypes = {
  client: PropTypes.any,
  width: PropTypes.number,
  height: PropTypes.number,
  names: PropTypes.arrayOf(PropTypes.string),
}

const ComparativeChart = withApollo(BaseComparativeChart);
 
const IndexesPage = () => {
  return (
    <>
      <div className="row">
        <div className="col-md-12">
          <h1 className="mt-5">Indexes Page</h1>
        </div>
      </div>

      <ComparativeChart
        names={['a', 'b']}
        width={800}
        height={600}
        />
    </>
  )
}

export default IndexesPage;
 
