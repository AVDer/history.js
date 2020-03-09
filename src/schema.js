const { gql } = require('apollo-server-express');

module.exports = gql`
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