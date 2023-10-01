import React, { useState } from "react";
import { useQuery } from '@apollo/react-hooks';

// local imports
import SimpleSeriesChart from '../components/SimpleSeriesChart';
import BarChartHorizontal from '../components/BarChartHorizontal';
import {timeSeriesNames, QUERY_TIME_SERIES, QUERY_GAINING_CARDS_PRICE} from '../Queries';


const MarketValue = () => {  
  const [timePeriod, setTimePeriod] = useState("1m");
  
  const {loading, error, data} = useQuery(QUERY_TIME_SERIES, {
    variables: {
      name: timeSeriesNames.MARKET_VALUE, 
      timePeriod: timePeriod
    }
  })

  if (loading) return <p>Loading ...</p>
  if (error) return <p>Error ...</p>

  const series = data.timeSeries.values

  const backgroundColor = "blue"
  const color = "white"
  
  return (
    <>
      <div
        className="widget-chart" 
        style={{"backgroundColor": backgroundColor, 'color': color}}
        >
        <div>
          <h4 className="title">Estimated Yugiogh Market Value</h4>
          <h4 className="subtitle">$1,000.01</h4>
        </div>
        
        <div className="chart">
          <SimpleSeriesChart
            width={400} 
            height={300}
            series={series}
          />
        </div>

        <div className="controls">
          <button onClick={() => setTimePeriod('1m') }>1m</button>
          <button onClick={() => setTimePeriod('3m') }>3m</button>
          <button onClick={() => setTimePeriod('12m') }>12m</button>
        </div>
  
      </div>
    </>
  )
}

const TrendingUp = () => {
  const count = 10;
  const [timePeriod, setTimePeriod] = useState("1m");

  const { loading, error, data } = useQuery(QUERY_GAINING_CARDS_PRICE, {
    variables: {
      timePeriod: timePeriod,
      count: count
    }
  })

  const activeBtnClassName = "btn btn-sm btn-light active"
  const inactiveBtnClassName = "btn btn-sm btn-light"
  const getBtnClassName = (btnTp) => (timePeriod == btnTp) ? activeBtnClassName : inactiveBtnClassName

  if (loading) return <p>Loading ...</p>;
  if (error) return <p>Error ...</p>;

  return (
    <>
      <div style={{backgroundColor: "#eaedff"}}>
        <div>
          <BarChartHorizontal
            events={true}
            title={"Trending by Price"}
            xdata={data.topGainers.cards}
            sortData={true}
            width={600}
            height={300}
            margin={{ top: 30, left: 150, right: 40, bottom: 35 }}
          />
        </div>

        <div style={{textAlign: "center", paddingBottom: "10px" }} className="actions">
          <div className="btn-group" role="group">
            <button className={getBtnClassName("1m")} onClick={() => setTimePeriod('1m') }>1m</button>
            <button className={getBtnClassName("3m")} onClick={() => setTimePeriod('3m') }>3m</button>
            <button className={getBtnClassName("12m")} onClick={() => setTimePeriod('12m') }>12m</button>
          </div>
        </div>
      </div>
    </>
  )
}

const HomePage = () => {
  return (
    <>
      
      <div className="row">
        <div className="col-md-7">
          <MarketValue/>
        </div>
      </div>

      <div className="row">
        <div className="col-md-7" style={{borderStyle: "dotted"}}>
          <TrendingUp />
        </div>
      </div>
    </>
  )
}
 
export default HomePage;