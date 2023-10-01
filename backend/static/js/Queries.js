import gql from 'graphql-tag'


const QUERY_TIME_SERIES = gql`
  query ($name: String!, $timePeriod: String) {
    timeSeries(name: $name, timePeriod: $timePeriod) {
      name,
      timePeriod,
      values { 
        date,
        value
      }
    }
  }
`

const QUERY_TIME_SERIES_COLLECTION = gql`
  query ($names: [String!]!, $timePeriod: String) {
    timeSeriesCollection(names: $names, timePeriod: $timePeriod) {
      collection {
        id,
        name,
        timePeriod,
        values {
          date,
          value
        }
      }
    }
  }
`

const QUERY_TIME_SERIES_COLLECTION_BY_IDS = gql`
  query($ids: [ID!]!, $timePeriod: String) {
    timeSeriesCollectionByIds(ids: $ids, timePeriod: $timePeriod) {
      collection {
        id,
        name,
        timePeriod,
        values  {
          date,
          value
        }
      }
    }
  }
`

const QUERY_GAINING_CARDS_PRICE = gql`
  query($timePeriod: String, $count: Int) {
    topGainers(timePeriod: $timePeriod, count: $count) {
      name,
      timePeriod,
      count,
      cards {
        name,
        value
      }
    }
  }
`

const QUERY_LOSING_CARDS_PRICE = gql`
  query($timePeriod: String, $count: Int) {
    topLosers(timePeriod: $timePeriod, count: $count) {
      name,
      timePeriod,
      count,
      cards {
        name,
        value
      }
    }
  }
`

const QUERY_INDEXES = gql`
  query($name: String) {
    indexes(name: $name) {
      success,
      errors,
      indexes {
        id,
        name
      }
    }
  }
`

const QUERY_CARD_SET_PRICES_BY_IDS = gql`
  query($ids: [String], $timePeriod: String) {
    cardSetPricesByIds(ids: $ids, timePeriod: $timePeriod) {
      success,
      errors,
      cardSets {
        id,
        name,
        setSku,
        dateValues {
          date,
          value
        }
      }
    }
  }
`


const timeSeriesNames = {
  MARKET_VALUE: 'MARKET_VALUE',
}

export {
  QUERY_TIME_SERIES, 
  QUERY_TIME_SERIES_COLLECTION, 
  QUERY_TIME_SERIES_COLLECTION_BY_IDS,
  QUERY_GAINING_CARDS_PRICE,
  QUERY_LOSING_CARDS_PRICE,
  QUERY_INDEXES,
  QUERY_CARD_SET_PRICES_BY_IDS,
  timeSeriesNames
}