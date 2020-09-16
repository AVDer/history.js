module.exports = {
    hello: () => 'Hello world!',
    leaders: async (parent, args, {models}) => await models.Leader.find(),
    leader: async (parent, args, {models}) => await models.Leader.findById(args.id),
    leadersRange: async (parent, {start, end}, {models}) => await models.Leader.find({$and: [{'end.y': { $gt: start}}, {'start.y': { $lt: end}} ]}),
    lands: async (parent, {start, end}, {models}) => {
        let result = new Set();
        const query = {$and: [{'end.y': { $gt: start}}, {'start.y': { $lt: end}} ]};
        const reply = await models.Leader.find(query);
        reply.forEach((leader) => {
            leader.land.forEach((lan) => result.add(lan));
        })
        return Array.from(result);
    }
}