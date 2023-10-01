import "core-js/stable";
import "regenerator-runtime/runtime";

import React from "react"
import ReactDOM from "react-dom"
import { BrowserRouter } from "react-router-dom"
import { ApolloProvider } from "react-apollo"
import { ApolloClient } from "apollo-client"
import { InMemoryCache } from "apollo-cache-inmemory"
import { HttpLink } from "apollo-link-http"

// tier1marketplace js code
import App from "./App"
import 'bootstrap'

// tier1marketplace css and styling
import "./bootstrap.scss"
import "./index.scss"

const cache = new InMemoryCache();

const link = new HttpLink({
    uri: `/graphql`
});

const client = new ApolloClient({
  cache,
  link
});

const rootElement = document.getElementById("root")

ReactDOM.render(
    <BrowserRouter>
        <ApolloProvider client={client}>
            <App/>
        </ApolloProvider>
    </BrowserRouter>
    , rootElement
)