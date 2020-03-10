const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const { AuthenticationError,
    ForbiddenError
} = require('apollo-server-express');
require('dotenv').config();

var JWT_SECRET = 'Secret56';

exports.newLeader = async (parent, args, { models }) => {
    console.log(args);
    return await models.Leader.create({
        nameLatin: args.name,
        nameOriginal: args.name
    });
};

exports.signUp = async (parent, { username, email, password }, { models }) => {
    // normalize email address
    email = email.trim().toLowerCase();
    // hash the password
    const hashed = await bcrypt.hash(password, 10);
    try {
        const user = await models.User.create({
            username,
            email,
            password: hashed
        });

        // create and return the json web token
        return jwt.sign({ id: user._id }, JWT_SECRET);
    } catch (err) {
        console.log(err);
        // if there's a problem creating the account, throw an error
        throw new Error('Error creating account');
    }
};