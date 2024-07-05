CREATE TABLE [Growers] (
    [Id] int NOT NULL IDENTITY,
    [Grower] nvarchar(max) NOT NULL,
    [State] nvarchar(max) NOT NULL,
    CONSTRAINT [PK_Growers] PRIMARY KEY ([Id])
);
GO


CREATE TABLE [Matrixes] (
    [Id] int NOT NULL IDENTITY,
    [Terpene] nvarchar(max) NOT NULL,
    [Matrix] int NOT NULL,
    [Row] int NOT NULL,
    [Column] int NOT NULL,
    [Color] nvarchar(max) NOT NULL,
    CONSTRAINT [PK_Matrixes] PRIMARY KEY ([Id])
);
GO


CREATE TABLE [RatingCategories] (
    [Id] int NOT NULL IDENTITY,
    [CategoryName] nvarchar(max) NOT NULL,
    [CategoryDescription] nvarchar(max) NOT NULL,
    [CategoryTitle] nvarchar(max) NOT NULL,
    CONSTRAINT [PK_RatingCategories] PRIMARY KEY ([Id])
);
GO


CREATE TABLE [Strains] (
    [Id] int NOT NULL IDENTITY,
    [StrainName] nvarchar(max) NOT NULL,
    [StrainDescription] nvarchar(max) NOT NULL,
    CONSTRAINT [PK_Strains] PRIMARY KEY ([Id])
);
GO


CREATE TABLE [Batches] (
    [Id] int NOT NULL IDENTITY,
    [Name] nvarchar(max) NOT NULL,
    [Date] int NOT NULL,
    [GrowerID] int NOT NULL,
    [GrowersId] int NULL,
    [StrainsId] int NULL,
    CONSTRAINT [PK_Batches] PRIMARY KEY ([Id]),
    CONSTRAINT [FK_Batches_Growers_GrowersId] FOREIGN KEY ([GrowersId]) REFERENCES [Growers] ([Id]),
    CONSTRAINT [FK_Batches_Strains_StrainsId] FOREIGN KEY ([StrainsId]) REFERENCES [Strains] ([Id])
);
GO


CREATE TABLE [Ratings] (
    [Id] int NOT NULL IDENTITY,
    [userid] nvarchar(max) NOT NULL,
    [batchId] nvarchar(max) NOT NULL,
    [OverallRating] int NULL,
    [Taste] int NULL,
    [Effect] int NULL,
    [Notes] nvarchar(max) NULL,
    [BuyAgain] bit NOT NULL,
    [BatchesId] int NULL,
    [RatingCategoriesId] int NULL,
    CONSTRAINT [PK_Ratings] PRIMARY KEY ([Id]),
    CONSTRAINT [FK_Ratings_Batches_BatchesId] FOREIGN KEY ([BatchesId]) REFERENCES [Batches] ([Id]),
    CONSTRAINT [FK_Ratings_RatingCategories_RatingCategoriesId] FOREIGN KEY ([RatingCategoriesId]) REFERENCES [RatingCategories] ([Id])
);
GO


CREATE TABLE [TerpeneValues] (
    [Id] int NOT NULL IDENTITY,
    [Grower] nvarchar(max) NOT NULL,
    [Type] nvarchar(max) NOT NULL,
    [Value] float NOT NULL,
    [Material] nvarchar(max) NOT NULL,
    [TerpName] nvarchar(max) NOT NULL,
    [Strain] nvarchar(max) NOT NULL,
    [BatchID] int NOT NULL,
    [Rating] float NOT NULL,
    [Scale] nvarchar(max) NOT NULL,
    [Date] date NOT NULL,
    [BatchesId] int NULL,
    CONSTRAINT [PK_TerpeneValues] PRIMARY KEY ([Id]),
    CONSTRAINT [FK_TerpeneValues_Batches_BatchesId] FOREIGN KEY ([BatchesId]) REFERENCES [Batches] ([Id])
);
GO


CREATE INDEX [IX_Batches_GrowersId] ON [Batches] ([GrowersId]);
GO


CREATE INDEX [IX_Batches_StrainsId] ON [Batches] ([StrainsId]);
GO


CREATE INDEX [IX_Ratings_BatchesId] ON [Ratings] ([BatchesId]);
GO


CREATE INDEX [IX_Ratings_RatingCategoriesId] ON [Ratings] ([RatingCategoriesId]);
GO


CREATE INDEX [IX_TerpeneValues_BatchesId] ON [TerpeneValues] ([BatchesId]);
GO