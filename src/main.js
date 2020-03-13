require('dotenv').config();
const db = require('./db');
const models = require('./models/index')

const helmet = require('helmet');
const cors = require('cors');
const express = require('express');
const { ApolloServer, gql } = require('apollo-server-express');


// Run the server on a port specified in our .env file or port 4000
const port = process.env.PORT || 4000;
// Store the DB_HOST value as a variable
//const DB_HOST = process.env.DB_HOST;
const DB_HOST = "mongodb://localhost:27017";

const typeDefs = require('./schema');

// Provide resolver functions for our schema fields
const resolvers = require('./resolvers/index');

const app = express();
app.use(helmet());
app.use(cors());

db.connect(DB_HOST);
// Apollo Server setup
const server = new ApolloServer({
  typeDefs, resolvers, context: () => {
    // Add the db models to the context
    return { models };
  }
});

// Apply the Apollo GraphQL middleware and set the path to /api
server.applyMiddleware({ app, path: '/api' });

app.listen({ port }, () =>
  console.log(
    `GraphQL Server running at http://localhost:${port}${server.graphqlPath}`
  )
);
