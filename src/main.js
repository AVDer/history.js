require('dotenv').config();
const db = require('./db');
const models = require('./models/index')

const express = require('express');
const { ApolloServer, gql } = require('apollo-server-express');


// Run the server on a port specified in our .env file or port 4000
const port = process.env.PORT || 4000;
// Store the DB_HOST value as a variable
//const DB_HOST = process.env.DB_HOST;
const DB_HOST = "mongodb://localhost:27017";

let leaders = [
  {
    "nameLatin": "Askold and Dir",
    "nameOriginal": "Аскольд и Дир",
    "land": [
      "Kievan Rus"
    ],
    "start": "842",
    "end": "882"
  },
  {
    "nameLatin": "Oleg of Novgorodr",
    "nameOriginal": "Олег Вещий",
    "land": [
      "Kievan Rus"
    ],
    "start": "882",
    "end": "912"
  },
  {
    "nameLatin": "Igor I",
    "nameOriginal": "Игорь Рюрикович",
    "land": [
      "Kievan Rus"
    ],
    "start": "913",
    "end": "945"
  },

];

// Construct a schema, using GraphQL's schema language
const typeDefs = gql`
type Leader {
  nameLatin: String!,
  nameOriginal: String,
  land: [String]!,
  start: String!,
  end: String!,
  id: ID!
},

type Query {
  hello: String,
  leaders: [Leader!]!,
  leader(id: ID!): Leader
}

type Mutation {
    newLeader(name: String!): Leader
  }
`;

// Provide resolver functions for our schema fields
const resolvers = {
  Query: {
    hello: () => 'Hello world!',
    leaders: async () => await models.Leader.find(),
    leader: async (parent, args) => await models.Leader.findById(args.id)
  },

  Mutation: {
    newLeader: async (parent, args) => {
      console.log(args);
      return await models.Leader.create({
        nameLatin: args.name,
        nameOriginal: args.name
      });
    }
  }
};

const app = express();

db.connect(DB_HOST);
// Apollo Server setup
const server = new ApolloServer({ typeDefs, resolvers });

// Apply the Apollo GraphQL middleware and set the path to /api
server.applyMiddleware({ app, path: '/api' });

app.listen({ port }, () =>
  console.log(
    `GraphQL Server running at http://localhost:${port}${server.graphqlPath}`
  )
);
