module.exports = {
    hello: () => 'Hello world!',
    leaders: async (parent, args, {models}) => await models.Leader.find(),
    leader: async (parent, args, {models}) => await models.Leader.findById(args.id)
}