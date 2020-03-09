// Require the mongoose library
const mongoose = require('mongoose');

// Define the leader's database schema
const leaderSchema = new mongoose.Schema(
    {
        nameLatin: {
            type: String,
            required: true
        },
        nameOriginal: {
            type: String,
            required: false
        },
        land: {
            type: [String],
            required: false
        }
    },
    {
        // Assigns createdAt and updatedAt fields with a Date type
        timestamps: true
    }
);

// Define the 'Leader' model with the schema
const Leader = mongoose.model('Leader', leaderSchema);
// Export the module
module.exports = Leader;