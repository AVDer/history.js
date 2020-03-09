{
    newLeader: async (parent, args, {models}) => {
        console.log(args);
        return await models.Leader.create({
            nameLatin: args.name,
            nameOriginal: args.name
        });
    }
}