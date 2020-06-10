const { gql } = require('apollo-server-express');

module.exports = gql`

type Date {
  y: Int!,
  m: Int,
  d: Int
},

type Leader {
  nameLatin: String!,
  nameOriginal: String,
  land: [String]!,
  start: Date!,
  end: Date!,
  url: String,
  id: ID!
},

type User {
  id: ID!,
  username: String!,
  email: String
},

type Query {
  hello: String,
  leaders: [Leader!]!,
  leader(id: ID!): Leader,
  lands(start: Int!, end: Int!): [String!]!
}

type Mutation {
  newLeader(name: String!): Leader,
  signUp(username: String!, email: String!, password: String!): String!,
  signIn(username: String, email: String, password: String!): String!,
  deleteUser(username: String!): String!
}
`;